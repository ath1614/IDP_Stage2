from flask import Flask, request, jsonify
from PIL import Image
import base64, io, torch, logging, time, gc
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

# Maximum image dimension to prevent GPU OOM errors
MAX_DIMENSION = 1200

# Memory threshold - trigger cleanup if GPU memory exceeds this (in GB)
# T4 has 16GB, keep threshold at 12GB for safety
GPU_MEMORY_THRESHOLD_GB = 12.0

# Maximum batch size for batch OCR (T4 with 16GB can handle ~3 images safely)
MAX_BATCH_SIZE = 3

# Request semaphore - prevent concurrent OCR requests
ocr_semaphore = threading.Semaphore(1)

# Request counter for periodic deep cleanup
request_counter = 0
DEEP_CLEANUP_INTERVAL = 50  # Deep cleanup every N requests

det_predictor = None
rec_predictor = None
models_loaded = False

def load_models():
    global det_predictor, rec_predictor, models_loaded
    logger.info("Loading Surya OCR models...")
    
    from surya.detection import DetectionPredictor
    from surya.recognition import RecognitionPredictor
    from surya.foundation import FoundationPredictor
    
    # Initialize predictors (this loads models)
    foundation_predictor = FoundationPredictor()
    det_predictor = DetectionPredictor()
    rec_predictor = RecognitionPredictor(foundation_predictor)
    
    models_loaded = True
    
    # Try to log device
    try:
        device = next(det_predictor.model.parameters()).device
        logger.info(f"Models loaded on: {device}")
    except:
        logger.info("Models loaded")

def resize_image_if_needed(image, max_dim=MAX_DIMENSION):
    """Resize image if any dimension exceeds max_dim to prevent GPU OOM"""
    width, height = image.size
    if width <= max_dim and height <= max_dim:
        return image, False

    # Calculate new size maintaining aspect ratio
    if width > height:
        new_width = max_dim
        new_height = int(height * (max_dim / width))
    else:
        new_height = max_dim
        new_width = int(width * (max_dim / height))

    logger.info(f"Resizing image from {width}x{height} to {new_width}x{new_height}")
    return image.resize((new_width, new_height), Image.LANCZOS), True

def clear_gpu_memory(force_deep=False):
    """Clear GPU memory cache to prevent fragmentation."""
    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.synchronize()
        torch.cuda.empty_cache()

        if force_deep:
            gc.collect()
            torch.cuda.empty_cache()
            allocated = torch.cuda.memory_allocated(0) / 1e9
            cached = torch.cuda.memory_reserved(0) / 1e9
            logger.info(f"Deep cleanup done. GPU memory - Allocated: {allocated:.2f}GB, Cached: {cached:.2f}GB")


def check_memory_threshold():
    """Check if GPU memory usage exceeds threshold and cleanup if needed."""
    if not torch.cuda.is_available():
        return

    allocated = torch.cuda.memory_allocated(0) / 1e9
    if allocated > GPU_MEMORY_THRESHOLD_GB:
        logger.warning(f"GPU memory {allocated:.2f}GB exceeds threshold {GPU_MEMORY_THRESHOLD_GB}GB. Forcing deep cleanup.")
        clear_gpu_memory(force_deep=True)

@app.route("/api/health")
def health():
    gpu_mem = None
    if torch.cuda.is_available():
        total = torch.cuda.get_device_properties(0).total_memory / 1e9
        allocated = torch.cuda.memory_allocated(0) / 1e9
        cached = torch.cuda.memory_reserved(0) / 1e9
        gpu_mem = {
            "total_gb": round(total, 2),
            "allocated_gb": round(allocated, 2),
            "cached_gb": round(cached, 2),
            "free_gb": round(total - cached, 2),
            "utilization_pct": round((allocated / total) * 100, 1)
        }
    return jsonify({
        "status": "ok" if models_loaded else "error",
        "gpu": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_memory": gpu_mem,
        "requests_processed": request_counter,
        "memory_threshold_gb": GPU_MEMORY_THRESHOLD_GB,
        "max_batch_size": MAX_BATCH_SIZE
    })


@app.route("/api/cleanup", methods=["POST"])
def force_cleanup():
    """Endpoint to manually trigger deep memory cleanup."""
    logger.info("Manual deep cleanup triggered")
    clear_gpu_memory(force_deep=True)

    gpu_mem = None
    if torch.cuda.is_available():
        gpu_mem = {
            "allocated_gb": round(torch.cuda.memory_allocated(0) / 1e9, 2),
            "cached_gb": round(torch.cuda.memory_reserved(0) / 1e9, 2)
        }

    return jsonify({
        "status": "cleanup_complete",
        "gpu_memory_after": gpu_mem
    })


@app.route("/api/ocr/batch", methods=["POST"])
def ocr_batch_endpoint():
    global request_counter

    if not models_loaded:
        return jsonify({"error": "Models not loaded"}), 503

    acquired = ocr_semaphore.acquire(timeout=180)
    if not acquired:
        return jsonify({"error": "Server busy, request timed out"}), 503

    images = []
    buffers = []
    predictions = None
    start_time = time.time()

    try:
        data = request.json
        images_b64 = data.get("images", [])
        
        if not images_b64:
            return jsonify({"error": "No images provided"}), 400

        if len(images_b64) > MAX_BATCH_SIZE:
            logger.warning(f"Batch size {len(images_b64)} exceeds max {MAX_BATCH_SIZE}, truncating")
            images_b64 = images_b64[:MAX_BATCH_SIZE]

        logger.info(f"Processing batch of {len(images_b64)} images")

        resize_info = []
        for idx, img_b64 in enumerate(images_b64):
            image_bytes = base64.b64decode(img_b64)
            buf = io.BytesIO(image_bytes)
            buffers.append(buf)

            img = Image.open(buf).convert("RGB")
            original_size = img.size
            img, was_resized = resize_image_if_needed(img)
            images.append(img)
            resize_info.append({
                "original_size": original_size,
                "processed_size": img.size,
                "resized": was_resized
            })
            logger.info(f"  Image {idx+1}: {img.size[0]}x{img.size[1]} (resized: {was_resized})")

        with torch.no_grad():
            task_names = ["ocr_with_boxes"] * len(images)
            predictions = rec_predictor(images, task_names=task_names, det_predictor=det_predictor)

        results = []
        for idx, pred in enumerate(predictions):
            lines = []
            if hasattr(pred, 'text_lines'):
                for line in pred.text_lines:
                    conf = float(getattr(line, "confidence", 1.0))
                    if conf != conf: conf = 0.0
                    lines.append({"text": line.text, "confidence": conf})
            
            text = "\n".join([l["text"] for l in lines])
            avg_conf = sum(l["confidence"] for l in lines) / len(lines) if lines else 0

            results.append({
                "text": text,
                "lines": lines,
                "confidence": avg_conf,
                **resize_info[idx]
            })

        processing_time = int((time.time() - start_time) * 1000)
        logger.info(f"Batch OCR completed: {len(results)} images in {processing_time}ms")

        return jsonify({
            "results": results,
            "batch_size": len(results),
            "processing_time_ms": processing_time
        })

    except Exception as e:
        logger.error(f"Batch OCR error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

    finally:
        if predictions is not None:
            del predictions
        for img in images:
            img.close()
        images.clear()
        for buf in buffers:
            buf.close()
        buffers.clear()

        request_counter += len(images) if images else 1
        clear_gpu_memory(force_deep=True)
        check_memory_threshold()
        ocr_semaphore.release()


@app.route("/api/ocr", methods=["POST"])
def ocr_endpoint():
    global request_counter

    if not models_loaded:
        return jsonify({"error": "Models not loaded"}), 503

    acquired = ocr_semaphore.acquire(timeout=120)
    if not acquired:
        return jsonify({"error": "Server busy, request timed out"}), 503

    image = None
    original_image = None
    predictions = None
    image_buffer = None

    try:
        data = request.json
        image_bytes = base64.b64decode(data["image"])
        image_buffer = io.BytesIO(image_bytes)
        original_image = Image.open(image_buffer)
        image = original_image.convert("RGB")

        if original_image is not image:
            original_image.close()
            original_image = None

        original_size = image.size
        image, was_resized = resize_image_if_needed(image)

        logger.info(f"Processing {image.size[0]}x{image.size[1]} image (resized: {was_resized})")

        with torch.no_grad():
            task_names = ["ocr_with_boxes"]
            predictions = rec_predictor([image], task_names=task_names, det_predictor=det_predictor)

        if not predictions:
             result = {"text": "", "lines": [], "confidence": 0.0}
        else:
            pred = predictions[0]
            lines = []
            if hasattr(pred, 'text_lines'):
                for line in pred.text_lines:
                    conf = float(getattr(line, "confidence", 1.0))
                    if conf != conf: conf = 0.0
                    lines.append({"text": line.text, "confidence": conf})

            text = "\n".join([l["text"] for l in lines])
            avg_conf = sum(l["confidence"] for l in lines) / len(lines) if lines else 0

            result = {
                "text": text,
                "lines": lines,
                "confidence": avg_conf,
                "resized": was_resized,
                "original_size": original_size,
                "processed_size": image.size
            }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

    finally:
        if predictions is not None: del predictions
        if image is not None:
            image.close()
            del image
        if original_image is not None:
            original_image.close()
            del original_image
        if image_buffer is not None:
            image_buffer.close()
            del image_buffer

        request_counter += 1
        if request_counter % DEEP_CLEANUP_INTERVAL == 0:
            clear_gpu_memory(force_deep=True)
        else:
            clear_gpu_memory()
        check_memory_threshold()
        ocr_semaphore.release()

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SURYA OCR SERVICE - Starting")
    logger.info("=" * 60)

    load_models()
    clear_gpu_memory(force_deep=True)

    if torch.cuda.is_available():
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
    
    app.run(host="0.0.0.0", port=8000, threaded=False)

from flask import Flask, request, jsonify
from vllm import LLM, SamplingParams
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model on startup
# Using Llama-3-8B-Instruct AWQ (4-bit quantized)
MODEL_NAME = "casperhansen/llama-3-8b-instruct-awq"

logger.info(f"Loading LLM: {MODEL_NAME}")
# gpu_memory_utilization=0.85 ensures we use max RAM but leave room for overhead
llm = LLM(model=MODEL_NAME, quantization="awq", gpu_memory_utilization=0.85, max_model_len=8192)
logger.info("LLM Loaded successfully")

@app.route("/api/extract", methods=["POST"])
def extract():
    try:
        data = request.json
        text = data.get("text", "")
        schema = data.get("schema", "")
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Construct Prompt for Extraction
        # REMOVED the trailing { to let model start naturally
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert document analyzer. Extract the following fields from the provided text into a valid JSON object.
Return ONLY the JSON object. Do not include markdown formatting or explanations.

Fields to extract:
{schema}

<|eot_id|><|start_header_id|>user<|end_header_id|>

Document Text:
{text}

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
        
        # Sampling params
        sampling_params = SamplingParams(
            temperature=0.1,
            max_tokens=2048,
            stop=["<|eot_id|>"]
        )
        
        # Generate
        outputs = llm.generate([prompt], sampling_params)
        generated_text = outputs[0].outputs[0].text.strip()
        
        # Cleanup markdown if present (local service usually does this too, but good to have here)
        if generated_text.startswith("```json"):
            generated_text = generated_text.split("```json")[1].split("```")[0].strip()
        elif generated_text.startswith("```"):
            generated_text = generated_text.split("```")[1].split("```")[0].strip()
            
        return jsonify({
            "result": generated_text,
            "usage": {
                "input_tokens": len(outputs[0].prompt_token_ids),
                "output_tokens": len(outputs[0].outputs[0].token_ids)
            }
        })

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

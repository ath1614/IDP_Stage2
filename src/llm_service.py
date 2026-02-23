from fastapi import FastAPI, Request, HTTPException
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.sampling_params import SamplingParams
from vllm.utils import random_uuid
import uvicorn
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("llm_service")

app = FastAPI()

# Configuration
MODEL_NAME = "Qwen/Qwen2.5-14B-Instruct-AWQ"

logger.info(f"Initializing AsyncLLMEngine with model: {MODEL_NAME}")

# Initialize engine
# gpu_memory_utilization=0.95 ensures we use max RAM for context
# quantization="awq" is explicit
# max_model_len=8192 is a safe default for T4
engine_args = AsyncEngineArgs(
    model=MODEL_NAME,
    quantization="awq",
    gpu_memory_utilization=0.98,
    max_model_len=8192,
    enforce_eager=True,
    trust_remote_code=True,
    disable_log_requests=True
)

# Create the engine
# Note: AsyncLLMEngine handles the event loop integration
engine = AsyncLLMEngine.from_engine_args(engine_args)
logger.info("AsyncLLMEngine Initialized")

@app.post("/api/extract")
async def extract(request: Request):
    """
    Endpoint to extract fields from text using the LLM.
    Expects JSON: {"text": "...", "schema": "..."}
    """
    request_id = random_uuid()
    try:
        data = await request.json()
        text = data.get("text", "")
        schema = data.get("schema", "")
        
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        logger.info(f"Received request {request_id}. Text length: {len(text)}")

        # Construct Prompt for Extraction using Qwen ChatML format
        # We pre-fill the assistant response with "{" to force JSON output
        prompt = f"""<|im_start|>system
You are an expert document analyzer. Extract the following fields from the provided text into a valid JSON object.
Return ONLY the JSON object. Do not include markdown formatting or explanations.

Fields to extract:
{schema}<|im_end|>
<|im_start|>user
Document Text:
{text}<|im_end|>
<|im_start|>assistant
{{"""
        
        # Sampling params for deterministic output (low temp)
        sampling_params = SamplingParams(
            temperature=0.1,
            max_tokens=2048,
            stop=["<|im_end|>", "<|endoftext|>"]
        )
        
        # Generate
        results_generator = engine.generate(prompt, sampling_params, request_id)
        
        # Stream results until finished
        final_output = None
        async for request_output in results_generator:
            final_output = request_output
            # In a real streaming app, we could yield here. 
            # For this batch-like API, we just wait for the final result.
            
        if final_output is None:
            raise HTTPException(status_code=500, detail="LLM generated no output")

        generated_text = final_output.outputs[0].text.strip()
        
        # Ensure it's valid JSON (prepend { if missing since we prompted it)
        # The prompt ends with "{", so the model completes the REST of the JSON.
        # So we likely need to prepend "{" to the generated text to make it valid JSON.
        if not generated_text.startswith("{"):
            result_json = "{" + generated_text
        else:
            result_json = generated_text
            
        logger.info(f"Request {request_id} completed. Output tokens: {len(final_output.outputs[0].token_ids)}")
        
        return {
            "result": result_json,
            "usage": {
                "input_tokens": len(final_output.prompt_token_ids),
                "output_tokens": len(final_output.outputs[0].token_ids)
            }
        }

    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}", exc_info=True)
        # Abort the request in the engine if it failed
        # engine.abort(request_id) # AsyncLLMEngine handles aborts if generator is cancelled, 
        # but explicit abort is good practice if we can. 
        # However, engine.abort is not always available on the main class in older versions? 
        # It is available. But here we are just catching exception.
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

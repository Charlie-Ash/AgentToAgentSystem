# Interacts first-hand with the language model
import json, re
from vllm import LLM, SamplingParams
from orchestrator.prompts import build_orchestrator_prompt

class OrchestratorLLM():

    # Initialization settings currently set to that of VLLM_RAG
    def __init__(self):
        
        self.llm = LLM(
            model="google/gemma-4-E4B",  # Gemma 4 E4B as the LLM brain of the orchestrator
            gpu_memory_utilization=0.8,  # reserve up to 80% of available VRAM for the KV cache and runtime buffers (tweak this if memory runs out when running)
            max_model_len=4096  # sets the maximum context window that vLLM will allocate KV cache for
        )  # Use this to install gemma4:26B quantized via Huggingface

        self.sampling_params = SamplingParams(
            temperature=0.65,  # temperture: randomness
            top_p=0.95,  # top_p; nucleus sampling
            max_tokens=512,  # Max tokens outputted
            repetition_penalty = 1.1  # Penalty to apply if tokens continue repeating.
        )   # top_p; nucleus sampling,

    # Used to check if the output of the tool-routing by the orchestrator is indeed a valid JSON or not
    def extract_json(self, text: str):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError(f"No JSON found: {text}")
        return json.loads(match.group(0))  # JSON structture loaded here
    
    def tool_decision(self, user_message):

        prompt = build_orchestrator_prompt(user_message)
        output = self.llm.generate([prompt], self.sampling_params)

        raw_text = output[0].outputs[0].text
        print("\nRAW MODEL OUTPUT:\n", raw_text)  # Maybe can remove this in the future

        # Parse out JSON
        parsed_out_json = self.extract_json(raw_text)

        # Hard validation for correct JSON structure
        required_keys = {"tool", "action", "args"}
        if not required_keys.issubset(parsed_out_json.keys()):
            raise ValueError(f"Invalid schema: {parsed_out_json}")

        return parsed_out_json

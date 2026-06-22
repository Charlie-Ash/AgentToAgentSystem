# Interacts first-hand with the language model
from vllm import LLM, SamplingParams
from prompts import build_orchestrator_prompt

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
    
    def tool_decision(self, user_message):

        prompt = build_orchestrator_prompt(user_message)
        output = self.llm.generate([prompt], self.sampling_params)
        tool_decision_json = output[0].outputs[0].text

        return tool_decision_json

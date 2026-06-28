# Ochestrator class's main logic
# 1. Route to correct tools according to the prompt

from vllm import LLM
import json

from orchestrator.tool_router import ToolRouter
from orchestrator.llm import OrchestratorLLM

class Orchestrator():

    def __init__(self):
        
        self.tool_route = ToolRouter()
        self.llm = OrchestratorLLM()

    def run_orchestrator(self, user_message):

        # Ask LLM what tool should be used. A structured JSON structure is returned
        decision_json_struct = self.llm.tool_decision(user_message)
        
        # Extracting tool name from returned JSON structure
        tool_name = decision_json_struct["tool"]
        tool_args = decision_json_struct["args"]

        print("LLM tool decision: ", tool_name)
        print("LLM tool argument: ", tool_args)

        # Execute tool
        result = self.tool_route.execute_tool(tool_name, tool_args)
        return result
# Ochestrator class's main logic
# 1. Route to correct tools according to the prompt

from vllm import LLM
import json

from tool_router import ToolRouter
from llm import OrchestratorLLM

class Orchestrator():

    def __init__(self):
        
        self.tool_route = ToolRouter()
        self.llm = OrchestratorLLM()

    def run_orchestrator(self, user_message):

        # Ask LLM what tool should be used. A structured JSON structure is returned
        decision_json_struct = self.llm.tool_decision(user_message)
        
        # Extracting tool name from returned JSON structure
        json_data = json.loads(decision_json_struct)
        tool_name = json_data["tool"]

        print("LLM tool decision: ", tool_name)

        # Execute tool
        result = self.tool_route.execute_tool(tool_name, decision_json_struct)
        return result
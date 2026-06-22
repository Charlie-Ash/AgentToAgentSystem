# Class that routes to the correct tool
from tools import Default_tool, RAG_tool, Notes_tool

class ToolRouter():
    
    def __init__(self):
        
        # Dictionary of all avialable tools
        self.tools = {

            "default": Default_tool(),
            "rag": RAG_tool(),
            "note": Notes_tool()

        }

    def execute_tool(self, tool_name):

        # If the returned tool does not exists
        if tool_name not in self.tools:
            return "Unknown Tool Error Occured"
        
        # Run each tool with their "run()" operation
        # This function should return the output (string format) of each tool, back to the orchestrator
        return self.tools.run(tool_name)
# Class that routes to the correct tool
from tools.default_tool import DefaultTool
from tools.rag_tool import RAGTool
from tools.notes_tool import NotesTool

class ToolRouter():
    
    def __init__(self):
        
        # Dictionary of all avialable tools
        self.tools = {

            "default": DefaultTool(),
            "rag": RAGTool(),
            "note": NotesTool()

        }

    def execute_tool(self, tool_name, tool_json_struct):

        # If the returned tool does not exists
        if tool_name not in self.tools:
            return "Unknown Tool Error Occured"
        tool = self.tools.get(tool_name)
        
        # Run each tool with their respective "run()" operation
        # This function should return the output (string format) of each tool, back to the orchestrator
        return tool.run(tool_json_struct)
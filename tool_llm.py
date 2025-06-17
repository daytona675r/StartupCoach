from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

class ToolLLM:
    def __init__(self):
        """Initialize the Tool LLM with GPT-3.5."""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Define the system prompt for tool-specific tasks
        self.system_prompt = """You are a specialized AI assistant focused on executing specific tools and functions.
        Your role is to:
        1. Understand the user's request
        2. Determine which tool or function to use
        3. Format the input correctly for the tool
        4. Return the result in a clear, structured format
        
        You have access to the following tools:
        - Business Model Canvas Generator
        - Burn Rate Calculator
        - Pitch Deck Generator
        
        Always be precise and efficient in your tool usage."""
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        
        # Create the chain
        self.chain = (
            {"input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def process_tool_request(self, user_input: str) -> str:
        """
        Process a tool-specific request using GPT-3.5.
        
        Args:
            user_input (str): The user's input requesting a tool operation
            
        Returns:
            str: The processed result from the tool
        """
        try:
            # Process the request through the chain
            result = self.chain.invoke(user_input)
            return result
        except Exception as e:
            return f"Error processing tool request: {str(e)}"
    
    def format_tool_input(self, tool_name: str, parameters: dict) -> str:
        """
        Format input for specific tools.
        
        Args:
            tool_name (str): Name of the tool to use
            parameters (dict): Parameters for the tool
            
        Returns:
            str: Formatted input for the tool
        """
        tool_prompts = {
            "business_model_canvas": "Generate a business model canvas with the following parameters: {parameters}",
            "burn_rate": "Calculate burn rate with the following financial data: {parameters}",
            "pitch_deck": "Create a pitch deck structure with the following information: {parameters}"
        }
        
        if tool_name not in tool_prompts:
            raise ValueError(f"Unknown tool: {tool_name}")
            
        return tool_prompts[tool_name].format(parameters=parameters) 
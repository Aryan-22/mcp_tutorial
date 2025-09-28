from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

async def main():
    """_summary_
    """
    client = MultiServerMCPClient(
        
        {
            "calculator":{
                "command":"python",
                 "args":["calculator.py"],
                  "transport":"stdio"
                 
                },
            
            
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"
                
            }
            
        }
        
    )
    tools = await client.get_tools()
    
    model = ChatGroq(model="deepseek-r1-distill-llama-70b")
    
    agent = create_react_agent(model, tools)
    
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    import re

    for message in response['messages']:
        content = message.content
        # Remove LaTeX math delimiters
        content = re.sub(r'\\[\[\(]', '', content)
        content = re.sub(r'\\[\]\)]', '', content)
        # Remove boxed commands
        content = re.sub(r'\\boxed\{([^}]+)\}', r'\1', content)
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        print(content.strip())
        print("---")

asyncio.run(main())
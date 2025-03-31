# Create server parameters for stdio connection
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
import asyncio
import argparse

model = ChatOpenAI(model="gpt-4o", max_completion_tokens=8192)

async def main(prompt: str):
    async with MultiServerMCPClient(
    {
        "Search": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["mcp_server.py"],
            "transport": "stdio",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        response = await agent.ainvoke({"messages": prompt})
        print(response['messages'][-1].content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your script")
    parser.add_argument("--prompt", type=str, default="")
    args = parser.parse_args()
    asyncio.run(main(args.prompt))
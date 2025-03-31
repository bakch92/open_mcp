# Langchain 이용하여 MCP 서버 구현

## 1. MCP Server
```python
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools import YouTubeSearchTool
from youtube_search import YoutubeSearch
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Search")

@mcp.tool()
def web_search(prompt: str) -> str:
    """웹 검색 결과를 가져옵니다.

    Args:
        prompt (str): Search query

    Returns:
        str: Search result
    """
    google_wrapper = GoogleSerperAPIWrapper(gl="kr", hl="ko", type="news")
    google_results = GoogleSerperRun(api_wrapper=google_wrapper)
    search_result = google_results.invoke(prompt)
    return search_result

@mcp.tool()
def youtube_video_search(prompt: str) -> dict:
    """Returns YouTube video search results in Dictionary format.

    Args:
        prompt (str): video search term

    Returns:
        dict: video search results
    """
    search = YoutubeSearch(prompt, max_results=10).to_dict()
    return search

if __name__ == "__main__":
  # Start a process that communicates via standard input/output
  mcp.run(transport="stdio")
    # mcp.run()
```

## 2. MCP Client
```python
# Create server parameters for stdio connection
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
import asyncio

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
    asyncio.run(main("MCP 영상에 대해서 찾아주세요."))
```

## How to use
```
python client.py --prompt "프롬프트 입력"
```
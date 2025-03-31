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
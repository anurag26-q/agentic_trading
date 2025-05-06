from langchain.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lancedb.rerankers import LinearCombinationReranker 
from langchain_community.vectorstores import LanceDB
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.tools.tavily_search import TavilySearchResults


from data_models.models import RagToolSchema


@tool(args_schema=RagToolSchema)
def retriever_tool(question):
  
  ' complete code for thr retriver '
  return ' '


@tool
def tavily_tool(question:str):
  ' search it '
  return TavilySearchResults(
        question,
        serach_depth='advance',
        max_results=5,
        include_answer=True,
        include_raw_content=True,
        )

@tool
def create_polygon_tool():
  'search it'
  return PolygonFinancials(api_wrapper=PolygonAPIWrapper())

@tool
def create_bing_tool():
  'search it'
  return BingSearchResults()


def get_all_tools(question):
  return [
    retriever_tool(question),
    tavily_tool,
    create_polygon_tool,
    create_bing_tool
    ]




if __name__=='__main__':
  print(get_all_tools('my question '))
from langchain_core.tools import tool
from datetime import datetime
import ast
import operator
from langchain_tavily import TavilySearch


@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions safely."""
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub, 
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](eval_expr(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_time() -> str:
    """Get the current time."""
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def web_search(query: str) -> str:
    """Search for information."""
    tool = TavilySearch(
    max_results=5,
    topic="general"
    )
    tool.invoke({"query": query})
    data = tool.invoke({"query": "What happened at the last wimbledon"})
    all_content = " ".join([item["content"] for item in data["results"] if item.get("content")])
    return all_content


tools = [calculator, get_time, web_search]
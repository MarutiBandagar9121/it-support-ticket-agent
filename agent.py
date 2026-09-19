from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from config import settings
from tools import get_avg_resolution_time_based_on_ticket_priority

MODEL = "deepseek/deepseek-v4-flash-0731"

llm = ChatOpenAI(
    model=MODEL,
    api_key=settings.open_router_api_key,
    base_url="https://openrouter.ai/api/v1",
)

tools = [get_avg_resolution_time_based_on_ticket_priority]
tools_by_name = {t.name: t for t in tools}

llm_with_tools = llm.bind_tools(tools)

messages = [HumanMessage("What's the average resolution time for tickets raised by females?")]

ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

print("Model requested tool calls:", ai_msg.tool_calls)

if ai_msg.tool_calls:
    for tool_call in ai_msg.tool_calls:
        tool_fn = tools_by_name[tool_call["name"]]
        tool_result = tool_fn.invoke(tool_call["args"])
        messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
    final_response = llm_with_tools.invoke(messages)
    print("Final answer:", final_response.content)
else:
    print("Final answer:", ai_msg.content)


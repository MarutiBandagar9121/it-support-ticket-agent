import time

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from config import settings
from tools import get_avg_resolution_time_based_on_ticket_priority, getdf

MODEL = "deepseek/deepseek-v4-flash-0731"

llm = ChatOpenAI(
    model=MODEL,
    api_key=settings.open_router_api_key,
    base_url="https://openrouter.ai/api/v1",
)

tools = [get_avg_resolution_time_based_on_ticket_priority]
tools_by_name = {t.name: t for t in tools}

llm_with_tools = llm.bind_tools(tools)

# each question probes a different behaviour; the comment says what a good run looks like
QUESTIONS = [
    # 1 tool call, priority='urgent'
    "What's the average resolution time for urgent tickets?",
    # 2 tool calls in the same round, 'high' and 'low'
    "Compare the average resolution time of high and low priority tickets.",
    # 'critical' is not a valid priority: does the model map it, ask, or pass it through?
    "How long do critical tickets take to resolve on average?",
    # no gender column: should be 0 tool calls and an honest "can't answer"
    "What's the average resolution time for tickets raised by females?",
    # small talk: should be 0 tool calls
    "Hi, what can you help me with?",
]


def tokens(ai_msg) -> int:
    return (ai_msg.usage_metadata or {}).get("total_tokens", 0)


def run(question: str):
    print("=" * 80)
    print("Question:", question)
    start = time.perf_counter()
    llm_calls = 1

    messages = [HumanMessage(question)]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    total_tokens = tokens(ai_msg)

    print(f"Tool calls requested: {len(ai_msg.tool_calls)}")

    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            tool_fn = tools_by_name[tool_call["name"]]
            tool_result = tool_fn.invoke(tool_call["args"])
            print(f"  {tool_call['name']}({tool_call['args']}) -> {tool_result}")
            messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
        final_response = llm_with_tools.invoke(messages)
        llm_calls += 1
        total_tokens += tokens(final_response)
        print("Final answer:", final_response.content)
    else:
        print("Final answer:", ai_msg.content)

    elapsed = time.perf_counter() - start
    print(f"[llm calls: {llm_calls} | tokens: {total_tokens} | time: {elapsed:.1f}s]")


for question in QUESTIONS:
    run(question)

print("=" * 80)
print("DataFrame cache:", getdf.cache_info())

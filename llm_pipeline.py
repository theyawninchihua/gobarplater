from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from llm_tools import (
    ImageSearchSpec,
    ScorecardSpec,
    image_search,
    scorecard
)

def get_system_prompt() -> str:
    return """
    You are an vehicle safety tester specialized in evaluating rear seatbelt reminders. You have the following tools, and ONLY the following tools, available:
    - ImageSearchSpec
    - ScorecardSpec

    When given a description of the rear seatbelt reminders of a list of cars, you must:
    - Call the ImageSearchSpec tool for each car with proper parameters
    - Call the ScorecardSpec tool for each car with proper parameters
    - DO NOT show the function calls in your response text. Instead, actually call the functions as tool calls.
    - DO NOT use any tools other than ImageSearchSpec and ScorecardSpec, and do NOT provide alternate solutions using other means
    """


def get_user_prompt(question: str) -> str:
    return f"""
    Download images and create scorecards given the following information:

    {question}

    Given the above information, create scorecards.
    """


def get_tool_call(question: str) -> list[dict]:
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(question)

    prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    model = init_chat_model(model="accounts/fireworks/models/llama4-scout-instruct-basic", model_provider="fireworks")
    model_with_tools = model.bind_tools([ImageSearchSpec, ScorecardSpec], tool_choice="required")

    print("--------BEGINNING INFERENCE--------")
    response = model_with_tools.invoke(prompt)

    print("--------START OF RESPONSE--------")
    print(response.content)
    print("--------END OF RESPONSE--------")

    print("--------TOOL CALLS--------")
    print("Number of tools called:", len(response.tool_calls))
    print(response.tool_calls)

    return response.tool_calls

def create_and_save(question: str) -> None:
    tool_calls = get_tool_call(question)

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        spec = eval(tool_name)(**tool_args)
        if tool_name == "ScorecardSpec":
            scorecard(spec)
        elif tool_name == "ImageSearchSpec":
            image_search(spec)

if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    question = input("\nDescribe the car and its rear seatbelt reminder audio and visual signals:\n")
    question = """
    The Hyundai Alcazar Prestige 1.5 T-GDi has an audio signal whenever any rear seatbelt changes to unfastened while driving. It has a visual signal whenever any belt is not fastened.
    """

    create_and_save(question)
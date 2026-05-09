from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

def calculate(expression):
    return eval(expression)

tools = [
    {
        "name": "calculate",
        "description": "Evaluates a math expression and returns the result. Use this whenever you need to perform calculations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, e.g. '123 * 456'"
                }
            },
            "required": ["expression"]
        }
    }
]

def run_agent(user_message):
    print(f"\nUser: {user_message}")
    print("-" * 40)

    messages = [{"role": "user", "content": user_message}]

    # Keep looping until Claude is done
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # Claude is done - print the answer and exit the loop
        if response.stop_reason == "end_turn":
            print("Final answer:", response.content[0].text)
            break

        # Claude wants to use a tool - handle every tool it requested
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = calculate(block.input["expression"])
                    print(f"Tool call: calculate('{block.input['expression']}') = {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            messages.append({"role": "user", "content": tool_results})

# Ask something that requires multiple calculations
run_agent("What is (123 * 456) + (789 * 12)? Show me each step.")
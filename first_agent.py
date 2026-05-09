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

messages = [
    {"role": "user", "content": "What is 123 multiplied by 456?"}
]

# First call - Claude requests a tool
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print("Step 1 - Stop reason:", response.stop_reason)

# Pull the tool request out of the response
tool_call = response.content[0]
expression = tool_call.input["expression"]
result = calculate(expression)

print(f"Step 2 - Ran tool: calculate('{expression}') = {result}")

# Send the result back to Claude
messages.append({"role": "assistant", "content": response.content})
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": tool_call.id,
        "content": str(result)
    }]
})

# Second call - Claude now has the result and can answer
final_response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print("Step 3 - Stop reason:", final_response.stop_reason)
print("Final answer:", final_response.content[0].text)
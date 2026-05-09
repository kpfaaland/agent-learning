from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is 123 multiplied by 456?"}
    ]
)

print("Full response object:")
print(response)
print("\n--- Just the parts we care about ---")
print("Stop reason:", response.stop_reason)
print("Content type:", response.content[0].type)
print("Text:", response.content[0].text)
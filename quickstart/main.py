from openai import OpenAI
from dotenv import load_dotenv

# OPENAI_API_KEY loaded here
load_dotenv()

client = OpenAI()

response = client.responses.create(
  model="gpt-4.1",
  input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

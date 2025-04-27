from pprint import pprint

from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

from numeric import ChatGptNumericPrompter, ClaudeNumericPrompter, EnsembleNumericPrompter

# Load the API keys.
load_dotenv()

# Create the OpenAI client.
oclient = OpenAI()

# Create the Anthropic client.
aclient = Anthropic()

# Create various prompters to use in an ensemble.
claudePrompter = ClaudeNumericPrompter(client=aclient)
gpt4_1Prompter = ChatGptNumericPrompter(client=oclient, model="gpt-4.1")
gpt4oPrompter = ChatGptNumericPrompter(client=oclient, model="gpt-4o")
prompters = [
  claudePrompter,
  gpt4_1Prompter,
  gpt4oPrompter,
]

# Create the ensemble prompter.
ensemblePrompter = EnsembleNumericPrompter(prompters = prompters)

questions = [
  "What is 1 divided by 0?",
  "What is 28379456426 divided by 8788?",
  "How many grains of sand are there on Earth?",
  "What year will artificial intelligence surpass human intelligence?",
  "How many stars are visible from Earth with the naked eye?",
  "How many species are currently undiscovered by science?",
  "What percentage of the ocean floor has been explored?",
  "How many hours does it take to truly master a skill?",
  "How many planets with intelligent life exist in our galaxy?",
  "In how many years will humans achieve immortality (if ever)?",
  "How many words does the average person speak in a lifetime?",
  "How many thoughts does a person have per day?",
  "What is the ideal number of hours of sleep for optimal health?",
  "By what year will renewable energy replace fossil fuels completely?",
  "How many years will it take before space tourism becomes affordable for the average person?",
  "How many gallons of paint would be needed to paint every building in New York City?",
  "How many generations does it take for significant evolutionary change to occur in a species?",
  "What is the maximum human lifespan achievable through medical advancements?",
  "How many times will the average person fall in love in their lifetime?",
  "By what year will global poverty be completely eliminated (if ever)?",
  "How many bytes of information can the human brain store?",
  "How many people can sustainably live on Earth?",
]

for question in questions:
  # response = gpt4_1Prompter.prompt(question)
  # response = claudePrompter.prompt(question)
  response = ensemblePrompter.prompt(question)
  print("========")
  print("question: " + question)
  print(f"answer: {response.answer}")
  # print("reasoning: " + response.reasoning_steps)
  print(f"abstained: {response.voting.abstained}")
  print(f"stddev: {response.voting.stddev}")
  print("votes:")
  pprint(response.voting.votes)

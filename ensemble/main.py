from pprint import pprint

from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

from prompter import ClaudePrompter, ChatGptPrompter, EnsemblePrompter

# Load the API keys.
load_dotenv()

# Create the OpenAI client.
oclient = OpenAI()

# Create the Anthropic client.
aclient = Anthropic()

# Define the options the AI can respond with.
options=["yes","no"]

# Create various prompters to use in an ensemble.
claudePrompter = ClaudePrompter(client=aclient, options=options)
gpt4_1Prompter = ChatGptPrompter(client=oclient, options=options, model="gpt-4.1")
gpt4oPrompter = ChatGptPrompter(client=oclient, options=options, model="gpt-4o")
prompters = [
  claudePrompter,
  gpt4_1Prompter,
  gpt4oPrompter,
]

# Create the ensemble prompter.
ensemblePrompter = EnsemblePrompter(prompters = prompters)

questions = [
  "Will large-language-model-based tools remain the dominant interface for everyday computing five years from now?",
  "Is universal basic income (UBI) a net positive for social welfare in advanced economies?",
  "Should governments treat broadband Internet access as a public utility, regulated like electricity or water?",
  "Can nuclear fission realistically supply at least one-third of global electricity by 2050?",
  "Is mandatory corporate reporting of greenhouse-gas emissions an effective driver of decarbonization?",
  "Does full-time remote work generally lead to equal or better productivity than in-office work for most knowledge workers?",
  "Will CRISPR gene-editing therapies become affordable for middle-income patients within the next decade?",
  "Can you currently use CRISPR to get rid of APOE4 genes related to Alzheimers in your offspring?",
  "Should social-media platforms be legally liable for algorithmic amplification of harmful misinformation?",
  "Can planting and protecting additional forests alone sequester enough carbon to meet the Paris Agreement targets?",
  "Is a permanent human settlement on Mars technically feasible with resources available by 2075?",
]

for question in questions:
  response = ensemblePrompter.prompt(question)
  print("========")
  print("question: " + question)
  print("answer: " + response.answer)
  # print("reasoning: " + response.reasoning_steps)
  print(f"consensus: {response.voting.majority}/{response.voting.total}")
  print("votes:")
  pprint(response.voting.votes)

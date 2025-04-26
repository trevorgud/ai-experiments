from abc import ABC, abstractmethod
from collections import Counter
import uuid
import json
import multiprocessing
from multiprocessing.dummy import Pool
from typing import List

from pydantic import BaseModel


class PromptResponse(BaseModel):
  answer: str
  reasoning_steps: str

class VotingBreakdown(BaseModel):
  total: int
  majority: int
  votes: dict

class PromptVotingResponse(PromptResponse):
  voting: VotingBreakdown


class Prompter(ABC):
  @abstractmethod
  def prompt(self, message: str) -> PromptResponse:
    pass


class EnsemblePrompter(Prompter):
  def __init__(self, prompters):
    self.prompters = prompters

  def prompt(self, message: str) -> PromptResponse:
    responses = self._delegate_prompts(message)
    combined = self._combine_responses(responses)
    voting = self._breakdown_votes(combined, responses)
    return PromptVotingResponse(
      answer=combined.answer,
      reasoning_steps=combined.reasoning_steps,
      voting=voting,
    )

  def _delegate_prompts(self, message) -> List[PromptResponse]:
    nprompters = len(self.prompters)
    # Create a wrapper function that takes a tuple of (prompter_index, message)
    def prompt_with_index(args):
      prompter_index, msg = args
      return self.prompters[prompter_index].prompt(msg)
    # Create argument tuples: (prompter_index, message)
    args_list = [(i, message) for i in range(nprompters)]
    # Use process pool to execute in parallel
    with Pool(processes=nprompters) as pool:
      results = pool.map(prompt_with_index, args_list)
    return results

  def _combine_responses(self, responses: List[PromptResponse]) -> PromptResponse:
    # print("All responses:")
    # for response in responses:
    #   print(response)
    # Extract answers from responses
    answers = [response.answer for response in responses]
    # Find the most common answer
    # In case of a tie, returns the first one found.
    most_common_answer = Counter(answers).most_common(1)[0][0]
    # Return the first response with the most common answer
    return next(resp for resp in responses if resp.answer == most_common_answer)

  def _breakdown_votes(self, majority: PromptResponse, responses: List[PromptResponse]) -> VotingBreakdown:
    total = len(responses)
    nmajority = 0
    votes = {}
    for i in range(len(responses)):
      name = self.prompters[i].name
      answer = responses[i].answer
      if answer == majority.answer:
        nmajority += 1
      votes[name] = answer
    return VotingBreakdown(
      total=total,
      majority=nmajority,
      votes=votes,
    )


class ChatGptPrompter(Prompter):
  def __init__(self, client, options, model="gpt-4.1"):
    self.client = client
    self.options = options
    self.model = model
    self.name = "openai-"+model

  def prompt(self, message: str) -> PromptResponse:
    sys = self._system_prompts()
    messages = [
      *sys,
      {"role": "user", "content": message},
    ]
    response = self.client.responses.parse(
      model=self.model,
      input=messages,
      text_format=PromptResponse,
    )
    return response.output_parsed

  def _system_prompts(self):
    options_str = ", ".join(self.options)
    return [
      {
        "role":"system",
        "content": "Answer the question and lay out your reasoning step by step",
      },
      {
        "role":"system",
        "content": f"Respond in the answer with only one of these options: {options_str}",
      }
    ]


class ClaudePrompter():
  def __init__(self, client, options, model = "claude-3-5-sonnet-latest"):
    self.client = client
    self.options = options
    self.model = model
    self.name = "anthropic-"+model
    self.retries = 3

  def prompt(self, message: str) -> PromptResponse:
    # Submit the prompt with retries.
    # Assumes _single_prompt will return None on errors and need retry.
    for i in range(self.retries):
      response = self._single_prompt(message)
      if response is not None:
        return response
    return None

  def _single_prompt(self, message: str) -> PromptResponse:
    sys = self._system_prompts()
    messages = [
      {"role": "user", "content": message},
    ]
    response = self.client.messages.create(
      max_tokens=1024,
      system=sys,
      messages=messages,
      model=self.model,
    )
    pr = self._parse_json(response.content[0].text)
    return pr

  def _parse_json(self, response) -> PromptResponse:
    try:
      j = json.loads(response)
      pr = PromptResponse.parse_obj(j)
      return pr
    except:
      print("failed to parse JSON:")
      print(response)
      return None

  def _system_prompts(self):
    options_str = ", ".join(self.options)
    sample = PromptResponse(
      answer=self.options[0],
      reasoning_steps="<add several reasoning steps here>",
    )
    js = sample.model_dump_json()
    prompts = [
      "Answer the question and lay out your reasoning step by step",
      f"Respond with only JSON in this format: {js}",
      f"Respond in the answer with only one of these options: {options_str}",
    ]
    sys = "\n".join(prompts)
    return sys

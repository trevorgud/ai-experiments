from abc import ABC, abstractmethod
from multiprocessing.dummy import Pool
from typing import List, Union
import json
import math
import multiprocessing
import statistics

from pydantic import BaseModel


class NumericPromptResponse(BaseModel):
  answer: Union[float, int, None]
  reasoning_steps: str

class NumericVotingBreakdown(BaseModel):
  total: int
  abstained: int
  stddev: Union[float, None]
  votes: dict

class NumericPromptVotingResponse(NumericPromptResponse):
  voting: NumericVotingBreakdown


class NumericPrompter(ABC):
  @abstractmethod
  def prompt(self, message: str) -> NumericPromptResponse:
    pass


class EnsembleNumericPrompter(NumericPrompter):
  def __init__(self, prompters):
    self.prompters = prompters

  def prompt(self, message: str) -> NumericPromptResponse:
    responses = self._delegate_prompts(message)
    combined = self._combine_responses(responses)
    voting = self._breakdown_votes(combined, responses)
    return NumericPromptVotingResponse(
      answer=combined.answer,
      reasoning_steps=combined.reasoning_steps,
      voting=voting,
    )

  def _delegate_prompts(self, message) -> List[NumericPromptResponse]:
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

  def _combine_responses(self, responses: List[NumericPromptResponse]) -> NumericPromptResponse:
    final_answer = None
    answers = []
    for response in responses:
      if response.answer is not None:
        answers.append(response.answer)

    # Must have a majority of prompters returning a real number to allow a non-null response.
    min_answers = math.ceil(len(responses) / 2)
    # If you instead want to allow a numeric answer if even a single prompter responds numerically:
    # min_answers = 1
    if len(answers) >= min_answers:
      final_answer = statistics.mean(answers)

    # NOTE: Numeric reasoning steps are ommitted. Can't combine these as easily as categorical.
    # Consider allowing different strategies (ex: median) and use that median value reasoning.
    return NumericPromptResponse(answer=final_answer, reasoning_steps="")

  def _breakdown_votes(
    self,
    combined: NumericPromptResponse,
    responses: List[NumericPromptResponse],
  ) -> NumericVotingBreakdown:
    total = len(responses)
    abstained = 0
    stddev = None
    votes = {}
    answers = []
    # Collect valid answers and abstained vote count.
    for i in range(len(responses)):
      name = self.prompters[i].name
      answer = responses[i].answer
      if answer is not None:
        answers.append(answer)
      else:
        abstained += 1
      votes[name] = answer
    # Only calc stddev if we found a valid answer, otherwise leave as None.
    if len(answers) > 0 and combined.answer is not None:
      stddev = statistics.stdev(answers)
    return NumericVotingBreakdown(
      total=total,
      abstained=abstained,
      stddev=stddev,
      votes=votes,
    )


class ChatGptNumericPrompter(NumericPrompter):
  def __init__(self, client, model="gpt-4.1"):
    self.client = client
    self.model = model
    self.name = "openai-"+model

  def prompt(self, message: str) -> NumericPromptResponse:
    sys = self._system_prompts()
    messages = [
      *sys,
      {"role": "user", "content": message},
    ]
    response = self.client.responses.parse(
      model=self.model,
      input=messages,
      text_format=NumericPromptResponse,
    )
    return response.output_parsed

  def _system_prompts(self):
    return [
      {
        "role":"system",
        "content": "Answer the question and lay out your reasoning step by step",
      },
      {
        "role":"system",
        "content": "Prefer choosing any number over no answer. No answer can only be used if a sentinel value is required.",
      },
    ]


class ClaudeNumericPrompter():
  def __init__(self, client, model = "claude-3-5-sonnet-latest"):
    self.client = client
    self.model = model
    self.name = "anthropic-"+model
    self.retries = 3

  def prompt(self, message: str) -> NumericPromptResponse:
    # Submit the prompt with retries.
    # Assumes _single_prompt will return None on errors and need retry.
    for i in range(self.retries):
      response = self._single_prompt(message)
      if response is not None:
        return response
    return None

  def _single_prompt(self, message: str) -> NumericPromptResponse:
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

  def _parse_json(self, response) -> NumericPromptResponse:
    try:
      j = json.loads(response)
      pr = NumericPromptResponse.parse_obj(j)
      return pr
    except:
      print("failed to parse JSON:")
      print(response)
      return None

  def _system_prompts(self):
    sample = NumericPromptResponse(
      answer=10,
      reasoning_steps="<add several reasoning steps here>",
    )
    other_samples = [
      NumericPromptResponse(answer=None, reasoning_steps="<reasoning>"),
      NumericPromptResponse(answer=0, reasoning_steps="<reasoning>"),
      NumericPromptResponse(answer=0.5, reasoning_steps="<reasoning>"),
    ]
    prompt_samples = "Other valid JSONs: \n"
    for s in other_samples:
      j = s.model_dump_json()
      prompt_samples += j + "\n"
    js = sample.model_dump_json()
    prompts = [
      "Answer the question and lay out your reasoning step by step.",
      f"Respond with only JSON in this format: {js}",
      "Make sure to escape newlines in the reasoning to ensure valid JSON.",
      prompt_samples,
    ]
    sys = "\n".join(prompts)
    return sys

# ai-experiments
Playing around with generative AI

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 ./main.py
```

Ensemble Answers:
```
question: Can nuclear fission realistically supply at least one-third of global electricity by 2050?
answer: yes
reasoning: 1. Current nuclear capacity provides about 10% of global electricity and has proven scalability
2. Many countries including China, India, and Russia are actively expanding nuclear programs
3. Advanced reactor designs (SMRs, Gen IV) are becoming commercially viable
4. Growing recognition of nuclear as clean energy for climate goals
5. Historical evidence shows rapid nuclear buildout is possible (France achieved 75% nuclear power in 15 years)
6. Rising electricity demand and decarbonization goals create strong incentives
7. Existing nuclear infrastructure and expertise can support expansion
8. 30-year timeline allows for planning, construction and grid integration
consensus: 2/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'no',
 'openai-gpt-4o': 'yes'}
```
```
========
question: Will large-language-model-based tools remain the dominant interface for everyday computing five years from now?
answer: yes
consensus: 2/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'no',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Is universal basic income (UBI) a net positive for social welfare in advanced economies?
answer: yes
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Should governments treat broadband Internet access as a public utility, regulated like electricity or water?
answer: yes
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Can nuclear fission realistically supply at least one-third of global electricity by 2050?
answer: yes
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Is mandatory corporate reporting of greenhouse-gas emissions an effective driver of decarbonization?
answer: yes
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Does full-time remote work generally lead to equal or better productivity than in-office work for most knowledge workers?
answer: yes
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Will CRISPR gene-editing therapies become affordable for middle-income patients within the next decade?
answer: yes
consensus: 2/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'no',
 'openai-gpt-4o': 'yes'}
========
question: Can you currently use CRISPR to get rid of APOE4 genes related to Alzheimers in your offspring?
answer: no
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'no',
 'openai-gpt-4.1': 'no',
 'openai-gpt-4o': 'no'}
========
question: Should social-media platforms be legally liable for algorithmic amplification of harmful misinformation?
answer: yes
consensus: 2/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'no',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
========
question: Can planting and protecting additional forests alone sequester enough carbon to meet the Paris Agreement targets?
answer: no
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'no',
 'openai-gpt-4.1': 'no',
 'openai-gpt-4o': 'no'}
========
question: Is a permanent human settlement on Mars technically feasible with resources available by 2075?
answer: yes
consensus: 3/3
votes:
{'anthropic-claude-3-5-sonnet-latest': 'yes',
 'openai-gpt-4.1': 'yes',
 'openai-gpt-4o': 'yes'}
```

Numeric Ensemble Answers:
```bash
python3 ./main2.py
```
```
========
question: What is 1 divided by 0?
answer: None
abstained: 3
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': None,
 'openai-gpt-4o': None}
========
question: What is 28379456426 divided by 8788?
answer: 3230308.9267498334
abstained: 0
stddev: 572.2006981565179
votes:
{'anthropic-claude-3-5-sonnet-latest': 3230712,
 'openai-gpt-4.1': 3230560.7802495,
 'openai-gpt-4o': 3229654}
========
question: How many grains of sand are there on Earth?
answer: 7.166666666666667e+18
abstained: 0
stddev: 2.8867513459481286e+17
votes:
{'anthropic-claude-3-5-sonnet-latest': 7.5e+18,
 'openai-gpt-4.1': 7000000000000000000,
 'openai-gpt-4o': 7000000000000000000}
========
question: What year will artificial intelligence surpass human intelligence?
answer: None
abstained: 3
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': None,
 'openai-gpt-4o': None}
========
question: How many stars are visible from Earth with the naked eye?
answer: 5666.666666666667
abstained: 0
stddev: 577.3502691896258
votes:
{'anthropic-claude-3-5-sonnet-latest': 6000,
 'openai-gpt-4.1': 6000,
 'openai-gpt-4o': 5000}
========
question: How many species are currently undiscovered by science?
answer: 8550000
abstained: 1
stddev: 70710.67811865476
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': 8500000,
 'openai-gpt-4o': 8600000}
========
question: What percentage of the ocean floor has been explored?
answer: 15
abstained: 0
stddev: 8.660254037844387
votes:
{'anthropic-claude-3-5-sonnet-latest': 5,
 'openai-gpt-4.1': 20,
 'openai-gpt-4o': 20}
========
question: How many hours does it take to truly master a skill?
answer: 10000
abstained: 0
stddev: 0.0
votes:
{'anthropic-claude-3-5-sonnet-latest': 10000,
 'openai-gpt-4.1': 10000,
 'openai-gpt-4o': 10000}
========
question: How many planets with intelligent life exist in our galaxy?
answer: None
abstained: 3
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': None,
 'openai-gpt-4o': None}
========
question: In how many years will humans achieve immortality (if ever)?
answer: None
abstained: 3
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': None,
 'openai-gpt-4o': None}
========
question: How many words does the average person speak in a lifetime?
answer: 590970666.6666666
abstained: 0
stddev: 466277348.2181322
votes:
{'anthropic-claude-3-5-sonnet-latest': 860000000,
 'openai-gpt-4.1': 52560000,
 'openai-gpt-4o': 860352000}
========
question: How many thoughts does a person have per day?
answer: 27466.666666666668
abstained: 0
stddev: 36834.947174298126
votes:
{'anthropic-claude-3-5-sonnet-latest': 6200,
 'openai-gpt-4.1': 70000,
 'openai-gpt-4o': 6200}
========
question: What is the ideal number of hours of sleep for optimal health?
answer: 7.833333333333333
abstained: 0
stddev: 0.28867513459481287
votes:
{'anthropic-claude-3-5-sonnet-latest': 7.5,
 'openai-gpt-4.1': 8,
 'openai-gpt-4o': 8}
========
question: By what year will renewable energy replace fossil fuels completely?
answer: None
abstained: 3
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': None,
 'openai-gpt-4o': None}
========
question: How many years will it take before space tourism becomes affordable for the average person?
answer: 21.666666666666668
abstained: 0
stddev: 7.637626158259733
votes:
{'anthropic-claude-3-5-sonnet-latest': 15,
 'openai-gpt-4.1': 30,
 'openai-gpt-4o': 20}
========
question: How many gallons of paint would be needed to paint every building in New York City?
answer: 17500000
abstained: 1
stddev: 3535533.9059327375
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': 20000000,
 'openai-gpt-4o': 15000000}
========
question: How many generations does it take for significant evolutionary change to occur in a species?
answer: 1000
abstained: 1
stddev: 0.0
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': 1000,
 'openai-gpt-4o': 1000}
========
question: What is the maximum human lifespan achievable through medical advancements?
answer: None
abstained: 2
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': 150,
 'openai-gpt-4o': None}
========
question: How many times will the average person fall in love in their lifetime?
answer: 3
abstained: 0
stddev: 1.0
votes:
{'anthropic-claude-3-5-sonnet-latest': 3,
 'openai-gpt-4.1': 2,
 'openai-gpt-4o': 4}
========
question: By what year will global poverty be completely eliminated (if ever)?
answer: None
abstained: 3
stddev: None
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': None,
 'openai-gpt-4o': None}
========
question: How many bytes of information can the human brain store?
answer: 9166666666667.5
abstained: 0
stddev: 13768926368214.424
votes:
{'anthropic-claude-3-5-sonnet-latest': 2.5,
 'openai-gpt-4.1': 25000000000000,
 'openai-gpt-4o': 2500000000000}
========
question: How many people can sustainably live on Earth?
answer: 10000000000
abstained: 1
stddev: 0.0
votes:
{'anthropic-claude-3-5-sonnet-latest': None,
 'openai-gpt-4.1': 10000000000,
 'openai-gpt-4o': 10000000000}
```
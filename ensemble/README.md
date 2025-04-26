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
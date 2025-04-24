# ai-experiments
Playing around with generative AI

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 ./main.py \
--repo-path /home/trevor/git/source \
--start-commit 417d46676057 \
--end-commit 03467aa1b66a5

python3 ./main.py \
--repo-path /home/trevor/git/source \
--target-branch main \
--source-branch cleanup/resolve-staticcheck-issues

# Assumes target is main branch
python3 ./main.py \
--repo-path /home/trevor/git/source \
--source-branch cleanup/resolve-staticcheck-issues
```

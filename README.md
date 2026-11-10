# Local LLM 8GB VRAM test

The exact files from my video **Best Local LLM for 8GB VRAM (I Tested 5 on My RTX 4060)** on the Microlearn YouTube channel, so you can run the same test on your own machine and compare your numbers with mine.

My machine: RTX 4060 Laptop GPU (8 GB VRAM), 12th-gen Intel i7, 32 GB RAM, Ollama 0.35.0, default downloads of each model.

## What's here

| File | What it is |
|---|---|
| `tasks2.py` | The coding task: 6 functions with docstrings and no code. Give it to a model and ask it to implement every function. |
| `test_tasks2.py` | 33 pytest tests for those functions. An empty file fails 33/33, a correct solution passes 33/33. |
| `handbook_long.txt` | A long, fictional company handbook (about 23,000 words, 28K tokens) with look-alike decoy facts. |
| `questions.json` | 10 questions about the handbook, each with its correct answer. |
| `bench2.py` | The script I used to run the models through Ollama's API (speed, code, documents). |

## Run the coding test

1. Paste the whole of `tasks2.py` into the model with: "Implement every function so it does exactly what its docstring says. Standard library only. Return the whole file."
2. Save the model's answer as `tasks2.py` (next to `test_tasks2.py`).
3. Run `pip install pytest` once, then `pytest -q test_tasks2.py` and read the score out of 33.

## Run the document test

Give the model the whole of `handbook_long.txt` plus one question from `questions.json` at a time (it needs a 32K context window: `ollama run <model>` then `/set parameter num_ctx 32768`), and check its answer against `"a"`. Time how long it takes to answer all 10.

## Or run everything with the script

With Ollama running and the models pulled:

```
python bench2.py qwen3.5:4b qwen3.5:9b gemma4:12b gpt-oss:20b qwen3.6:35b-a3b
```

It writes `results2.json` and each model's code to `out2/`. Settings: temperature 0, seed 1, and thinking off (gpt-oss: "low").

## My results

| Model | Speed (tok/s) | Code (33 tests) | Documents: all 10 right in |
|---|---|---|---|
| Qwen3.5 4B | 67.7 | 0 (rambled to the 4,096-token cap) | 17 s |
| Qwen3.5 9B | 41.4 | 24 | 29 s |
| Gemma 4 12B | 29.0 | 33 | 55 s |
| gpt-oss 20B | 31.1 | 0 (one extra quote mark broke the file) | 70 s |
| Qwen3.6 35B-A3B | 40.3 | 31 | 150 s |

Speed is the median of 3 warm runs at 4K context. If your numbers are very different, tell me in the comments with your GPU and RAM.

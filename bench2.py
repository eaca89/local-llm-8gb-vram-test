"""Round 2, clean run (nothing else on the GPU). Speed x3 (median), hard code task (33 tests),
long documents (~30K tokens, decoys). Writes results2.json and out2/."""
import json, os, re, shutil, statistics, subprocess, sys, tempfile, time, urllib.request

API = "http://localhost:11434"
MODELS = sys.argv[1:] or ["qwen3.5:4b", "qwen3.5:9b", "gemma4:12b", "gpt-oss:20b", "qwen3.6:35b-a3b"]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out2")
SPEED_PROMPT = "Explain to a new engineer, in about 300 words, how a hash map works and when it gets slow."


def post(path, body, timeout=3600):
    req = urllib.request.Request(API + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def gen(model, prompt, ctx, predict=4096):
    body = {"model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0, "seed": 1, "num_ctx": ctx, "num_predict": predict}}
    body["think"] = "low" if model.startswith("gpt-oss") else False
    t = time.time()
    r = post("/api/generate", body)
    r["wall_s"] = round(time.time() - t, 1)
    return r


def rates(r):
    ev = r.get("eval_count", 0) / max(r.get("eval_duration", 1) / 1e9, 1e-9)
    pe = r.get("prompt_eval_count", 0) / max(r.get("prompt_eval_duration", 1) / 1e9, 1e-9)
    return round(ev, 1), round(pe, 1)


def split():
    out = subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout
    m = re.search(r"(\d+%/\d+% CPU/GPU|100% GPU|100% CPU)", out)
    s = re.search(r"\s(\d+(?:\.\d+)? GB)\s", out)
    return (m.group(1) if m else "?"), (s.group(1) if s else "?")


def vram_mib():
    q = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                       capture_output=True, text=True).stdout
    return int(q.strip().splitlines()[0])


def unload_all():
    for line in subprocess.run(["ollama", "ps"], capture_output=True, text=True).stdout.splitlines()[1:]:
        name = line.split()[0]
        post("/api/generate", {"model": name, "keep_alive": 0})
    time.sleep(3)


def code_job(model):
    src = open(os.path.join(HERE, "tasks2.py")).read()
    prompt = ("Implement every function in this Python file so it does exactly what its docstring says. "
              "Return the complete file in one ```python code block and nothing else.\n\n```python\n" + src + "\n```")
    r = gen(model, prompt, 8192)
    blocks = re.findall(r"```(?:python)?\n(.*?)```", r.get("response", ""), re.S)
    code = blocks[-1] if blocks else r.get("response", "")
    d = tempfile.mkdtemp()
    shutil.copy(os.path.join(HERE, "test_tasks2.py"), d)
    open(os.path.join(d, "tasks2.py"), "w").write(code)
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=d,
                         capture_output=True, text=True, timeout=120).stdout
    m = re.search(r"(\d+) passed", out)
    open(os.path.join(OUT, model.replace(":", "_") + "_code.py"), "w").write(code)
    return {"passed": int(m.group(1)) if m else 0, "of": 33, "wall_s": r["wall_s"], "tok_s": rates(r)[0],
            "out_tokens": r.get("eval_count")}


def docs_job(model):
    hb = open(os.path.join(HERE, "handbook_long.txt")).read()
    qs = json.load(open(os.path.join(HERE, "questions.json")))
    prompt = ("Answer from the handbook below only. Reply with a numbered list, one short answer per question.\n\n"
              + hb + "\n\nQuestions:\n" + "\n".join(f"{i + 1}. {q['q']}" for i, q in enumerate(qs)))
    r = gen(model, prompt, 32768, 600)
    ans = r.get("response", "")
    lines = {int(m.group(1)): m.group(2) for m in re.finditer(r"^\s*(\d+)[.)]\s*(.*)$", ans, re.M)}
    norm = lambda s: s.lower().replace(",", "").replace(" ", "")
    right = sum(1 for i, q in enumerate(qs) if norm(q["a"]) in norm(lines.get(i + 1, "")))
    open(os.path.join(OUT, model.replace(":", "_") + "_docs.txt"), "w").write(ans)
    ev, pe = rates(r)
    sp, size = split()
    return {"right": right, "of": len(qs), "wall_s": r["wall_s"], "tok_s": ev, "prompt_tok_s": pe,
            "prompt_tokens": r.get("prompt_eval_count"), "split": sp, "size": size, "vram_mib": vram_mib()}


os.makedirs(OUT, exist_ok=True)
path = os.path.join(HERE, "results2.json")
results = json.load(open(path)) if os.path.exists(path) else {}
unload_all()
idle = vram_mib()
for m in MODELS:
    print("==", m, flush=True)
    unload_all()
    t = time.time()
    gen(m, "Say OK.", 8192, 5)
    load_s = round(time.time() - t, 1)
    runs = [rates(gen(m, SPEED_PROMPT, 8192, 400)) for _ in range(3)]
    sp, size = split()
    res = {"idle_vram_mib": idle, "load_s": load_s, "split_8k": sp, "size_8k": size, "vram_8k_mib": vram_mib(),
           "speed_tok_s": statistics.median(x[0] for x in runs), "speed_runs": [x[0] for x in runs],
           "prompt_tok_s": statistics.median(x[1] for x in runs)}
    print(" speed", res, flush=True)
    res["code"] = code_job(m)
    print(" code", res["code"], flush=True)
    unload_all()
    res["docs"] = docs_job(m)
    print(" docs", res["docs"], flush=True)
    results[m] = res
    json.dump(results, open(path, "w"), indent=1)
    unload_all()
print("ROUND2 FINISHED", flush=True)

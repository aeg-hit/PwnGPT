# PwnGPT
Caputre the flag with Large Language Models. Constructed by langgraph, and I learn a lot from langgraph doument, thanks for them.

# Workflow
![workflow](./assert/workflow.png)
Decompile binary file by the Hex-Rays decompiler (version 8.3.0.230608) in this project.

# Run
Test LLMs by benchmark.py, run PwnGPT in llm4ctf.py.

# Directory
## preprocessing/ 
load file, analysis, embedding and save.

## processing/ 
llm application with langgraph.

## pwn/ （benchmark）
pwn challenges that are collected online. 
rop1 and rop4 ret2text, rop2 and rop3 ret2libc, 
rop5 ret2text(64bit), rop6 ret2text(64bit, gadget), rop7 ret2text(64bit, gadget, rop chain), rop8-9 ret2shellcode, rop10 canary(ret2libc fmt).
fmt1 write, fmt2 read, fmt3 hijack retaddr, fmt4-5 hijack GOT.                     
int1 Integer Overflow and ret2text, int1 Integer Overflow and ret2shellcode.
heap1 UAF, heap2 heap overflow. (heap challenges with libc are too difficult to llm)
### problems.txt: 
(1) file info (2) decompile (3) readelf -r  (get plt: objdump -d ./pwn/stack/rop-2/rop2 | grep @plt) (4) strings -d (5) ROPgadget --binary rop --only "pop|ret" > g.txt (6) checksec --format=json --file=

## cve/
Collect cve vulnerable Docker environments and exploit code from github. For more information, see [here](./cve/README.md).
### CVE-2011-2523 : vsftpd Backdoor Command Execution (cve-1)
### CVE-2018-10933 : libssh Authentication Bypass Vulnerability (cve-2)

# Usage as Library

You can import `llmgraph` from `processing` as a library in your own project.

## Quick Start

```python
from processing import llmgraph

# Load a decompiled C file
decfile = llmgraph.get_decompilefile('./example/level0.c')[0]

# Run the LangGraph workflow to generate exploit code
result = llmgraph.run_graph(decfile.page_content)

# Access generated code
code_solution = result["generation"]
print(code_solution.prefix)   # Problem analysis and approach
print(code_solution.imports)  # Import statements
print(code_solution.code)     # Exploit code
```

## Configuration

Set the following environment variable before importing:

```bash
export OPENAI_API_KEY="your-api-key"
```

Key configurable attributes on the `llmgraph` module:

| Attribute | Description | Default |
|-----------|-------------|---------|
| `expt_llm` | LLM model identifier | `openai/gpt-4o-2024-11-20` |
| `base` | API base URL | `https://openrouter.ai/api/v1` |
| `max_iterations` | Max retry iterations in graph workflow | `1` |

Example:

```python
import llmgraph

llmgraph.expt_llm = "qwen-max"
llmgraph.base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
llmgraph.max_iterations = 2  # Enable reflection & retry on failure
```

## API Reference

### `get_decompilefile(path)`
Load a decompiled source file using LangChain's `TextLoader`.

- **path** *(str)*: Path to the decompiled C file.
- **Returns**: List of `Document` objects; use `[0]` to get the document and `.page_content` for the text.

### `run(concatenated_content)`
Direct LLM invocation with structured output and retry logic.

- **concatenated_content** *(str)*: Challenge context (e.g., decompiled code, problem description).
- **Returns**: `code` object with `.prefix`, `.imports`, `.code`.

### `run_graph(info, messages=[])`
Run the full LangGraph workflow: **generate → check imports → execute → reflect → retry**.

- **info** *(str)*: Challenge context / problem description.
- **messages** *(list, optional)*: Extra message tuples, e.g., `[('user', 'The binary path is /path/to/binary')]`. Useful for providing additional hints such as binary file address or vulnerability type.
- **Returns**: `dict` with keys:
  - `generation`: `code` object (`.prefix`, `.imports`, `.code`)
  - `error`: `"yes"` / `"no"`
  - `messages`: Full conversation history
  - `iterations`: Number of iterations performed

### `run_direct(info, messages=[])`
Direct LLM call without structured output (fallback for models that don't support `json_schema` / tool calling).

- Same parameters as `run_graph`.
- **Returns**: Raw LLM response (`.content` contains the text).

### `subprocess_check(path)`
Execute a generated Python script in a subprocess with a 20-second timeout.

- **path** *(str)*: Path to the Python script to execute.
- **Returns**: `(subprocess.Popen, stdout_text)`
- **Raises**: `Exception` on timeout, import error, or execution failure.

## Complete Example

```python
from processing import llmgraph
from preprocessing import constructInfo, file

# 1. Analyze challenge directory
pwn_path = file.PwnInfo("./pwn/stack/", "rop")
clist = pwn_path.get_clist()      # List of C source files
blist = pwn_path.get_binarylist() # List of binary paths

# 2. Load decompiled code
decfile = llmgraph.get_decompilefile(clist[0])[0]

# 3. Build problem description
funclist = constructInfo.get_funclist(
    llmgraph.expt_llm, llmgraph.base, decfile.page_content)
problem = constructInfo.get_problem(
    blist[0], pwn_path.filename + "1", funclist)

# 4. Run the graph workflow
result = llmgraph.run_graph(problem)

# 5. Save the generated exploit
if result["error"] == "no" and "generation" in result:
    with open('exploit.py', 'w') as f:
        f.write(result["generation"].imports + "\n" + result["generation"].code)
```

# attention

some LLMs do not support ["json_schema"](https://platform.openai.com/docs/guides/structured-outputs), such as o1-preview. When we use qwen, we use OpenAI's tool-calling (formerly called function calling) for `with_structured_output` function.

# Citation

```bibtex
@inproceedings{peng-etal-2025-pwngpt,
    title = "{P}wn{GPT}: Automatic Exploit Generation Based on Large Language Models",
    author = "Peng, Wanzong  and
      Ye, Lin  and
      Du, Xuetao  and
      Zhang, Hongli  and
      Zhan, Dongyang  and
      Zhang, Yunting  and
      Guo, Yicheng  and
      Zhang, Chen",
    editor = "Che, Wanxiang  and
      Nabende, Joyce  and
      Shutova, Ekaterina  and
      Pilehvar, Mohammad Taher",
    booktitle = "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.acl-long.562/",
    doi = "10.18653/v1/2025.acl-long.562",
    pages = "11481--11494",
    ISBN = "979-8-89176-251-0",
}
```

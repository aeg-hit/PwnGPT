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

## pwn/ 
pwn challenges that are collected online. 
rop1 and rop4 ret2text, rop2 and rop3 ret2libc, 
rop5 ret2text(64bit), rop6 ret2text(64bit, gadget), rop7 ret2text(64bit, gadget, rop chain), rop8-9 ret2shellcode, rop10 canary(ret2libc fmt).
fmt1 write, fmt2 read, fmt3 hijack retaddr, fmt4-5 hijack GOT.
int1 Integer Overflow and ret2text, int1 Integer Overflow and ret2shellcode.
heap1 UAF, heap2 heap overflow. (heap challenges with libc are too difficult to llm)
### problems.txt: 
(1) file info (2) decompile (3) readelf -r  (get plt: objdump -d ./pwn/stack/rop-2/rop2 | grep @plt) (4) strings -d (5) ROPgadget --binary rop --only "pop|ret" > g.txt (6) checksec --format=json --file=

# attention
some LLMs do not support "json_schema" (https://platform.openai.com/docs/guides/structured-outputs), such as o1-preview. When we use qwen, we use OpenAI's tool-calling (formerly called function calling) for 'with_structured_output'.
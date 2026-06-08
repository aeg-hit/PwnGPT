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

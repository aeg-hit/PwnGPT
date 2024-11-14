# LLM4CTF
Caputre the flag with Large Language Models. Constructed by langgraph and chromadb, I learn from langgraph doument.

# Workflow
![workflow](./assert/workflow.png)
I only implemented the exploit system (RAG section). Decompile by IDA.

## Method
RAG (Retrieval Augmented Generation) then check code and reflect.

## Directory
download/ some data document about ctf (datasets).

preprocessing/ load file, embedding and save.

processing/ llm application with langgraph.

pwn/ pwn challenges that are collected online. rop8-9 shellcode; rop10 canary. 
problems.txt: (1) file (2) decompile (3) readelf -r  (4) strings -d 
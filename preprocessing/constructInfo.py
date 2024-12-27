from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

import subprocess
import getpass
import re
import json

from preprocessing import analysis

info_expt_llm = "qwen-plus-2024-11-27"
# base="https://openrouter.ai/api/v1"
info_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
key = getpass.getpass("Information Extraction Key:")
key = None if key == '0' else key
info_llm = ChatOpenAI(temperature=0, model=info_expt_llm,
                      base_url=info_base, api_key=key)

# Data model


class funclist(BaseModel):
    """Schema for code solutions to questions about LCEL."""

    func_name: list[str] = Field(description="List of function names")


class info(BaseModel):
    """Schema for code solutions to questions about LCEL."""

    code: str = Field(description="Code block")


def get_funclist(expt_llm, base, de_str):
    llm = ChatOpenAI(temperature=0, model=expt_llm, base_url=base)
    structured_llm_claude = llm.with_structured_output(funclist)
    prompt = ChatPromptTemplate.from_messages([("system", '''You are a expert on Capture the Flag (CTF) competition, and are good at Binary Exploitation (pwn) challenges. \n 
                                                There is a pwn challenge in the CTF competition, we need to write code to solve the challenge and here is C file decompiled from the challenge :\n ------- \n  {context} \n ------- \n 
                                                '''), ("placeholder", "{messages}")])
    flist = (prompt | structured_llm_claude).invoke({"context": de_str, "messages": [
        ("human", "Please find the functions that affect our exploit code, just give me a list of function names.")]})

    if 'main' not in flist.func_name:
        flist.func_name.append('main')
    print(flist.func_name)

    # add other relate function, but this will add 'put' and 'print' sometime

    # prompt.append(("ai", str(result1.func_name)))
    # prompt.append(("human", "Are there other functions that print characters? Please give me a list of function names, which also affect our result code."))
    # print(prompt)
    # result2=(prompt | structured_llm_claude).invoke({"context":de_str})
    # print(result2.func_name)

    info_structured_llm_claude = info_llm.with_structured_output(info)
    infomation = (prompt | info_structured_llm_claude).invoke({"context": de_str, "messages": [
        ("human", f"This is a list of key function names: {flist.func_name}. I only focus on these functions, please extract the code of these functions from the C file.")]})
    return infomation.code


def get_baseinfo(path):
    result = subprocess.run(['file', path], check=True,
                            capture_output=True, text=True)
    strs = result.stdout.split(':')[1]

    return strs.split(',')


def get_strings(path):
    result = subprocess.run(['strings', '-d', path],
                            check=True, capture_output=True, text=True)
    # search by pattern (/bin/、/usr/bin/ 、/sbin/)
    binary_paths_pattern = re.compile(r'(/\b(?:bin|usr/bin|sbin)\b/[^"\s]+)')

    matches = binary_paths_pattern.findall(result.stdout)

    # if matches:
    #     print("Found potential binary paths:")
    #     for match in matches:
    #         print(f"  - {match}")
    # else:
    #     print("No potential binary paths found.")

    return matches


def get_secinfo(path):
    result = subprocess.run(['checksec', '--format=json', '--file='+path],
                            check=True, capture_output=True, text=True)
    strs = result.stdout

    return strs


def get_gadget(path):
    result = subprocess.run(['ROPgadget', '--binary', path, '--only', 'pop|ret'],
                            check=True, capture_output=True, text=True)
    strs = result.stdout

    return strs


def get_plt(path):
    result = subprocess.run(['readelf', '-r', path],
                            check=True, capture_output=True, text=True)
    strs = result.stdout.split('\n\n')
    result = ''
    for section in strs:
        if section.startswith("Relocation section '.rel.plt'"):
            result = section
    return result


def static_analysis(code):
    result = ''
    functions = analysis.find_functions(code)
    extracted_funcs = analysis.extract_main_and_calls(functions)
    for func_name, func_code in extracted_funcs.items():
        result += func_code+"\n\n"
    return result


def get_problem(path, filename, funclist):
    baseinfo = get_baseinfo(path)
    info_num = 1
    problem = f'Challenge is a{baseinfo[0]} file and the file path is "{path}".\n1.Here is the key function for exploit in the C file decompiled from {filename}:\n'
    funclist += '\n\n'
    problem += funclist
    info_num += 1
    # checksec
    secinfo = json.loads(get_secinfo(path))[path]
    problem += f"{info_num}.Here is the file security infomation identified by 'checksec' command:\n"
    info_num += 1
    problem += json.dumps(secinfo)+'\n\n'
    # printable strings
    strings = get_strings(path)
    if strings:
        problem += f"{info_num}.Here is some printable strings in the data sections of {filename}:\n"
        info_num += 1
        for match in strings:
            problem += match+'\n'
        problem += '\n'
    # ROPgadget
    ROPgadget = get_gadget(path)
    problem += f"{info_num}.We use ROPgadget to search gadgets on {filename}:\n"
    info_num += 1
    problem += ROPgadget+'\n'
    # Relocation section (.plt is useful for read. When relro is full, .rel.plt (.got.plt) is unuseful)
    if secinfo['relro'] != 'full':
        relplt = get_plt(path)
        problem += f"{info_num}.Here is information of the file's relocation section:\n"
        info_num += 1
        problem += relplt+'\n'
    return problem

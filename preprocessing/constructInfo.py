from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

import getpass

info_expt_llm = "qwen-plus-2024-11-27"
# base="https://openrouter.ai/api/v1"
info_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
key=getpass.getpass("Information Extraction Key:")
key= None if key == '0' else key
info_llm = ChatOpenAI(temperature=0, model=info_expt_llm, base_url=info_base,api_key=key)

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
    flist=(prompt | structured_llm_claude).invoke({"context":de_str, "messages":[("human", "Please find the functions that affect our exploit code, just give me a list of function names.")]})
    print(flist.func_name)

    # add other relate function, but this will add 'put' and 'print' sometime

    # prompt.append(("ai", str(result1.func_name)))
    # prompt.append(("human", "Are there other functions that print characters? Please give me a list of function names, which also affect our result code."))
    # print(prompt)
    # result2=(prompt | structured_llm_claude).invoke({"context":de_str})
    # print(result2.func_name)

    info_structured_llm_claude = info_llm.with_structured_output(info)
    infomation=(prompt | info_structured_llm_claude).invoke({"context":de_str, "messages":[("human", f"This is a list of key function names: {flist.func_name}. I only focus on these functions, please extract the code of these functions from the C file.")]})
    return infomation.code




    






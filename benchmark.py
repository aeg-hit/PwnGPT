from processing import llmgraph
from preprocessing import file

import subprocess
from pprint import pprint

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def evaluate_0():
    # evaluate 0: pure llm without reflect (flag = "do not reflect" max_iterations=1)
    # pwn_path=file.PwnInfo("./pwn/stack/", "rop")
    # pwn_path=file.PwnInfo("./pwn/string/", "fmt")
    pwn_path = file.PwnInfo("./pwn/integer/", "int")
    clist = pwn_path.get_clist()
    print("Start: ")
    for i in range(len(clist)):
        pprint(clist[i])
        decfile = llmgraph.get_decompilefile(clist[i])[0]
        c_infohead = "\nHere is the decompiled C file:\n"
        resultcode = llmgraph.run_graph(c_infohead+decfile.page_content)
        # save
        with open(pwn_path.list[i]+f'/result_1_{llmgraph.expt_llm}.txt', 'w') as f:
            pprint(resultcode, stream=f)

llm = ChatOpenAI(temperature=0, model=llmgraph.expt_llm, base_url=llmgraph.base)
code_gen_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a expert on Capture the Flag (CTF) competition, and are good at Binary Exploitation (pwn) challenges. \n 
        There is a pwn challenge in the CTF competition, and here is information about the challenge to you for analysis:  \n ------- \n  {context} \n ------- \n
          Answer the user question based on the above provided information. Here is the user question:""",
            ),
            ("placeholder", "{messages}"),
        ]
    )
gen_chain = code_gen_prompt | llm

def evaluate_1():
    # evaluate 1: key information analysis
    pwn_path = file.PwnInfo("./pwn/stack/", "rop")
    blist = pwn_path.get_binarylist()
    i = 0
    file_result = subprocess.run(['file', blist[i]],
                                 check=True, capture_output=True, text=True)

    check_result = subprocess.run(['checksec', '--format=json', '--file='+blist[i]],
                                  check=True, capture_output=True, text=True)
    
    pprint(blist[i])
    contest = f"\nHere is the file infomation created by 'file' command:\n{file_result.stdout}\n\nHere is the file security infomation created by 'checksec' command:\n{check_result.stdout}"
    question="Please analyse these information."
    resultcode=gen_chain.invoke(
        {"context": contest, "messages": [("user", question)]}
    )
    print(resultcode)
    # save
    with open(pwn_path.list[i]+f'/evaluate_1_{llmgraph.expt_llm}.txt', 'w') as f:
        print(resultcode.content, stream=f)



if __name__ == "__main__":
    evaluate_1()

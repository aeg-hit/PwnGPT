from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain_community.document_loaders import TextLoader

def get_decompilefiles(path):
    textload=TextLoader(path)
    return textload.load()

### OpenAI api




# Data model
class code(BaseModel):
    """Schema for code solutions to questions about LCEL."""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")

class MainGraph:
    # Grader prompt that use placeholder function
    code_gen_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a coding assistant with expertise in LCEL, LangChain expression language. \n 
        Here is a full set of LCEL documentation:  \n ------- \n  {context} \n ------- \n Answer the user 
        question based on the above provided documentation. Ensure any code you provide can be executed \n 
        with all required imports and variables defined. Structure your answer with a description of the code solution. \n
        Then list the imports. And finally list the functioning code block. Here is the user question:""",
            ),
            ("placeholder", "{messages}"),
        ]
    )

    def __init__(self, expt_llm, base):
        self.llm= ChatOpenAI(temperature=0, model=expt_llm, base_url=base)

    def run(self):
        code_gen_chain_oai = self.code_gen_prompt | self.llm.with_structured_output(code)
        question = "How do I build a RAG chain in LCEL?"
        solution = code_gen_chain_oai.invoke(
            {"context": self.concatenated_content, "messages": [("user", question)]}
        )
        return solution

def run(concatenated_content)->code:
        # Grader prompt that use placeholder function
    code_gen_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a expert on Capture the Flag (CTF) competition, and are good at Binary Exploitation (pwn) challenges. \n 
        There is a pwn challenge in the CTF competition, and here is the decompiled C file to you for analysis:  \n ------- \n  {context} \n ------- \n Answer the user 
        question based on the above provided file. Ensure any code you provide can be executed \n 
        with all required imports and variables defined. Structure your answer with a description of the code solution. \n
        Then list the imports. And finally list the functioning code block. Here is the user question:""",
            ),
            ("placeholder", "{messages}"),
        ]
    )

    expt_llm = "qwen-plus"
    base="https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm= ChatOpenAI(temperature=0, model=expt_llm, base_url=base)
    code_gen_chain_oai = code_gen_prompt | llm.with_structured_output(code)
    question = "How do I use pwntool to solve this challange?"
    solution = code_gen_chain_oai.invoke(
            {"context": concatenated_content, "messages": [("user", question)]}
        )
    return solution
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain_community.document_loaders import TextLoader

import os
import getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var]=getpass.getpass(f"{var}:")


_set_env("OPENAI_API_KEY")

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

class MainChain:
    # Grader prompt that use placeholder function
    code_gen_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a expert on Capture the Flag (CTF) competition, and are good at Binary Exploitation (pwn) challenges. \n 
        There is a pwn challenge in the CTF competition, and here is the decompiled C file to you for analysis:  \n ------- \n  {context} \n ------- \n Answer the user 
        question based on the above provided file. Ensure any code you provide can be executed \n 
        with all required imports and variables defined. Structure your answer: 1) a prefix describing the code solution, 2) the imports, 3) the functioning code block. \n
    Invoke the code tool to structure the output correctly. Here is the user question:""",
            ),
            ("placeholder", "{messages}"),
        ]
    )

    def __init__(self, expt_llm, base):
        self.llm= ChatOpenAI(temperature=0, model=expt_llm, base_url=base)
        self.structured_llm_claude = self.llm.with_structured_output(code, include_raw=True)
        # Chain with output check
        self.code_chain_claude_raw = (MainChain.code_gen_prompt | self.structured_llm_claude | MainChain.check_claude_output)
        # This will be run as a fallback chain
        fallback_chain = MainChain.insert_errors | self.code_chain_claude_raw
        N = 3  # Max re-tries
        code_gen_chain_re_try = self.code_chain_claude_raw.with_fallbacks(
            fallbacks=[fallback_chain] * N, exception_key="error"
        )
        # Optional: With re-try to correct for failure to invoke tool
        self.code_gen_chain_retry = code_gen_chain_re_try | MainChain.parse_output

        # No re-try
        self.code_gen_chain = MainChain.code_gen_prompt | self.structured_llm_claude | MainChain.parse_output




    # Optional: Check for errors in case tool use is flaky
    def check_claude_output(tool_output):
        """Check for parse error or failure to call the tool"""

        # Error with parsing
        if tool_output["parsing_error"]:
            # Report back output and parsing errors
            print("Parsing error!")
            raw_output = str(tool_output["raw"].content)
            error = tool_output["parsing_error"]
            raise ValueError(
                f"Error parsing your output! Be sure to invoke the tool. Output: {raw_output}. \n Parse error: {error}"
            )

        # Tool was not invoked
        elif not tool_output["parsed"]:
            print("Failed to invoke tool!")
            raise ValueError(
                "You did not use the provided tool! Be sure to invoke the tool to structure the output."
            )
        return tool_output
    
    def insert_errors(inputs):
        """Insert errors for tool parsing in the messages"""

        # Get errors
        error = inputs["error"]
        messages = inputs["messages"]
        messages += [
            (
                "assistant",
                f"Retry. You are required to fix the parsing errors: {error} \n\n You must invoke the provided tool.",
            )
        ]
        return {
            "messages": messages,
            "context": inputs["context"],
        }
    
    def parse_output(solution):
        """When we add 'include_raw=True' to structured output,
        it will return a dict w 'raw', 'parsed', 'parsing_error'."""

        return solution["parsed"]




expt_llm = "qwen-plus"
base="https://dashscope.aliyuncs.com/compatible-mode/v1"
chain=MainChain(expt_llm,base)

def run(concatenated_content)->code:
    question = "How do I use pwntool to solve this challange?"
    solution = chain.code_gen_chain_retry.invoke(
            {"context": concatenated_content, "messages": [("user", question)]}
        )
    return solution

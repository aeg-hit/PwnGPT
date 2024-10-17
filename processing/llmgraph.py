from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from langchain_community.document_loaders import TextLoader

from typing import List
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START

import os
import getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var]=getpass.getpass(f"{var}:")


_set_env("OPENAI_API_KEY")

def get_decompilefile(path):
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



#init llm
expt_llm = "qwen-plus"
base="https://dashscope.aliyuncs.com/compatible-mode/v1"
chain=MainChain(expt_llm,base)


## test chain
def run(concatenated_content)->code:
    question = "How do I use pwntool to solve this challange?"
    solution = chain.code_gen_chain_retry.invoke(
            {"context": concatenated_content, "messages": [("user", question)]}
        )
    return solution



concatenated_content=get_decompilefile('./example/level0.c')[0]

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        error : Binary flag for control flow to indicate whether test error was tripped
        messages : With user question, error messages, reasoning
        generation : Code solution
        iterations : Number of tries
    """

    error: str
    messages: List
    generation: str
    iterations: int

### Parameter

# Max tries
max_iterations = 1
# Reflect
# flag = 'reflect'
flag = "do not reflect"

### Nodes


def generate(state: GraphState):
    """
    Generate a code solution

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """



    # State
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]

    print(f"---  GENERATING CODE SOLUTION: {iterations}  ---")
    # We have been routed back to generation with an error
    if error == "yes":
        messages += [
            (
                "user",
                "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
            )
        ]

    # Solution
    code_solution = chain.code_gen_chain.invoke(
        {"context": concatenated_content, "messages": messages}
    )
    messages += [
        (
            "assistant",
            f"{code_solution.prefix} \n Imports: {code_solution.imports} \n Code: {code_solution.code}",
        )
    ]

    # Increment
    iterations = iterations + 1
    return {"generation": code_solution, "messages": messages, "iterations": iterations}


def code_check(state: GraphState):
    """
    Check code

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, error
    """

    print("---CHECKING CODE---")

    # State
    messages = state["messages"]
    code_solution = state["generation"]
    iterations = state["iterations"]

    # Get solution components
    imports = code_solution.imports
    code = code_solution.code

    # Check imports
    try:
        exec(imports)
    except Exception as e:
        print("---CODE IMPORT CHECK: FAILED---")
        print(f"Your solution failed the import test: {e}")
        error_message = [("user", f"Your solution failed the import test: {e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # Check execution
    try:
        exec(imports + "\n" + code)
    except Exception as e:
        print("---CODE BLOCK CHECK: FAILED---")
        print(f"Your solution failed the code execution test: {e}")
        error_message = [("user", f"Your solution failed the code execution test: {e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # No errors
    print("---NO CODE TEST FAILURES---")
    return {
        "generation": code_solution,
        "messages": messages,
        "iterations": iterations,
        "error": "no",
    }


def reflect(state: GraphState):
    """
    Reflect on errors

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation
    """

    print("---REFLECTING ON CODE ERROR---")

    # State
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["generation"]

    # Prompt reflection

    # Add reflection
    reflections = chain.code_gen_chain.invoke(
        {"context": concatenated_content, "messages": messages}
    )
    messages += [("assistant", f"Here are reflections on the error: {reflections}")]
    return {"generation": code_solution, "messages": messages, "iterations": iterations}


### Edges


def decide_to_finish(state: GraphState):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        if flag == "reflect":
            return "reflect"
        else:
            return "generate"
        
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("generate", generate)  # generation solution
workflow.add_node("check_code", code_check)  # check code
workflow.add_node("reflect", reflect)  # reflect

# Build graph
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "reflect": "reflect",
        "generate": "generate",
    },
)
workflow.add_edge("reflect", "generate")
app = workflow.compile()

def run_graph():
    question = "How do I use pwntool to solve this challange?"
    solution = app.invoke({"messages": [("user", question)], "iterations": 0, "error": ""})
    return solution
import os
import getpass

from preprocessing import file
from processing import llmgraph

from pprint import pprint



def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var]=getpass.getpass(f"{var}:")



if __name__ == "__main__":
    _set_env("OPENAI_API_KEY")
    decfile=llmgraph.get_decompilefiles('./example/level0.c')[0]
    resultcode=llmgraph.run(decfile.page_content)
    pprint(resultcode.prefix)
    pprint(resultcode.imports)
    pprint(resultcode.code)

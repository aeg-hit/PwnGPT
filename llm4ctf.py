from preprocessing import file
from processing import llmgraph

from pprint import pprint





if __name__ == "__main__":
    #test base invoke
    decfile=llmgraph.get_decompilefiles('./example/level0.c')[0]
    resultcode=llmgraph.run(decfile.page_content)
    pprint(resultcode.prefix)
    print("\n\nimports\n\n")
    pprint(resultcode.imports)
    print("\n\ncode\n\n")
    pprint(resultcode.code)

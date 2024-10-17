from preprocessing import file
from processing import llmgraph

from pprint import pprint





if __name__ == "__main__":
    #test base invoke
    # decfile=llmgraph.get_decompilefile('./example/level0.c')[0]
    # resultcode=llmgraph.run(decfile.page_content)

    #test graph
    result=llmgraph.run_graph()
    resultcode=result["generation"]

    #pretty print
    pprint(resultcode.prefix)
    print("\n\nimports\n\n")
    pprint(resultcode.imports)
    print("\n\ncode\n\n")
    pprint(resultcode.code)

    #save
    with open('result.txt','w') as f:
        pprint(result, stream=f)

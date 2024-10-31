from processing import llmgraph
from preprocessing import file, retrieval


from pprint import pprint

def test1():
    # test base invoke
    decfile = llmgraph.get_decompilefile('./example/level0.c')[0]
    resultcode = llmgraph.run(decfile.page_content)


def test2():
    # test graph
    decfile = llmgraph.get_decompilefile('./example/level0.c')[0]
    c_infohead="\nHere is the decompiled C file:\n"
    result = llmgraph.run_graph(c_infohead+decfile.page_content)
    resultcode = result["generation"]

    # pretty print
    pprint(resultcode.prefix)
    print("\n\nimports\n\n")
    pprint(resultcode.imports)
    print("\n\ncode\n\n")
    pprint(resultcode.code)

    # save
    with open('result.txt', 'w') as f:
        pprint(result, stream=f)


def test_retrieval():
    # #retriever
    # retriever=retrieval.save_vector(['./download/buffer.txt'])
    # res=retriever.similarity_search("overflow")
    # pprint(res)
    store = retrieval.vectorstore
    pprint(store.similarity_search("overflow", k=1))

def evaluate_1():
    #evaluate 1
    # pwn_path=file.PwnInfo("./pwn/stack/", "rop")
    # pwn_path=file.PwnInfo("./pwn/string/", "fmt")
    pwn_path=file.PwnInfo("./pwn/integer/", "int")
    clist=pwn_path.get_clist()
    print("Start: ")
    for i in range(len(clist)):
        pprint(clist[i])
        decfile = llmgraph.get_decompilefile(clist[i])[0]
        c_infohead="\nHere is the decompiled C file:\n"
        resultcode = llmgraph.run_graph(c_infohead+decfile.page_content)
        # save
        with open(pwn_path.list[i]+'/result_1.txt', 'w') as f:
            pprint(resultcode, stream=f)

if __name__ == "__main__":
    proc, out =llmgraph.subprocess_check('./pwn/stack/rop-1/try.py')
    print("wtf",proc.returncode,out)
    with open('./ctftest.py', 'w') as f:
        print(out, file=f)





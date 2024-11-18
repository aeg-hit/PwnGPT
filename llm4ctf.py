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
    c_infohead = "\nHere is the decompiled C file:\n"
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


def test_subprocess():
    proc, out = llmgraph.subprocess_check('./pwn/stack/rop-1/try.py')
    print("wtf", proc.returncode, out)


def evaluate_2():
    # evaluate 2:  llm with reflect (max_iterations>1)
    llmgraph.max_iterations = 2
    # pwn_path=file.PwnInfo("./pwn/stack/", "rop")
    # pwn_path=file.PwnInfo("./pwn/string/", "fmt")
    pwn_path = file.PwnInfo("./pwn/integer/", "int")
    clist = pwn_path.get_clist()
    blist = pwn_path.get_binarylist()
    print("Start: ")
    success = 0
    for i in range(len(clist)):
        decfile = llmgraph.get_decompilefile(clist[i])[0]
        # limit 128k token
        if len(decfile.page_content.split()) > 128000:
            resultcode="Invalid_request_error: Input is too big."
            print("Input words are more than 128k.")
        else:
            c_infohead = "\nHere is the decompiled C file:\n"
            messages = [
                ('user', "the binary file addresss of the challenge is '"+blist[i]+"'.")]
            resultcode = llmgraph.run_graph(
                c_infohead+decfile.page_content, messages)
            if resultcode['error'] == 'no':
                success += 1
        # save
        with open(pwn_path.list[i]+'/result_2_try_2.txt', 'w') as f:
            pprint(resultcode, stream=f)
            if 'generation' in resultcode:
                f.write(resultcode["generation"].imports + "\n" + resultcode["generation"].code)
    print("result: ", str(success)+'/'+str(len(clist)))


if __name__ == "__main__":
    # 事实证明通义不会用FmtStr
    pwn_path = file.PwnInfo("./pwn/string/", "fmt")
    clist = pwn_path.get_clist()
    blist = pwn_path.get_binarylist()
    print("Start: ")

    i = 0

    decfile = llmgraph.get_decompilefile(clist[i])[0]
    c_infohead = "\nHere is the decompiled C file:\n"
    messages = [('user', "The challenge is a format string vulnerabilit, you can use FmtStr() to get offset, and fmtstr_payload() to create payload. The binary file addresss of the challenge is '"+blist[i]+"'.")]
    resultcode = llmgraph.run_graph(c_infohead+decfile.page_content, messages)

    # save
    with open(pwn_path.list[i]+'/result_2_try_2_withinfo.txt', 'w') as f:
        pprint(resultcode, stream=f)

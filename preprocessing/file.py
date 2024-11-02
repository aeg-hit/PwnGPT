import sys
import os
import subprocess


class PwnInfo:
    path: str
    filename: str
    c_name = "de.c"
    asm_name = "de.asm"

    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename
        if not os.path.exists(path):
            raise Exception(
            "Please provide a existed path.")
        self.list=self.get_pwnlist(path,filename)

    def get_pwnlist(self, path: str, filename: str):
        """
        Attributes:
        path: "./pwn/string/"
        str: "fmt"
        """
        i = 1
        result = []
        while os.path.exists(path+filename+"-"+str(i)):
            result.append(path+filename+"-"+str(i))
            i += 1
        return result
    
    def get_clist(self):
        return [x+"/"+self.filename+x[-1]+self.c_name for x in self.list]
    
    def get_binarylist(self):
        return [x+"/"+self.filename+x[-1] for x in self.list]


def get_filepath():
    if len(sys.argv) < 2:
        raise Exception(
            "Please provide a file to decompile, as `llm4ctf [your_file]`")
    return sys.argv[1]


def retdec():

    input_file = get_filepath()
    output_file = input_file + ".c"

    if not os.path.exists(output_file):
        command = ["retdec-decompiler", input_file]
        print("decompiling with retdec-decompile")
        subprocess.run(command)
    else:
        print(f" File {output_file} already exists, thank god. \n skipping \"retdec-decompile\", lets continue")

    return input_file, output_file

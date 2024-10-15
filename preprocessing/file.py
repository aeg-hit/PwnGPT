import sys
import os
import subprocess
from rich.console import Console

def get_filepath():
    if len(sys.argv) < 2:
        raise Exception("Please provide a file to decompile, as `llm4ctf [your_file]`")
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
import re

# Function to read the content of a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Regular expression pattern for matching function definitions
# This will capture the return type, function name, and parameters
FUNC_PATTERN = r"^(\w[\w\s\*\(\),_]+)\s+(\w+)\s*\(.*\)\s*\{"


# Function to find and extract all functions in the code
def find_functions(code):
    functions = {}
    # Match all function definitions in the code using the regex pattern
    matches = re.finditer(FUNC_PATTERN, code, re.MULTILINE)
    
    for match in matches:
        ret_type, func_name = match.groups()
        start_idx = match.start()  # Start index of the function
        # Now, we need to find the end of the function by matching braces
        brace_depth = 0
        end_idx = start_idx
        
        # Start scanning for the closing brace from the function start
        for idx in range(start_idx, len(code)):
            char = code[idx]
            
            if char == '{':
                brace_depth += 1  # Opening brace found
            elif char == '}':
                brace_depth -= 1  # Closing brace found
                
                # If we've closed all opened braces, we've reached the end of the function
                if brace_depth == 0:
                    end_idx = idx + 1  # Include the closing brace
                    break
        
        # Extract the code of the function
        func_code = code[start_idx:end_idx]
        
        # Capture the comment lines just above the function
        comment_lines = ""
        commend_max=100
        comment_lines=code[start_idx-commend_max:start_idx].splitlines()[-1]

        
        # Store the function's details: code and comments
        functions[func_name] = {
            'start': start_idx,
            'end': end_idx,
            'code': func_code,
            'comment': comment_lines.strip()  # Remove trailing whitespace
        }
    
    return functions

# Regular expression pattern to find function calls within a function body
CALL_PATTERN = r"(\w+)\s*\("

# Function to find all function calls within the code of a given function
def find_calls(func_code):
    # Use regex to find all function calls by matching function names followed by parentheses
    calls = re.findall(CALL_PATTERN, func_code)
    return calls

# Function to extract 'main' function and the functions it calls (up to 2 layers)
def extract_main_and_calls(functions):
    # Start by extracting the 'main' function
    to_extract = ['main']
    
    # If 'main' exists, find all functions called within it
    main_code = functions.get('main', None)
    if main_code:
        calls = find_calls(main_code['code'])  # Find calls in the 'main' function
        to_extract.extend(calls)  # Add all the called functions to the extraction list
    
    # Extract the functions and the functions they call (up to two layers)
    result = {}
    for func_name in to_extract:
        func = functions.get(func_name)
        if func:
            # Store the function's comment (for location) and code
            result[func_name] = func['comment'] + "\n" + func['code']
            
            # Find the calls inside this function and extract them
            calls_in_func = find_calls(func['code'])
            for called_func in calls_in_func:
                called_func_code = functions.get(called_func)
                if called_func_code:
                    # Store the called function's comment and code
                    result[called_func] = called_func_code['comment'] + "\n" + called_func_code['code']
    
    return result

# Function to save the extracted functions into a new file
def save_extracted_functions(extracted_funcs, output_path):
    with open(output_path, 'w') as out_file:
        for func_name, func_code in extracted_funcs.items():
            # Write a comment indicating the function's name
            out_file.write(func_code)  # Write the code of the function
            out_file.write("\n\n")

# Main function to orchestrate the extraction process
def main(input_file, output_file):
    # Read the entire content of the input file
    code = read_file(input_file)
    
    # Find all functions in the code
    functions = find_functions(code)
    for func_name, func_code in functions.items():
        print(func_name)
    # Extract 'main' and all related functions (up to 2 layers deep)
    extracted_funcs = extract_main_and_calls(functions)
    
    # Save the extracted functions and their code to the output file
    save_extracted_functions(extracted_funcs, output_file)



# Run the main function to execute the extraction process
if __name__ == "__main__":
    # Set the paths for input and output files
    input_file = './pwn/stack/rop-9/rop9de.c'  # Replace with your input file path
    output_file = 'extracted_functions.c'  # Output file with extracted functions
    main(input_file, output_file)

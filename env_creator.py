import os
import re
import secrets

def required_input(prompt):
    user_input = input(prompt)
    while not user_input.strip():
        print("You must enter something.")
        user_input = input(prompt)
    return user_input

def generate_secret_token_hex(length):
    return secrets.token_hex(length)

def handle_comment(comment):
    print(comment)
    
def complex_variable_solver(key, index, temp_values, value, ):
    output_text=""
    new_value=""
    if value.startswith('rep:'):
        rep_count = int(value[4:])
        new_values = []
        text = ""
        for i in range(rep_count):
            [new_value, text] = complex_variable_solver(key, index, temp_values[index + 1::], temp_values[index + 1])
            new_values.append(new_value)
        new_value = ", ".join(new_values)
        output_text += f"{rep_count} times {text} "
        
    elif value.startswith('empty:'):
        prompt = value[6:]
        user_input = input(f"{key} (enter {prompt} or left empty): ")
        if user_input.strip():
            new_value=user_input
            output_text += f"entered "
        else:
            output_text += f"left empty "
        
    elif value.startswith('or:'):
        prompt = value[3:]
        user_input = input(f"{prompt}: ")
        new_value=user_input
        output_text += f"entered "
        
    elif value == 'generate':
        generated_value = generate_secret_token_hex(32)
        new_value=generated_value
        output_text += f"generated "
        
    elif value.startswith('if:'):
        question = value[3:]
        response = input(f"{question} (Y/N): ")
        if response.lower() == 'y':
            user_input = complex_variable_solver(key, index, temp_values[index + 1::], temp_values[index + 1])
            new_value=user_input[0]
            output_text += f"filled "+ user_input[1]
        else:
            output_text += f"skipped "
            
    elif value.startswith('req:'):
        value_prompt = value[4:]
        user_input = required_input(f"{key} ({value_prompt}): ")
        new_value=user_input
        
    elif value.startswith('none:'):
        user_input = input(f"{key} (if empty will be generated): ")
        if user_input.strip():
            new_value=user_input
        else:
            generated_value = complex_variable_solver(key, index, temp_values[index + 1::], value[5:])
            new_value=generated_value[0]
            output_text += f"filled "+ generated_value[1]
            
    else:
        new_value=temp_values[index]
        output_text += f"set to {new_value} "
    return new_value, output_text
    
def hande_complex_variable(key, value):
    temp_values = [val.strip() for val in value[1:].split(',')]
    new_values = []
    output_text = ""

    temp_value=temp_values[0]
    [new_values, output_text] = complex_variable_solver(key, 0, temp_values, temp_value)
    if isinstance(new_values, list):
        new_values = [str(val) for val in new_values]
        return ', '.join(new_values), f"{key}: has been {output_text}"
    return new_values, f"{key}: has been {output_text}"
    

def handle_variable(key, value):
    if value.startswith('#'):
        return hande_complex_variable(key, value)
    else:
        default_value = value
        if not value or value == "":
            user_input = input(f"{key} (enter value or left empty): ")
        else:
            user_input = input(f"{key} (default: {default_value}): ")
        new_value = user_input if user_input.strip() else default_value
        return new_value, f"{key} (default: {default_value}): {user_input or 'unchanged'}"

def create_dotEnv(env_example_data):
    env_data = {}

    for entry in env_example_data:
        entry_type = entry['type']
        entry_data = entry['data']

        if entry_type == 'comment':
            handle_comment(entry_data)
        elif entry_type == 'variable':
            key, value = list(entry_data.items())[0]
            new_value, log = handle_variable(key, value)
            env_data[key] = new_value
            print(log)

    return env_data

def read_env_example(filename):
    env_data = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('#'):
                env_data.append({'type': 'comment', 'data': line[1:].strip()})
            else:
                key, value = line.split('=', 1)
                env_data.append({'type': 'variable', 'data': {key.strip(): value.strip()}})

    return env_data

def save_data_to_file(data, file):
    with open(file, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}={value}\n")
def display_data(data):
    print("\n---- Data ----")
    for key, value in data.items():
        print(f"{key}={value}")
    print("--------------")

if __name__ == "__main__":
    example_file = ".env.example"
    env_example_data = read_env_example(example_file)

    env_data = create_dotEnv(env_example_data)
    
    if required_input("\n\nDisplay data? (Y/N): ").lower() == 'y':
        display_data(env_data)
        
    if required_input("\n\nSave data? (Y/N): ").lower() == 'y':
        file_name = required_input("Enter file name: ")
        save_data_to_file(env_data, file_name)
    
    

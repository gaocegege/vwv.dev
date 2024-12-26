import json
from openai import OpenAI
import os
import re
import sys
from flask import Flask, request, jsonify


api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def get_response_from_chat(messages):
    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=messages,
        max_tokens=1024,
        temperature=0.0,
        stream=False,
        response_format={
            'type': 'json_object'
        }
    )
    return response

def create_files_from_response(response_content):
    """
    Creates files from the given JSON response content. If a file with the same name already exists,
    it renames the existing file by appending a version number before creating the new file.

    Args:
        response_content (str): A JSON string containing a dictionary where keys are filenames and values are file contents.

    Example:
        response_content = '{"file1.txt": "Hello, World!", "file2.txt": "Python is awesome!"}'
        create_files_from_response(response_content)
        # This will create 'file1.txt' with content "Hello, World!" and 'file2.txt' with content "Python is awesome!".
        # If 'file1.txt' already exists, it will be renamed to 'file1.txt.v1', 'file1.txt.v2', etc., before creating the new 'file1.txt'.
    """
    files = json.loads(response_content)
    for filename, content in files.items():
        if os.path.exists(filename):
            version = 1
            new_filename = f"{filename}.v{version}"
            while os.path.exists(new_filename):
                version += 1
                new_filename = f"{filename}.v{version}"
            os.rename(filename, new_filename)
        with open(filename, 'w') as file:
            file.write(content)

messages = [
    {"role": "system", "content": """As a helpful assistant, you will write clean, well-organized, and easy-to-understand front-end code. The code should be written in json format. The key is the filename and the value is the content of the file."""},
]

while True:
    # Read user input from stdin
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        break
    if user_input:
        messages.append({"role": "user", "content": user_input})

    response = get_response_from_chat(messages)
    assistant_message = response.choices[0].message.content
    print("Assistant:", json.loads(assistant_message))

    messages.append({"role": "assistant", "content": assistant_message})

    create_files_from_response(assistant_message)

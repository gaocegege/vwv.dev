import json
import os
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from flask import Flask, request, jsonify
from openai import OpenAI
import uuid

# Define request and response models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    path: str
    response: List[Message]

# Load API key from environment variable
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def get_response_from_chat(messages: List[Message]):
    """
    Get response from the chat model.

    Args:
        messages (list): List of messages in the conversation.

    Returns:
        response: Response from the chat model.
    """
    system_message = {
        "role": "system",
        "content": """As a helpful assistant, you will write clean, well-organized, and easy-to-understand front-end code. The code should be written in json format. The key is the filename and the value is the content of the file."""
    }
    if not any(message.role == 'system' for message in messages):
        messages.insert(0, system_message)
    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=[message.dict() for message in messages],
        max_tokens=1024,
        temperature=0.0,
        stream=False,
        response_format={'type': 'json_object'}
    )
    return response


def create_files_from_response(response_content, directory):
    """
    Creates files from the given JSON response content in a new subdirectory with a random name within the specified directory.
    If a file with the same name already exists, it renames the existing file by appending a version number before creating the new file.

    Args:
        response_content (str): A JSON string containing a dictionary where keys are filenames and values are file contents.
        directory (str): The directory where the new subdirectory should be created.

    Returns:
        str: The path of the newly created subdirectory.

    Example:
        response_content = '{"file1.txt": "Hello, World!", "file2.txt": "Python is awesome!"}'
        create_files_from_response(response_content, "/path/to/directory")
        # This will create a new subdirectory with a random name in the specified directory,
        # and create 'file1.txt' with content "Hello, World!" and 'file2.txt' with content "Python is awesome!" in the new subdirectory.
        # If 'file1.txt' already exists, it will be renamed to 'file1.txt.v1', 'file1.txt.v2', etc., before creating the new 'file1.txt'.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    subdir = str(uuid.uuid4())
    subdir_path = os.path.join(directory, subdir)
    os.makedirs(subdir_path)

    files = json.loads(response_content)
    for filename, content in files.items():
        file_path = os.path.join(subdir_path, filename)
        if os.path.exists(file_path):
            version = 1
            new_filename = f"{filename}.v{version}"
            new_file_path = os.path.join(subdir_path, new_filename)
            while os.path.exists(new_file_path):
                version += 1
                new_filename = f"{filename}.v{version}"
                new_file_path = os.path.join(subdir_path, new_filename)
            os.rename(file_path, new_file_path)
        with open(file_path, 'w') as file:
            file.write(content)

    return subdir_path

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/examples", StaticFiles(directory="examples"), name="examples")

@app.get("/")
def read_root():
    """
    Serve the index.html file.
    """
    return FileResponse("static/index.html")

@app.get("/examples/{subdir:path}")
def read_example_subdir(subdir: str):
    """
    Serve the index.html file from any subdirectory within the examples directory.

    Args:
        subdir (str): The subdirectory path within the examples directory.

    Returns:
        FileResponse: The index.html file from the specified subdirectory.
    """
    subdir_path = os.path.join("examples", subdir)
    index_file_path = os.path.join(subdir_path, "index.html")
    if not os.path.exists(index_file_path):
        raise HTTPException(status_code=404, detail="Index file not found")
    return FileResponse(index_file_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(chat_request: ChatRequest):
    """
    Endpoint for chat.

    Args:
        chat_request (ChatRequest): The chat request containing the messages.

    Returns:
        ChatResponse: The response from the assistant.
    """
    messages = chat_request.messages
    logger.info("Received chat request with messages: %s", messages)

    response = get_response_from_chat(messages)
    assistant_message = response.choices[0].message.content
    logger.info("Received response from assistant: %s", assistant_message)

    try:
        response_content = json.loads(assistant_message)
    except json.JSONDecodeError:
        logger.error("Invalid response format from assistant: %s", assistant_message)
        raise HTTPException(status_code=500, detail="Invalid response format from assistant")

    subdir_path = create_files_from_response(assistant_message, "examples")
    logger.info("Created files from response in 'examples' directory")

    # Append the assistant's message to the conversation history
    messages.append(Message(role="assistant", content=assistant_message))

    logger.info("Returning final response: %s", response_content)
    return ChatResponse(path=subdir_path, response=messages)

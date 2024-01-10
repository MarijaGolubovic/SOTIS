# SOTIS - Robot Playground

## Application Setup Guide

### First-time Setup

1. Navigate to the container by executing the following command:
    ```bash
    make build start exec
    ```
   This is only necessary the first time.

2. Once the container is running, download the LLama model using the following link:
   [LLama model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q8_0.gguf)

3. Copy the downloaded LLama model to the `assets` directory.

### Subsequent Runs

Every time you want to start the application after the initial setup, execute the following command:
```bash
make exec

Running the Application

After downloading and copying the LLama model into the assets directory, run the application in the Docker container with the following command:

python3 src/spesbot/assets/gui.py


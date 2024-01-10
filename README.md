# SOTIS - Robot Playground
This repo represent part of platform for robot control. You need to have this platform if you want to run all system. For running only this part you need follow this guide.

## Application Setup Guide

### First-time Setup

1. Install all dependecies:
    ```bash
    pip3 install llama-cpp-python tk Jinja2
    ```
   This is only necessary the first time.

2. Download the LLama model using the following link:
   [LLama model](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q8_0.gguf)
   Other model sizes you can finds on following [link](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/tree/main). For newest version visit Hugging [Face site](https://huggingface.co/models).

4. Copy the downloaded LLama model to the `assets` directory.

Running the Application

After downloading and copying the LLama model into the assets directory, run the application with the following command inside assets directory:
```
python3 gui.py
```

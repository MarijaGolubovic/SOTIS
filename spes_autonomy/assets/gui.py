# gui.py
import threading
import tkinter as tk
from subprocess import Popen
from tkinter import ttk
import webbrowser
from llama_cpp import Llama
from tkinter import scrolledtext
import time 
import subprocess
import tokens.build_tree

def generate_tokens(user_input):
    model_path = "/spesbot/ros2_ws/src/spesbot/assets/llama-2-7b-chat.Q8_0.gguf"
    model = Llama(model_path=model_path)

    start_time = time.time()

    print("Generating answare...")
    system_message = "You are a helpful assistant"
    user_message = f"You have tokens X, TRANSLATE and ROTATE, REGULATE, REPEAT. TRANSLATE and ROTATE are name of action and they have not value. TRANSLATE move robot forward. \
      X is distanece for TRANSLATE or angle for ROTATE.  Give me answare without explanation. \
      This is example of question and answare: \
      Question:  I want to move my robot 10 cm and rotate for 100 degress. Repeat last action 4 times. Translate the robot 10 times by 10 cm. Translate the robot by 15 cm otherwise rotate robot by 90 degrees.\
      ### Ansaware: TRANSLATE, X:10; ROTATE, X:100; REPEAT:4; TRANSLATE, X:10; REPEAT:10; TRANSLATE, X:15; FALLBACK; ROTATE, X:90; \
      You have question, add me answare \
      Question: \
        Which tokens from list i must used and what they are value, if {user_input}\
     "
    prompt = f"""<s>[INST] <<SYS>>
    {system_message}
    <</SYS>>
    {user_message} [/INST]"""

    # Model parameters
    max_tokens = 1250

    # Run the model
    output = model(prompt, max_tokens=max_tokens, echo=True)

    end_time = time.time()
    print("*****************************************Model output****************************************")
    print(output)
    print("*********************************************************************************************")
    print("Time of executiong is: ", round((end_time - start_time),1), 's')
    return output


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot playground")
        self.root.geometry("800x600")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Code Generator")

        self.init_code_generator_tab()

        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Lessons")

        self.init_lessons_tab()

    
    def init_code_generator_tab(self):
        code_input_section = tk.LabelFrame(self.tab1, text="Request")
        code_input_section.pack(padx=10, pady=10, fill="both", expand="yes")

        self.entry_text = tk.Text(code_input_section, wrap=tk.WORD, width=50, height=5)
        self.entry_text.pack(pady=10)

        show_input_button = tk.Button(code_input_section, text="Start", command=self.show_input_content)
        show_input_button.pack(pady=10)
        
        button_webots = tk.Button(code_input_section, text="Start Webots", command=self.open_ros2_launch)
        button_webots.pack(padx=10)
        
        result_section = tk.LabelFrame(self.tab1, text="Response")
        result_section.pack(padx=10, pady=10, fill="both", expand="yes")

        
    
        self.result_text = scrolledtext.ScrolledText(result_section, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack(pady=10)
        
    def init_lessons_tab(self):
        lessons_section = tk.LabelFrame(self.tab2, text="Lessons")
        lessons_section.pack(padx=10, pady=10, fill="both", expand="yes")

        lesson1_text = (
            "Welcome to RobotPlayground! Check out tutorials for our platform on the following link."
        )
        lesson1_label = tk.Label(lessons_section, text=lesson1_text, wraplength=600)
        lesson1_label.pack(pady=10)

        button_lesson1 = tk.Button(lessons_section, text="Show Tutorial", command=self.open_lesson1,  width=15, height=3)
        button_lesson1.pack(side=tk.TOP, padx=10, pady=10)
    
    def open_lesson1(self):
        http_server_thread = threading.Thread(target=self.run_http_server)
        http_server_thread.start()
        lesson1_path = "http://localhost:8000/index.html"
        webbrowser.open_new_tab(lesson1_path)

    def run_http_server(self):
        try:
            http_server_process = subprocess.Popen(["python3", "-m", "http.server"], cwd="/spesbot/ros2_ws/src/spesbot/assets")
            http_server_process.wait()
        except Exception as e:
            print(f"Greška prilikom pokretanja HTTP servera: {str(e)}")

    def show_input_content(self):
        user_input = self.entry_text.get("1.0", tk.END).strip()
        self.result_text.delete("1.0", tk.END)

        self.result_text.insert(tk.END, f"Your input: {user_input}\n")
        self.result_text.insert(tk.END, f"\n\n\t\t\tGenerating code...\n")
        self.root.after(1000, self.generate_and_show_output, user_input)

    def generate_and_show_output(self, user_input):
        output = generate_tokens(user_input)
        self.result_text.insert(tk.END, f"\nAnsware: \n")
        
        answare_content = extract_answare(output)
        words = [word.strip() for word in answare_content.split(';')]

        with open('/spesbot/ros2_ws/src/spesbot/assets/action_params.txt', 'w') as file:
            file.write('\n'.join(words))
        
        file_content = tokens.build_tree.read_file_content()
        self.result_text.delete("1.0", tk.END)
        for line in file_content:
            self.result_text.insert(tk.END, f"{line}")
            self.root.update_idletasks() 
            self.root.after(200)
        
    def open_ros2_launch(self):
        tokens.build_tree.build_tree()

        try:
            process = subprocess.Popen(["ros2", "launch", "spesbot_webots", "webots_launch.py", "behavior:=USER_TREE"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print("Command is sucessfully executed.")
                print(stdout.decode())
            else:
                print(f"Error with simulator start: {stderr.decode()}")
        except Exception as e:
            print(f"Greška: {str(e)}")


def extract_answare(output):
    answare_text = output['choices'][0].get('text', '').strip()
    if 'Answare:' in answare_text:
        answare_content = answare_text.split('Answare:')[1].strip()
        return answare_content
    else:
        return "Answare not found."


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()

# I want that my robot go 50 cm forward. Repeat last action 2 times. After that rotate for 150 degrees and move 10 cm. Rotate the robot 10 times by 10 degrees.
# I want that my robot go 50 cm forward. Repeat last action 2 times. After that rotate for 150 degrees and move 10 cm. Rotate the robot  by 10 degrees and repeat this action 10 times.
# I want that my robot go 50 cm forward. Repeat last action 2 times. After that rotate for 150 degrees and move 10 cm, otherwise rotate the robot by 120 degrees. Rotate the robot  by 10 degrees and repeat this action 10 times. 
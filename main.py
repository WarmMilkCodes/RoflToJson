import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import json
import os

def extract_json_from_rofl(file_name):
    with open(file_name, 'rb') as file:
        content = file.read()
        brace_stack = []
        start_idx = None
        end_idx = None

        for idx, byte in enumerate(content):
            if byte == ord('{'):
                brace_stack.append(idx)
                if start_idx is None:
                    start_idx = idx
            elif byte == ord('}'):
                if brace_stack:
                    brace_stack.pop()
                    if not brace_stack:
                        end_idx = idx
                        break

        if start_idx is not None and end_idx is not None:
            json_bytes = content[start_idx:end_idx + 1]
            try:
                json_str = json_bytes.decode('utf-8', 'ignore')
                json_object = json.loads(json_str)
                return json_object
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        return None

def extract_stats_json_from_rofl(file_name):
    full_json = extract_json_from_rofl(file_name)
    if full_json and 'statsJson' in full_json:
        return full_json['statsJson']
    else:
        return None

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("ROFL files", "*.rofl"), ("All files", "*.*")])
    if file_path:
        json_data = extract_stats_json_from_rofl(file_path)
        if json_data:
            formatted_json = json.dumps(json_data, indent=4)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, formatted_json)
        else:
            messagebox.showerror("Error", "The file could not be processed.")

def save_json(data):
    file_path = filedialog.asksaveasfilename(
        defaultextension='.json',
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"File saved successfully at {file_path}")

def handle_save():
    current_text = text_widget.get("1.0", tk.END)
    try:
        data = json.loads(current_text)
        save_json(data)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "The current text is not valid JSON.")

root = tk.Tk()
root.title("RoflToJson")
root.geometry("800x600")

root.iconbitmap('rofltojson.ico')

style = ttk.Style()
style.theme_use("clam")

large_font = ("Verdna", 12)
small_font = ("Verdana", 10)

padding = (5,5)

button_frame = ttk.Frame(root, padding=padding)
button_frame.pack(side=tk.TOP, fill=tk.X)

text_frame = ttk.Frame(root, padding=padding)
text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

open_button = ttk.Button(button_frame, text="Open ROFL File", command=open_file)
open_button.pack(side=tk.LEFT, padx=10, pady=10)

save_button = ttk.Button(button_frame, text="Save JSON", command=handle_save)
save_button.pack(side=tk.RIGHT, padx=10, pady=10)

text_widget = tk.Text(text_frame, font=large_font, wrap=tk.WORD)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget['yscrollcommand'] = scrollbar.set

root.configure(background='#f0f0f0')
text_widget.configure(bg='#ffffff', fg='#333333')

footer_frame = ttk.Frame(root)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

footer_label = ttk.Label(footer_frame, text="2023 WarmMilkCodes - v1.0.0", background="#ddd", anchor="center")
footer_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
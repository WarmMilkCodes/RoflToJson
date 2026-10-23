import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import json
import os
import struct

ROFL_SIGNATURE = b'RIOT\x00\x00'   # replays before patch 14.9
ROFL2_SIGNATURE = b'RIOT\x02\x00'  # replays from patch 14.11 onward


def read_rofl_metadata(file_name):
    with open(file_name, 'rb') as file:
        signature = file.read(6)

        if signature == ROFL2_SIGNATURE:
            # Metadata JSON sits at the end of the file; the last 4 bytes hold its length.
            file.seek(15)
            game_version = file.read(14).decode('utf-8', 'ignore').strip('\x00 ')
            file.seek(-4, os.SEEK_END)
            metadata_length = struct.unpack('<I', file.read(4))[0]
            file.seek(-(metadata_length + 4), os.SEEK_END)
            metadata = json.loads(file.read(metadata_length).decode('utf-8'))
            metadata['gameVersion'] = game_version
        elif signature == ROFL_SIGNATURE:
            # Metadata offset and length are in the header, after the 256-byte signature.
            file.seek(262 + 6)
            metadata_offset, metadata_length = struct.unpack('<II', file.read(8))
            file.seek(metadata_offset)
            metadata = json.loads(file.read(metadata_length).decode('utf-8'))
        else:
            raise ValueError("Not a League of Legends replay file.")

    return metadata


def extract_json_from_rofl(file_name, keys):
    metadata = read_rofl_metadata(file_name)
    players = json.loads(metadata.get('statsJson') or '[]')
    if not players:
        raise ValueError("The replay contains no player stats (the game may not have finished).")

    return {
        'gameVersion': metadata.get('gameVersion'),
        'gameLength': metadata.get('gameLength'),
        'players': [{key: player[key] for key in keys if key in player} for player in players],
    }


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("ROFL files", "*.rofl"), ("All files", "*.*")])
    if file_path:
        try:
            json_data = extract_json_from_rofl(file_path, keys)
        except (OSError, ValueError, struct.error) as e:
            messagebox.showerror("Error", f"The file could not be processed.\n\n{e}")
            return
        formatted_json = json.dumps(json_data, indent=4)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, formatted_json)

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

keys = ['NAME', 'ASSISTS', 'BARON_KILLS', 'DOUBLE_KILLS', 'DRAGON_KILLS', 'HORDE_KILLS', 'PENTA_KILLS', 'QUADRA_KILLS', 'RIFT_HERALD_KILLS', 'TRIPLE_KILLS', 'UNREAL_KILLS', 'WIN']        

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

footer_label = ttk.Label(footer_frame, text="contact@warmmilk.dev - v1.2.0", background="#ddd", anchor="center")
footer_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
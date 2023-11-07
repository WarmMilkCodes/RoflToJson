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

# Replace 'replay.rofl' with the actual name of your replay file.
replay_file_name = 'replay.rofl'
stats_json = extract_stats_json_from_rofl(replay_file_name)

if stats_json:
    print(json.dumps(stats_json, indent=4))
else:
    print("No stats JSON object found in the file.")

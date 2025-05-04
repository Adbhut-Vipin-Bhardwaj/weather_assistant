import json

filename = "./rowboat_export.json"
prompt_file_path = "./openai_agents_sdk/weather_agent_prompt.py"

with open(filename, "r") as f:
    data = json.load(f)

weather_agent = data["agents"][0]
name = weather_agent["name"]
instructions = weather_agent["instructions"]
examples = weather_agent["examples"]

prompt_file_contents = f"""name = "{name}"

instructions = \"\"\"{instructions}\"\"\"

examples = \"\"\"{examples}\"\"\"
"""

with open(prompt_file_path, "w") as f:
    f.write(prompt_file_contents)

print(f"Prompt file created at {prompt_file_path}")

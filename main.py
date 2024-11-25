import subprocess
from pprint import pprint
import json

user_list = subprocess.check_output(["knife", "data", "bag", "show", "local_users"], encoding="utf-8").split("\n")

user_dict = {}

for i in user_list[0:5]:
    try:
        # Execute the command and capture the output
        result = subprocess.run(["knife", "data", "bag", "show", "local_users", i, "-F", "json"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Parse the JSON output
        json_output = json.loads(result.stdout)

        if "disable" not in json_output.keys():
            pprint(json_output)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e.stderr}")
import subprocess
from pprint import pprint
import json
from dotenv import load_dotenv
import os
import hvac

## LOAD ENVIRONMENT VARIABLES
load_dotenv()

ROLE_ID = os.getenv("ROLE_ID")
SECRET_ID = os.getenv("SECRET_ID")
MOUNT_POINT = os.getenv("MOUNT_POINT")
VAULT_PATH = os.getenv("VAULT_PATH")
VAULT_URL = os.getenv("VAULT_URL")
#METHOD_TYPE = os.getenv("METHOD_TYPE")
USER_TOKEN = os.getenv("USER_TOKEN")

print(SECRET_ID)

## SIGN IN WITH APPROLE
client = hvac.Client(url=VAULT_URL)
# client.sys.enable_auth_method(
#     method_type=METHOD_TYPE,
#     path="latis/login",
# )

# auth_response = client.auth.approle.login(
#     role_id=ROLE_ID,
#     secret_id=SECRET_ID
# )

client.token = USER_TOKEN

# Check if authentication is successful
if client.is_authenticated():
    print("Authentication successful!")
else:
    raise Exception("Authentication failed.")

## GET THE CHEF USER LIST
#user_list = subprocess.check_output(["knife", "data", "bag", "show", "local_users"], encoding="utf-8").split("\n")

#for i in user_list[0:10]:
for i in ["class_tasks"]:
    try:
        # Execute the command and capture the output
        result = subprocess.run(["knife", "data", "bag", "show", "local_users", i, "-F", "json"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #import pdb; pdb.set_trace()
        
        # Parse the JSON output
        json_output = json.loads(result.stdout)

        if "disable" not in json_output.keys():
            pprint(json_output)
            try:
                response = client.secrets.kv.v2.create_or_update_secret(
                    path=f"{VAULT_PATH}/{json_output['id']}",
                    secret=json_output,
                    mount_point=MOUNT_POINT
                )
                print(response)
                print(f"Secret written successfully to {MOUNT_POINT}/{VAULT_PATH}/{json_output['id']}")
            except hvac.exceptions.InvalidPath as e:
                print(f"Invalid path error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"{json_output['id']} is disabled.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e.stderr}")
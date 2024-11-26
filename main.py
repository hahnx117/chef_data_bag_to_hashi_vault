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
USER_TOKEN = os.getenv("USER_TOKEN")
DATA_BAG = "local_admins"
#METHOD_TYPE="approle"

admin_list = ["hahnx117", "kalle001", "olsont", "dolsen", "cbs"]

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

## GET THE CHEF DATA BAG ITEMS
data_bag_items = subprocess.check_output(["knife", "data", "bag", "show", DATA_BAG], encoding="utf-8").split("\n")

for i in data_bag_items:
#for i in ["local_hahnx117"]:
    try:
        # Execute the command and capture the output
        result = subprocess.run(["knife", "data", "bag", "show", DATA_BAG, i, "-F", "json"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Parse the JSON output
        json_output = json.loads(result.stdout)

        if "disable" not in json_output.keys() and json_output['id'] not in admin_list:
            pprint(json_output)
            endpont = json_output.pop('id')
            #import pdb; pdb.set_trace()
            try:
                response = client.secrets.kv.v2.create_or_update_secret(
                    path=f"{VAULT_PATH}/{DATA_BAG}/{endpont}",
                    secret=json_output,
                    mount_point=MOUNT_POINT
                )
                print(response)
                print(f"Secret written successfully to {MOUNT_POINT}/{VAULT_PATH}/{DATA_BAG}/{endpont}\n")
            except hvac.exceptions.InvalidPath as e:
                print(f"Invalid path error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            if json_output['id'] in admin_list:
                print(f"{json_output['id']} is already in there.")
            elif "disable" in json_output.keys():
                print(f"{json_output['id']} is disabled.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e.stderr}")
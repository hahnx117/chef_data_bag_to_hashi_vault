# Python Script for local_users into HashiCorp Vault

## Requirements

This script requires a `.env` file with the following information:
+ `ROLE_ID`: Currently not used.
+ `SECRET_ID`: Currently not used.
+ `MOUNT_POINT`: The mount point of the secrets.
+ `VAULT_PATH`: The path _minus the endpoint_ for the secret. The endpoint will be designated in the script and becomes the name for the secret itself.
+ `VAULT_URL`: The URL:port for the Vault instance.
+ `USER_TOKEN`: Gotten from Vault.



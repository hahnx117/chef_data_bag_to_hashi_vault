# Python Script for local_users into HashiCorp Vault

## Getting local_users from data bag

```
$ knife data bag show local_users
admit9
bege0005
blindeen
...
```

```
$ knife data bag show local_users admit9
comment:    MBA admission scripts service account
disable:    true
...
```
> Note: the `disable: true` line means we don't want to bring them over to Vault.
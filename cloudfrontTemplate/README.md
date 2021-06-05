# Info
This deploy is made with Sceptre, which is a wrapper over Cloudfromation for better handling of the parameters.

More info about Sceptre here:
https://sceptre.cloudreach.com/2.5.0/docs/install.html

Sceptre uses the credentials fro ~/.aws/credentials file

# Deploy new env

There is one env name "dev" already created. To create new env, for example "prod":
- duplicate "config/dev/" folder to "config/prod"
- in the file config/prod/cloudfront.yaml replace all occurences of "dev" string to "prod" string. In order to create new bucket names for example.
- Run command: sceptre create prod

# Delete env
- First empty the buckets from the AWS Console (the delete will fail otherwise)
- Run command: sceptre delete prod
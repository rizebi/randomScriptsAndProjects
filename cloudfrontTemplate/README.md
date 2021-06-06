# Info
This deploy is made with Sceptre, which is a wrapper over Cloudfromation for better handling of the parameters.

More info about Sceptre here:
https://sceptre.cloudreach.com/2.5.0/docs/install.html

Sceptre uses the credentials fro ~/.aws/credentials file

# Deploy new env

There is one env name "dev" already created. To create new env, for example "prod":
- duplicate "config/dev/" folder to "config/prod"
- in the file config/prod/cloudfront.yaml replace all occurences of "dev" string to "prod" string. In order to create new bucket names for example.
- Run command: sceptre create <env_name_to_replace>
- IMPORTANT NOTE. After creating of a new env, sometimes, for few hours, the S3 origins will not work. It is something related with propagation of DNS internally in AWS.
    - How to see if this is the case?
    - When requesting an object stored in one of the buckets, if Cloudfront DO NOT serve the object, but instead redirects to the S3 bucket, there is the issue.
    - More info: http://blog.open-tribute.org/2017/05/30/cloudfront-and-s3-307-redirects/
# Delete env
- First empty the buckets from the AWS Console (the delete will fail otherwise)
- Run command: sceptre delete <env_name_to_replace>
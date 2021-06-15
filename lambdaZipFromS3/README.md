# How to deploy the lambda function

### Create package with the function and dependencies
- Got to current folder (the one with index.js in it)
- Run: npm install archiver
- Run: zip -r function.zip .


### Create policy for the function (where it has access)
Go to AWS Console -> IAM -> Policies -> Create Policy -> JSON -> And paste the following JSON. It basically says "Read permissions from enaia-lambdazip-source and write permissions to enaia-lambdazip-destination"

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListObjectsInSourceBucket",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::enaia-lambdazip-source"
            ]
        },
        {
            "Sid": "ReadObjectActionsSourceBucket",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": [
                "arn:aws:s3:::enaia-lambdazip-source/*"
            ]
        },
        {
            "Sid": "ListObjectsInDestinationBucket",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::enaia-lambdazip-destination"
            ]
        },
        {
            "Sid": "AllObjectActionsDestinationBucket",
            "Effect": "Allow",
            "Action": "s3:*Object",
            "Resource": [
                "arn:aws:s3:::enaia-lambdazip-destination/*"
            ]
        }
    ]
}

### Create role for the function
Go to AWS Console -> IAM -> Roles -> Create role -> Select Lambda -> Attach previously created policy

### Create the function
Go to AWS console -> Lambda -> Create function -> Author from scratch

- Enter function name
- Use NodeJS 14.x
- Change default execution role with the previously created one
- Upload from -> .zip file -> Select function.zip -> OK -> Deploy
- Go to Configuration -> General configuration -> Increase timeout to 15 minutes
- Go to Configuration -> General configuration -> Set memory to 2048MB (this will result in better CPU and faster converting)
- Save

# How to test the function
Go to AWS Console -> Lambda -> Select function -> Test -> Create test event

{
  "destination_bucket": "enaia-lambdazip-destination",
  "destination_key": "zips/test.zip",
  "source_bucket": "enaia-lambdazip-source",
  "files": [
    "path1/file1.docx",
    "file1.docx",
    "path2/file2.png",
    "file.xlsx"
  ]
}

Then click Test
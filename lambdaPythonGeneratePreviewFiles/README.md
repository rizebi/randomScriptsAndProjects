### How to create Docker image for this function
docker build -t lambda-generate-preview-image .

### How to test the image locally
##### Start container for above image, and mount a volume
docker run -p 9000:8080 -v /Users/eusebiu.rizescu/Data/Git/randomScriptsAndProjects/lambdaPythonGeneratePreviewFiles:/mnt/data lambda-generate-preview-image

##### Invoke function
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"src_bucket": "", "src_path": "/preview-function/big.xlsx", "dest_bucket": "", "dest_path": "/preview-function/output.jpg", "width": "500", "height": "1000", "format": "png", "ok_sns": "arn::blabla", "error_sns": "arn::blabla"}'

### How to create the Lambda Function
1) Upload previously created image to ECR (container registry for AWS)

2) Create lambda function, using this image

3) Ensure that lambda has permissions to Read on the source bucket and Read-Write on the destination bucket

4) Increase timeout to 5 minutes (default is 3 seconds which is too little)

### How to use the function

- Invoke function like this from command line:

aws lambda invoke --region us-west-2 --function-name lambda-generate-preview-image --cli-binary-format raw-in-base64-out --payload '{"src_bucket": "lambda-generate-preview-image-source", "src_path": "source_folder/Equity Sharing Calculators.xlsm", "dest_bucket": "lambda-generate-preview-image-destination", "dest_path": "destination_folder/eusebiu_excel.jpg", "width": "500", "height": "1000", "format": "jpg", "ok_sns": "arn:aws:sns:us-west-2:020275857710:lambda-generate-preview-image-ok-topic", "error_sns": "arn:aws:sns:us-west-2:020275857710:lambda-generate-preview-image-error-topic"}' invoke_function_response

- For test we can go to Lambda console, and launch an test event

- NOTE! That the src_path and dest_path MUST not have a forward slash. They should start without it.

### How to update the code

-  Update code

-  Build image

docker build -t lambda-generate-preview-image .
-  Push image to ECR

docker tag lambda-generate-preview-image:latest 020275857710.dkr.ecr.us-west-2.amazonaws.com/lambda-generate-preview-image:latest

docker push 020275857710.dkr.ecr.us-west-2.amazonaws.com/lambda-generate-preview-image:latest

-  Update the Lambda to use the new image

-  Delete older image from ECR as no needed
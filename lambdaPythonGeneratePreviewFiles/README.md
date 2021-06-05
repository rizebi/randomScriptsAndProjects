### How to create Docker image for this function
docker build -t lambda-generate-preview-image .

### How to test the image locally
#####Start container for above image, and mount a volume
docker run -p 9000:8080 -v /Users/eusebiu.rizescu/Data/Git/randomScriptsAndProjects/lambdaPythonGeneratePreviewFiles:/mnt/data lambda-generate-preview-image

#####Invoke function
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"src_bucket": "", "src_path": "/mnt/data/pig.jpg", "dest_bucket": "", "dest_path": "/mnt/data/output.jpg", "width": "500", "height": "1000", "format": "png"}'

### How to create the Lambda Function
1) Upload previously created image to ECR (container registry for AWS)

2) Create lambda function, using this image

3) Ensure that lambda has permissions to Read on the source bucket and Read-Write on the destination bucket

### How to use the function

Invoke function like this:

aws lambda invoke --region <function_region> --function-name <function_name> --payload '{"src_bucket": "source-bucket-name", "src_path": "/path/to/pig.jpg", "dest_bucket": "dest-bucket-name", "dest_path": "/path/to/pig-preview.jpg", "width": "500", "height": "1000", "format": "jpg"}' invoke_function_response
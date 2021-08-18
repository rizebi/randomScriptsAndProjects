# File Previewer for Enaia

This is a lambda function that can take a document in one of many different formats and return an image preview of the first page. It is primarily a wrapper around the Python [preview-generator](https://pypi.org/project/preview-generator/) library.

## Creating the Docker image for this function

```bash
docker build -t lambda-generate-preview-image .
```

## Testing the image locally

### Start the container for above image, and mount a volume

```bash
docker run -p 9000:8080 -v /Users/eusebiu.rizescu/Data/Git/randomScriptsAndProjects/lambdaPythonGeneratePreviewFiles:/mnt/data lambda-generate-preview-image
```

### Invoke function

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"src_bucket": "", "src_path": "/mnt/data/vanilla-cakes.pdf", "dest_bucket": "", "dest_path": "/mnt/data/output_#{width}_#{height}.jpg", "format": "png", "request_id": "d23df3d2sg3sf3ew", "ok_sns": "arn::blabla", "error_sns": "arn::blabla", "dimensions": [{"width": "1000", "height": "500"}, {"width": "500", "height": "250"}, {"width": "250", "height": "120"}]}'
```

### How to create the Lambda Function

1. Upload previously created image to ECR (container registry for AWS)
2. Create lambda function, using this image
3. Ensure that lambda has permissions to Read on the source bucket and Read-Write on the destination bucket ([here](https://console.aws.amazon.com/iamv2/home?#/policies))
4. Increase timeout to 5 minutes (default is 3 seconds which is too little)

### How to use the function

Invoke function like this from command line:

```bash
aws lambda invoke --region us-west-2 --function-name lambda-generate-preview-image --cli-binary-format raw-in-base64-out --payload '{"src_bucket": "lambda-generate-preview-image-source", "src_path": "source_folder/Equity Sharing Calculators.xlsm", "dest_bucket": "lambda-generate-preview-image-destination", "dest_path": "destination_folder/eusebiu_excel.jpg", "width": "500", "height": "1000", "format": "jpg", "ok_sns": "arn:aws:sns:us-west-2:020275857710:lambda-generate-preview-image-ok-topic", "error_sns": "arn:aws:sns:us-west-2:020275857710:lambda-generate-preview-image-error-topic"}' invoke_function_response
```

- To test, you can go to the Lambda console and launch a test event.

- **Note:** the src_path and dest_path **must not** have a forward slash. They should start without it.

### How to update the code

* Update code
* Build image
* Run: `docker build -t lambda-generate-preview-image .`
* Push image to ECR:

```bash
docker tag lambda-generate-preview-image:latest 020275857710.dkr.ecr.us-west-2.amazonaws.com/lambda-generate-preview-image:latest
docker push 020275857710.dkr.ecr.us-west-2.amazonaws.com/lambda-generate-preview-image:latest
```

* Update the Lambda to use the new image
* Delete any older images from ECR as they are no longer needed
### More info about this full solution:
https://docs.aws.amazon.com/solutions/latest/serverless-image-handler/welcome.html

It basically take one or more S3 buckets, containing images and create some infrasturcture.
In the end you can say: "Give me image from bucket X, path Y, with 200px witdh, 400px height, grayscaled, flipped", for example.

The file serverless-image-handler.template is made by AWS. It can be found here:
https://solutions-reference.s3.amazonaws.com/serverless-image-handler/latest/serverless-image-handler.template

### How to use

- First we need to get the endpoints. To do that go do Cloudfromation -> us-west-2 -> ServerlessImageHandler -> Outputs
- ApiEndpoint is the API that will serve the processed images. On this deployment it is: https://d2br0kusuxz39i.cloudfront.net
- DemoUrl is the endpoint to use to thest the capabilities of the solution. On this deployment it is: https://d16vsqj5emqv0f.cloudfront.net/index.html
- Go to DemoUrl, and there play with the image processing. 
- To get from code, take the processed JSON, encode it to Base64, and then request it from ApiEndpoint URL

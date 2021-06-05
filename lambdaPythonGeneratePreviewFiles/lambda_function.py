import boto3
import traceback
from shutil import copyfile
from PIL import Image, ImageOps
from preview_generator.manager import PreviewManager

def lambda_handler(event, context):

  ### Inputs
  print("Event: " + str(event))
  src_bucket = event["src_bucket"]
  src_path = event["src_path"]
  dest_bucket = event["dest_bucket"]
  dest_path = event["dest_path"]
  wanted_width = int(event["width"])
  wanted_height = int(event["height"])
  output_format = event["format"]
  ok_sns = event["ok_sns"]
  error_sns = event["error_sns"]

  try:
    ### Copy the file from S3:
    print("Copy file from source S3")
    if src_bucket != "":
      client = boto3.client('s3')
      source_file = "/tmp/" + src_path.split("/")[-1]
      client.download_file(src_bucket, src_path, source_file)
    else:
      # If the src_bucket == 0 we will not copy from S3, and use local path.
      # This is for local testing
      source_file = src_path
    print("Successfully copied file from source S3")

    ### Generate preview
    print("Generating preview")
    manager = PreviewManager("/tmp/cache", create_folder= True)
    preview_image = manager.get_jpeg_preview(source_file, width=wanted_width, height=wanted_height)
    print("Successfully generated preview")

    ### Make sure the image has the expected size and format
    print("Resize and change the format")
    # Open the preview image
    img = Image.open(preview_image)

    # Calculate the differences between actual sizes and wanted sizes
    delta_w = wanted_width - img.width
    delta_h = wanted_height - img.height

    # Then actual sizes is odd (not even), the we need to add one more pixel
    precision_pixel_w = wanted_width - img.width - int(delta_w/2) - int(delta_w-(delta_w/2))
    precision_pixel_h = wanted_height - img.height - int(delta_h/2) - int(delta_h-(delta_h/2))

    # Resize the image
    ltrb_border=(int(delta_w/2), int(delta_h/2), int(delta_w-(delta_w/2)) + precision_pixel_w, int(delta_h-(delta_h/2)) + precision_pixel_h)
    img_with_border = ImageOps.expand(img, border=ltrb_border, fill='white')
    output_file = "/tmp/output_preview." + output_format
    img_with_border.save(output_file)
    print("Successfully resized and formatted")

    ### Copy to S3
    print("Copy preview to destination bucket")
    if dest_bucket != "":
      client = boto3.client('s3')
      client.upload_file(output_file, dest_bucket, dest_path)
    else:
      # If the dest_bucket == 0 we will not copy from S3, but will copy on local path
      copyfile(output_file, dest_path)
    print("Successfully copied preview to destination bucket")

    ### Send ok message to ok SNS
    print("Sending OK to SNS")
    if src_bucket != "":
      # If the src_bucket is not empty, then the function is running locally for dev purposes, so no need to send SNS
      client = boto3.client('sns')
      response = client.publish(
          TopicArn=ok_sns,
          Message="Preview generated successfully for: " + src_bucket + src_path
      )
    print("Successfully send OK to SNS")
    return "OK"

  except Exception as e:
    print("Error: {}".format(e))
    tracebackError = traceback.format_exc()
    print(tracebackError)
    ### Send error message to error SNS
    print("Sending ERROR to SNS")
    if src_bucket != "":
      # If the src_bucket is not empty, then the function is running locally for dev purposes, so no need to send SNS
      client = boto3.client('sns')
      response = client.publish(
          TopicArn=error_sns,
          Message="Preview FAILED to generate for: " + src_bucket + src_path
      )
    print("Successfully send ERROR to SNS")
    return "ERROR"
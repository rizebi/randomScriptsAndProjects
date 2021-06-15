// Archive many files from a bucket, and post the ZIP in another bucket (or the same), in a provided path
// {
//     "destination_bucket": "destination-bucket-name",
//     "destination_key": "zips/test.zip",
//     "source_bucket": "source-bucket-name",
//     "files": [
//       "/path/to/file1.xml",
//       "/path/to/file2.xls"
//     ]
// }
// Saves the zip file at "$destination_bucket/$destination_key" location

"use strict";

const AWS = require("aws-sdk");
const awsOptions = {
  region: "us-east-1",
  httpOptions: {
    timeout: 900000 // Matching Lambda function timeout
  }
};
const s3 = new AWS.S3(awsOptions);
const archiver = require("archiver");
const stream = require("stream");

// Function used to stream bytes of archived data directly to the S3 zip location
const streamTo = (bucket, key) => {
  var passthrough = new stream.PassThrough();
  s3.upload(
    {
      Bucket: bucket,
      Key: key,
      Body: passthrough,
      ContentType: "application/zip",
      ServerSideEncryption: "AES256"
    },
    (err, data) => {
      if (err) throw err;
    }
  );
  return passthrough;
};

// Function to get stream of bytes from S3 files
const getStream = (bucket, key) => {
  let streamCreated = false;
  const passThroughStream = new stream.PassThrough();

  passThroughStream.on("newListener", event => {
    if (!streamCreated && event == "data") {
      const s3Stream = s3
        .getObject({ Bucket: bucket, Key: key })
        .createReadStream();
      s3Stream
        .on("error", err => passThroughStream.emit("error", err))
        .pipe(passThroughStream);

      streamCreated = true;
    }
  });

  return passThroughStream;
};

// Main function
exports.handler = async (event, context, callback) => {
  // Get the parameters
  var sourceBucket = event["source_bucket"];
  var destinationKey = event["destination_key"];
  var destinationBucket = event["destination_bucket"];
  var files = event["files"];

  // Remove leading "/" if present
  var destinationKeyProcessed = destinationKey;
  if(destinationKey[0] == "/"){
    destinationKeyProcessed = destinationKey.slice(1);
  }

  await new Promise(async (resolve, reject) => {
    // Start destination stream
    var zipStream = streamTo(destinationBucket, destinationKeyProcessed);
    zipStream.on("close", resolve);
    zipStream.on("end", resolve);
    zipStream.on("error", reject);

    // Connect the archive to the destination stream
    var archive = archiver("zip");
    archive.on("error", err => {
      throw new Error(err);
    });
    archive.pipe(zipStream);

    var filesAlreadyInTheArchive = [];
    // Process each stream
    for (const file of files) {
        // Remove leading "/" if present
        var fileProcessed = file;
        if(file[0] == "/"){
          fileProcessed = file.slice(1);
        }

        // Get fileName from path
        var words = fileProcessed.split("/")
        var fileName = words[words.length - 1]

        // Treat the case if we have many files with the same name
        if (filesAlreadyInTheArchive.includes(fileName)) {
          var n = fileName.lastIndexOf(".");
          var timestamp = +new Date()
          fileName = fileName.slice(0, n) + fileName.slice(n).replace(".", "." + timestamp + ".");
        }
        filesAlreadyInTheArchive.push(fileName)
        archive.append(getStream(sourceBucket, fileProcessed), {
          name: fileName
        });
    }

    // Finalize the archive
    archive.finalize();
  }).catch(err => {
    throw new Error(err);
  });

  callback(null, {
    statusCode: 200,
    body: { "destination_bucket": destinationBucket, "destination_key": destinationKeyProcessed}
  });
};
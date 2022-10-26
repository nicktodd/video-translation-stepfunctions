// Load the SDK for JavaScript
const AWS = require('aws-sdk');

exports.handler = async function (event, context, callback) {


  let destBucket = process.env.FINAL_OUTPUT_BUCKET;
  let audioInputFileName = event.file_name;

  // sort out the original video filename
  let originalVideoFileNameWithoutTimeStamp = audioInputFileName.substring(10);
  console.log("video file name without timestamp is " + originalVideoFileNameWithoutTimeStamp);
  let originalVideoFilename = originalVideoFileNameWithoutTimeStamp.split("_translated")[0];
  console.log("video file is " + originalVideoFilename);

  // now get the subtitles
  let tranlatedSubtitlesLanguage = originalVideoFilename.split("__")[2].substring(0, 2);


  let threeLetterLanguageCode = codes[tranlatedSubtitlesLanguage]["639-2"].toUpperCase();
  let languageName = codes[tranlatedSubtitlesLanguage]["name"];

  console.log(threeLetterLanguageCode + " is being used for " + languageName)


  let masterVideoFile = "s3://" + originalVideoBucket + "/" + originalVideoFilename + ".mp4";
  let destinationLocation = "s3://" + destBucket + "/" + originalVideoFilename + "/";;

  console.log("destination location " + destinationLocation);


  const params = {
    Bucket: destBucket,
    Key: 'config.js', // File name you want to save as in S3
    Body: 'const videoFolderAndm3Filename = "' + originalVideoFilename + '"\n',
    ACL: 'public-read'
  };
  const s3 = new AWS.S3();
  // Uploading files to the bucket
  s3.upload(params, function (err, data) {
    if (err) {
      throw err;
    }
    console.log(`File uploaded successfully. ${data.Location}`);
  });

  let prefix = originalVideoFileName
  var listParams = {
    Bucket: destBucket,
    Prefix: prefix
  };

  let objects = await s3.listObjects(listParams).promise();
  for (var i in objects.Contents) {
    let object = objects.Contents[i];
    console.log('Making public: s3://%s/%s', destBucket, object.Key);

    var putACLParams = {
      Bucket: destBucket,
      Key: object.Key,
      ACL: 'public-read'
    };

    await s3.putObjectAcl(putACLParams).promise();
  }

}
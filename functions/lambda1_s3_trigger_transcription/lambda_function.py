import json
import boto3
import os

from datetime import datetime
def lambda_handler(event, context):
    ''' This lambda processes video files arriving in a bucket
and then creating a transcription of the audio.
The filename must end with the extension __en-US__es or equivalent
where en-US is the language of the input video, and es is the language
you want in the translation
'''
    # get the output bucket from the environment variable, or use a hardcoded default
    output_bucket_name = os.environ["OUTPUT_BUCKET"] if os.environ["OUTPUT_BUCKET"] else "transcribe.json.conygre.com"
    
    s3 = boto3.client('s3')
    if event:
        #fileobj = event["Records"][0]
        #input_bucket_name = str(fileobj['s3']['bucket']['name'])
        #audio_file_name = str(fileobj['s3']['object']['key'])
        
        input_bucket_name = "transcribe.input.conygre.com"
        audio_file_name = event["video_file"]
        print ("Filename ",audio_file_name)
        
        # this is needed to ensure that transcribe jobs get a unique name
        timestamp_file_prefix = datetime.today().strftime("%y%m%d%H%M")
        job_name = timestamp_file_prefix + (str(audio_file_name.split('.')[0]))
        original_language_code = job_name.rsplit('__', 2)[-2]
        
        transcribe = boto3.client('transcribe')
        print ("Job Name: ",job_name)
        print ("original_language_code: ",original_language_code)
        
        job_uri = "s3://" + input_bucket_name + "/" + audio_file_name 
        print("job uri is " + job_uri)
        transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode=original_language_code,
        OutputBucketName=output_bucket_name
        )
    
        
    return {
        "statusCode": 200,
        "file_name" : job_name
    }

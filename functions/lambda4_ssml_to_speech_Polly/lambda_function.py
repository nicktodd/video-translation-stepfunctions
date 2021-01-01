import json
import boto3
import os

from datetime import datetime

# voices
voiceid_list = {
    
    "en" : "Aditi",
    "fr" : "Mathieu",
    "es" : "Miguel",
    "ru" : "Maxim",
    "zh" : "Zhiyu",
    "ja" : "izuki",
    "pt" : "Ricardo",
    "de" : "Hans",
    "it" : "Giorgio",
    "tr" : "Filiz"
}


def lambda_handler(event, context):
    ''' This lambda takes an SSML file and creates the relevant audio
'''
    # get the output bucket from the environment variable, or use a hardcoded default
    output_bucket_name = os.environ["OUTPUT_BUCKET"] if os.environ["OUTPUT_BUCKET"] else "transcribe.audio.conygre.com"
    input_bucket_name = os.environ["INPUT_BUCKET"] if os.environ["INPUT_BUCKET"] else "transcribe.ssml.conygre.com"
    
    s3 = boto3.client('s3')
    ssml_file_name = event["file_name"]
    
    print ("Filename ",ssml_file_name)

    original_language_code = ssml_file_name.rsplit('__', 2)[-2]
    base_filename_ssml = ssml_file_name.rsplit('.',1)[0]
    language_string = base_filename_ssml.rsplit("__",2)
    source_language_code = language_string[-2].split('-')[0].lower()
    target_language_code= language_string[-1].lower().split("_")[0] # the final split removes the _translated bit
    
    s3.download_file(input_bucket_name, ssml_file_name, "/tmp/"+ssml_file_name)
    with open("/tmp/"+ ssml_file_name,"r", encoding="latin1") as ssml_file:
        ssml = ssml_file.read().replace('\n', '')

    polly = boto3.client('polly')
    response = polly.start_speech_synthesis_task(
        OutputFormat='mp3',
        OutputS3BucketName=output_bucket_name,
        Text=ssml,
        OutputS3KeyPrefix=base_filename_ssml,
        TextType ='ssml',
        VoiceId=voiceid_list[target_language_code]    
    )

    taskId = response['SynthesisTask']['TaskId']

    audio_file_name = base_filename_ssml + "." + taskId + ".mp3"

    return {
        "statusCode": 200,
        "file_name": audio_file_name
    }

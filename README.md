# Automated Translate and Transcode Video Pipeline

This application is a serverless application pipeline that does the following:
1. Take a video as an input
2. Translate the text into a different language
3. Add subtitles in the different language
4. Generate an AI based voice to dub the video with
5. Create a new version of the video with the subtitles and voice spoken in a different language

The application uses the following AWS services
1. Amazon S3
2. Amazon Lambda
3. Amzon Transcribe
5. Amazon Translate
4. Amazon Polly
5. Amazon Media Encoder
6. StepFunctions

The architecture is as follows:

![Architecture Diagram](/architecture.png)

## 1. Upload the original file
To trigger the pipeline, copy a video file into a bucket.

The Input file is named based on the original language 
and the desired translation. So in this case, the 
original is en-US and you want it in Spanish
eg.

```myvideo__en-US__es.mp4```


## 2. Transcribe the Audio
This upload triggers the first Lambda called LambdaTranscribe which transcribes the video 
and places a JSON output into a bucket called transcribe.json.conygre.com with the filename:

```timestamp```myvideo__en-US__es.json

## 3. Create Subtitles Files In Both Languages

This JSON which contains the transcribed text then needs to be converted into a subtitles file, and then translated.

This is done by the second Lambda ConvertTranscribeToSubtitle.
It creates two files:

```<timestamp>myvideo__en-US__es_original.srt```

```<timestamp>myvideo__en-US__es_translated.srt```

These files are placed into the next bucket transcribe.srt.conygre.com

## 4. Create the Speech Markup Language Files

The SRT files need to be converted into SSML files. This is done by the third Lambda ConvertSubtitleToSSML. This creates file with the name:

```<timestamp>myvideo__en-US__es_translated.ssml```

Note that it is written to ignore files with the word 'original' in them since they will not require an audio file

The file is placed into the bucket transcribe.ssml.conygre.com

## 5. Create the Audio File for the New Language

An audio file is then created based on the SSML file for the translated SSML.

This is done by the fourth Lambda called SSMLToAudio. It takes the SSML and runs Amazon Polly to create an audio file. The audio file has the name

```<timestamp>myvideo__en-US__de_translated<pollyJobId>```

## 6. Convert the output to be a new Playable Resource

The fifth and final Lambda then runs to run a **MediaConvert** job using all the files created already.

## 7. The StepFunctions

The entire flow is coordinated using Step Functions. You can see the flow here:

![Step Functions](stepfunctions.png)


## Review your Results

There is finally an HTML file called testmedia.html that can be used to display the finished media in a Web page. This can be edited for your final output.

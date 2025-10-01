# C4 Model Diagrams for Video Translation Application

This document contains C1, C2, and C3 diagrams for the automated video translation and transcoding pipeline using the C4 model architecture.

## C1 - System Context Diagram

This diagram shows the high-level view of the video translation system and how users and external systems interact with it.

```mermaid
graph TB
    User[Video Content Creator<br/>Person]
    VideoSystem[Automated Video Translation System<br/>Software System<br/>Translates videos into different languages with AI-generated voice and subtitles]
    
    %% External Systems
    AWS[Amazon Web Services<br/>Software System<br/>Cloud platform providing AI/ML services]
    WebBrowser[Web Browser<br/>Software System<br/>Views translated video content]
    
    %% Relationships
    User -->|Uploads original video| VideoSystem
    User -->|Views translated content| WebBrowser
    VideoSystem -->|Uses AI/ML services| AWS
    VideoSystem -->|Serves translated videos| WebBrowser
    WebBrowser -->|Displays content from| VideoSystem
    
    %% Styling
    classDef person fill:#08427b,stroke:#052e56,stroke-width:2px,color:#fff
    classDef system fill:#1168bd,stroke:#0b4884,stroke-width:2px,color:#fff
    classDef external fill:#999999,stroke:#6b6b6b,stroke-width:2px,color:#fff
    
    class User person
    class VideoSystem system
    class AWS,WebBrowser external
```

## C2 - Container Diagram

This diagram shows the high-level technology choices and how responsibilities are distributed across containers within the video translation system.

```mermaid
graph TB
    User[Video Content Creator<br/>Person]
    
    subgraph "Video Translation System"
        WebApp[Web Interface<br/>Container: HTML/JavaScript<br/>Displays translated video content]
        
        StepFunc[Step Functions Orchestrator<br/>Container: AWS Step Functions<br/>Orchestrates the translation workflow]
        
        S3Storage[File Storage<br/>Container: Amazon S3<br/>Stores videos, transcripts, audio, and subtitles]
        
        TranscribeLambda[Transcription Service<br/>Container: AWS Lambda + Python<br/>Transcribes video audio to text]
        
        TranslateLambda[Translation Service<br/>Container: AWS Lambda + Python<br/>Translates text and creates subtitles]
        
        SSMLLambda[SSML Generator<br/>Container: AWS Lambda + Python<br/>Converts subtitles to speech markup]
        
        PollyLambda[Speech Synthesis<br/>Container: AWS Lambda + Python<br/>Generates AI voice from SSML]
        
        MediaLambda[Media Processing<br/>Container: AWS Lambda + Node.js<br/>Combines video, audio, and subtitles]
        
        WebUpdateLambda[Web Updater<br/>Container: AWS Lambda + Node.js<br/>Updates web interface with results]
    end
    
    %% External Systems
    Transcribe[Amazon Transcribe<br/>Software System]
    Translate[Amazon Translate<br/>Software System]
    Polly[Amazon Polly<br/>Software System]
    MediaConvert[AWS MediaConvert<br/>Software System]
    
    %% User interactions
    User -->|Uploads video| S3Storage
    User -->|Views results| WebApp
    
    %% Internal workflows
    S3Storage -.->|Video upload triggers| StepFunc
    StepFunc -->|Orchestrates| TranscribeLambda
    StepFunc -->|Orchestrates| TranslateLambda
    StepFunc -->|Orchestrates| SSMLLambda
    StepFunc -->|Orchestrates| PollyLambda
    StepFunc -->|Orchestrates| MediaLambda
    StepFunc -->|Orchestrates| WebUpdateLambda
    
    %% Lambda interactions with storage
    TranscribeLambda <-->|Reads/Writes| S3Storage
    TranslateLambda <-->|Reads/Writes| S3Storage
    SSMLLambda <-->|Reads/Writes| S3Storage
    PollyLambda <-->|Reads/Writes| S3Storage
    MediaLambda <-->|Reads/Writes| S3Storage
    WebUpdateLambda -->|Updates| WebApp
    WebApp <-->|Serves content from| S3Storage
    
    %% External service calls
    TranscribeLambda -->|Uses| Transcribe
    TranslateLambda -->|Uses| Translate
    PollyLambda -->|Uses| Polly
    MediaLambda -->|Uses| MediaConvert
    
    %% Styling
    classDef person fill:#08427b,stroke:#052e56,stroke-width:2px,color:#fff
    classDef container fill:#1168bd,stroke:#0b4884,stroke-width:2px,color:#fff
    classDef external fill:#999999,stroke:#6b6b6b,stroke-width:2px,color:#fff
    
    class User person
    class WebApp,StepFunc,S3Storage,TranscribeLambda,TranslateLambda,SSMLLambda,PollyLambda,MediaLambda,WebUpdateLambda container
    class Transcribe,Translate,Polly,MediaConvert external
```

## C3 - Component Diagram (Translation Service)

This diagram shows the internal components of the Translation Service Lambda function, which is one of the core components handling text translation and subtitle generation.

```mermaid
graph TB
    subgraph "Translation Service Container (Lambda 2)"
        LambdaHandler[Lambda Handler<br/>Component: Python Function<br/>Main entry point for translation requests]
        
        TranscriptProcessor[Transcript Processor<br/>Component: Python Module<br/>Processes JSON transcription data]
        
        SubtitleGenerator[Subtitle Generator<br/>Component: Python Module<br/>Creates SRT subtitle files with timing]
        
        TranslationEngine[Translation Engine<br/>Component: Python Module<br/>Handles text translation logic]
        
        FileManager[File Manager<br/>Component: Python Module<br/>Manages S3 file operations]
        
        TimeFormatter[Time Formatter<br/>Component: Python Module<br/>Formats timestamps for SRT format]
        
        LanguageDetector[Language Detector<br/>Component: Python Module<br/>Extracts language codes from filenames]
    end
    
    %% External dependencies
    S3Client[Amazon S3 Client<br/>Component: Boto3]
    TranslateClient[Amazon Translate Client<br/>Component: Boto3]
    PySRT[PySRT Library<br/>Component: Python Package]
    
    %% Data stores
    TranscriptionBucket[Transcription Bucket<br/>Data Store: S3 Bucket<br/>Contains JSON transcription files]
    SubtitleBucket[Subtitle Bucket<br/>Data Store: S3 Bucket<br/>Contains SRT subtitle files]
    
    %% Component interactions
    LambdaHandler -->|Delegates processing| TranscriptProcessor
    LambdaHandler -->|Uses| FileManager
    
    TranscriptProcessor -->|Extracts text segments| SubtitleGenerator
    TranscriptProcessor -->|Sends text for translation| TranslationEngine
    
    SubtitleGenerator -->|Formats timestamps| TimeFormatter
    SubtitleGenerator -->|Creates SRT files| PySRT
    
    TranslationEngine -->|Calls translation API| TranslateClient
    
    FileManager -->|Downloads files| S3Client
    FileManager -->|Uploads results| S3Client
    
    LanguageDetector -->|Parses filename| LambdaHandler
    
    %% External connections
    S3Client <-->|Read/Write| TranscriptionBucket
    S3Client <-->|Write| SubtitleBucket
    TranslateClient -->|API calls| TranslateService[Amazon Translate Service]
    
    %% Data flow
    TranscriptionBucket -.->|JSON transcript| FileManager
    FileManager -.->|Processed subtitles| SubtitleBucket
    
    %% Styling
    classDef component fill:#85bbf0,stroke:#5d82a8,stroke-width:2px,color:#000
    classDef external fill:#999999,stroke:#6b6b6b,stroke-width:2px,color:#fff
    classDef datastore fill:#f0ad4e,stroke:#d58512,stroke-width:2px,color:#000
    
    class LambdaHandler,TranscriptProcessor,SubtitleGenerator,TranslationEngine,FileManager,TimeFormatter,LanguageDetector component
    class S3Client,TranslateClient,PySRT,TranslateService external
    class TranscriptionBucket,SubtitleBucket datastore
```

## Architecture Flow Summary

The system follows this high-level flow:

1. **User uploads video** → Triggers Step Functions workflow
2. **Transcription** → Converts audio to text using Amazon Transcribe
3. **Translation & Subtitles** → Translates text and creates SRT files
4. **SSML Generation** → Converts subtitles to speech markup language
5. **Speech Synthesis** → Generates AI voice using Amazon Polly
6. **Media Processing** → Combines original video with new audio and subtitles
7. **Web Update** → Makes translated video available through web interface

Each Lambda function is responsible for a specific step in this pipeline, with Step Functions orchestrating the entire workflow and S3 providing persistent storage for all intermediate and final outputs.
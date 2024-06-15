#!/usr/bin/python3
from google.cloud import speech
import sys
from google.oauth2 import service_account

def transcribe_gcs_with_word_time_offsets(
    gcs_uri: str,
) -> speech.RecognizeResponse:
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from oauth2client.client import GoogleCredentials
    import google.auth
    from google.oauth2 import service_account
    
    cred, project = google.auth.default()
    GOOGLE_APPLICATION_CREDENTIALS = './application_default_credentials.json'
    API_KEY="d6INXS5VTmfyzjrNeb+xBBST4VuExzs2oYNO/gph"
    
    from google.oauth2 import service_account

    #cred = service_account.Credentials.from_service_account_file(
    #GOOGLE_APPLICATION_CREDENTIALS)
    # Grab the application's default credentials from the environment.
    #cred = GoogleCredentials.get_application_default()
    print(cred)



    client = speech.SpeechClient(credentials=cred)

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="es-MX",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=1500)

    for result in result.results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
        print(f"Confidence: {alternative.confidence}")

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )

    return result

  



for idFile in sys.argv[1:]:
    inpath=f'gs://env_coop-audio/resample/{idFile}.wav'
    #outpath=f'/datalake/trans/{ifFile}'
    outpath=f'/home/ramja/proyectos/PyCoop/{idFile}'
    response = transcribe_gcs_with_word_time_offsets(inpath)

       
        



from datetime import datetime
import os

# Importar namespaces
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv

def main():
    try:
        global speech_config

        # Obter configurações
        load_dotenv()
        ai_key = ""
        ai_region = ""

        # Configurar serviço de fala
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        print('Pronto para utilizar serviço de fala em:', speech_config.region)


        # Obter entrada por fala
        command = TranscribeCommand()
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configurar reconhecimento de fala
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)

    # OPCIONAL: Definir idioma para Português do Brasil
    speech_config.speech_recognition_language = "pt-BR"

    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Fale agora...')


    # Processar entrada de fala
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)


    # Retornar o comando
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)

    # Configurar síntese de fala
    speech_config.speech_synthesis_voice_name = "pt-BR-DonatoNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)


    # Sintetizar saída falada
    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


    # Exibir a resposta
    print(response_text)


if __name__ == "__main__":
    main()
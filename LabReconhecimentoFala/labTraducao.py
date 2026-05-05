from datetime import datetime
import os

# Importar namespaces
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv

def main():
    try:
        global speech_config
        global translation_config

        # Obter configurações
        load_dotenv()
        ai_key = os.getenv("KEY")
        ai_region = os.getenv("REGIAO")

        
        
        # Configurar tradução
        translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('es')
        translation_config.add_target_language('hi')
        translation_config.add_target_language('pt')

        print('Preparado para traduzir de',translation_config.speech_recognition_language)


        # Configurar fala
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)


        # Obter entrada do usuário
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nInforme uma linguagem para traduzir\n fr = Francês\n es = Espanhol\n hi = Hindi\n Digite outra opção para parar\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'


    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Traduzir fala
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print("Fale agora...")
    result = translator.recognize_once_async().get()
    print('Traduzindo"{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)


    # Sintetizar tradução
    voices = {
        "fr": "fr-FR-HenriNeural",
        "es": "es-ES-ElviraNeural",
        "hi": "hi-IN-MadhurNeural"
    }
    translation_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(translation_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)



if __name__ == "__main__":
    main()

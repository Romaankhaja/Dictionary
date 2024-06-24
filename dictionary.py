import pyttsx3
from PyDictionary import PyDictionary
import speech_recognition as spr

# Speaking class
class Speak:
    def SpeakWord(self, audio):
        pSpeakEngine = pyttsx3.init('sapi5')
        pVoices = pSpeakEngine.getProperty('voices')
        pSpeakEngine.setProperty('voices', pVoices[0].id)
        pSpeakEngine.say(audio)
        pSpeakEngine.runAndWait()

# Create Recognizer, Microphone instance
sRecog = spr.Recognizer()
sMic = spr.Microphone()

try:
    with sMic as source:
        print("Speak 'Hello' to initiate the Speaking Dictionary!")
        print("----------------------------------------------")

        sRecog.adjust_for_ambient_noise(source, duration=0.5)
        rAudio = sRecog.listen(source)

        szHello = sRecog.recognize_google(rAudio, language='en-US')
        szHello = szHello.lower()

    if 'hello' in szHello:
        sSpeak = Speak()
        pDict = PyDictionary()

        print("Which word do you want to find? Please speak slowly.")
        sSpeak.SpeakWord("Which word do you want to find? Please speak slowly.")

        recognized = False
        while not recognized:
            with sMic as source2:
                sRecog.adjust_for_ambient_noise(source2, duration=0.5)
                rAudio2 = sRecog.listen(source2)

                szInput = sRecog.recognize_google(rAudio2, language='en-US')

                try:
                    print(f"Did you say '{szInput}'? Please answer with yes or no.")
                    sSpeak.SpeakWord(f"Did you say '{szInput}'? Please answer with yes or no.")

                    sRecog.adjust_for_ambient_noise(source2, duration=0.5)
                    rAudioYN = sRecog.listen(source2)

                    szYN = sRecog.recognize_google(rAudioYN, language='en-US')
                    szYN = szYN.lower()

                    if 'yes' in szYN:
                        szMeaning = pDict.meaning(szInput)
                        if szMeaning:
                            print("The meaning is:")
                            print(szMeaning)
                            sSpeak.SpeakWord("The meaning is " + str(szMeaning))
                            recognized = True  # Exit the loop on successful recognition
                        else:
                            print("Word not found in the dictionary.")
                            sSpeak.SpeakWord("Word not found in the dictionary.")
                            recognized = True  # Exit the loop as input is confirmed
                    elif 'no' in szYN:
                        sSpeak.SpeakWord("Please provide the correct word again.")
                    else:
                        sSpeak.SpeakWord("Sorry, I didn't understand. Please try again.")

                except spr.UnknownValueError:
                    sSpeak.SpeakWord("Unable to understand the input. Please try again.")
                except spr.RequestError as e:
                    sSpeak.SpeakWord("Unable to provide required output.")

except spr.UnknownValueError:
    print("Speech recognition could not understand audio.")
except spr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")

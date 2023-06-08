import speech_recognition as sr

# 인스턴스 생성
r = sr.Recognizer()

# 마이크에서 음성을 캡처
with sr.Microphone() as source:
    print("말하세요:")
    audio = r.listen(source)

    try:
        # Google 음성 인식을 사용하여 음성을 텍스트로 변환
        print("Google Speech Recognition thinks you said: " + r.recognize_google(audio, language='ko-KR'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

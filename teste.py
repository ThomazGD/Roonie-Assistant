import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Diga algo:")
    audio = r.listen(source)

try:
    texto = r.recognize_google(audio, language='pt-BR')
    print("Você disse: " + texto)
except sr.UnknownValueError:
    print("Não entendi o que você disse")
except sr.RequestError as e:
    print("Erro ao se conectar com o serviço: {0}".format(e))

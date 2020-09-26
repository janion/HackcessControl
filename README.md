# Smart Home [Working Title]
This is an experimental project to create a central "database" polling architecture for smart home related applications.
The premise is simple: create a "database" server which allows clients to add data fields, set their value and poll their value.

An abstract client is provided, but implementations are not limited in their function.
Initial example implementations show updating and polling the epoch time, and updating and polling the state of a
button on an ESP8266 microcontroller running MicroPython.

Plans are to create a client with hotword detection via [Snowboy](https://github.com/Kitt-AI/snowboy)
and speech recognition via [SpeechRecognition](https://github.com/Uberi/speech_recognition) using Google speech API.

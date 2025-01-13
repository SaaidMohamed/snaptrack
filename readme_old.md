# [Sesame][pypi-url]

[pypi-url]: https://github.com/code50/67076879/blob/main/project/README.md


## Description:
[Sesame](https://github.com/code50/67076879/tree/main/project) is a virtual desktop assistant. It will help make your daily activities on your PC easier with voice commands. By performing a number of functions. Like creating or deleting new files, creating or deleting new folders, starting applications, searching Google, searching You tube, signing out of your account and shutting down or restarting your PC.

Video Demo: <https://youtu.be/Tz3JNFO_JwI>


## Features:
* Create new files on your deskop by saying `sesame <wait for indicator> create file named <filename.extension>`.
* Delete existing files on your deskop by saying `sesame <wait for indicator> delete file named <filename.extension>`.
* Create new Folders on your deskop by saying `sesame <wait for indicator> create folder named <foldername>`.
* Delete existing Folders on your deskop by saying `sesame <wait for indicator> delete folder named <foldername>`.
* Close any application on your PC by saying `sesame <wait for indicator> close <app name>`.
* Open any application on your PC by saying `sesame <wait for indicator> open <app name>`.
* Search anything on Google by saying `sesame <wait for indicator> sarch Google <Query>`.
* Search anything on Youtube by saying `sesame <wait for indicator> sarch Youtube <Query>`.
* Sign out of your account by saying `sesame <wait for indicator> sign out`.
* Shutdown your computer by saying `sesame <wait for indicator> shutdown computer`.
* Restart your computer by saying `sesame <wait for indicator> restart computer`.


## Installation:
Install playsound:
```sh
pip install playsound==1.2.2
```
Install AppOpener:
```sh
pip install AppOpener
```
Install speech_recognition:
```sh
pip install speech_recognition
```
Install gTTS:
```sh
pip install gTTS
```
Install pocketsphinx:
```sh
pip3 install pocketsphinx
```
In project.py, file in create_file(), delete_file(), create_folder() and delete_folder() functions make sure you choose convenient path where you want to create/delete files, and change listen-start-sound.mp3 path or it will default to speaking "recording" as an indicator to start recording.


## Requirements:
To use all of the functionality of the program, you should have installed:

* **Python** 3.8+ (required)
* **playsound** 1.2.2 (required)
* **AppOpener** 1.7+ (required)
* **speech_recognition** 3.10.0+ (required)
* **gTTS**  2.4.0+ (required)
* **pocketsphinx** 5.0.2+ (required)
* **PyAudio**    (required)




## More Information:
For more information check out these libraries :
- [SpeechRecognition 1.2.4](https://pypi.org/project/SpeechRecognition/1.2.4/)
- [pocketsphinx 5.0.2](https://pypi.org/project/pocketsphinx/)
- [appopener 1.7](https://pypi.org/project/appopener/)
- [gTTS 2.4.0](https://pypi.org/project/gTTS/)
- [playsound 1.3.0](https://pypi.org/project/playsound/)
- [webbrowser](https://docs.python.org/3/library/webbrowser.html)
- [os](https://docs.python.org/3/library/os.html)



## Author:
Mohamed Saaid




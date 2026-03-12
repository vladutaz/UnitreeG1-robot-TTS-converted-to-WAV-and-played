## UnitreeG1 robot TTS converted to WAV and played
A brief introduction of the [UnitreeG1](https://www.unitree.com/g1) in Romanian where the PCM is connected, the TTS from the unitree robotics doesnt support moultiple languages and we use another way to comunicate. By connecting using the ethernet the robot doesn't support threading and so we us a double process operation; one for converting and rendering the text to a wav file and playing it and the other for using a specified gesture. We use a map for each procces.
```python
run_in_parallel([
  Process(target=play_text, args=(asyncio.run(text(TEXT["1"])),)),
  Process(target=gestures, args=("high wave",)),
])
```

Using an [ssh](https://en.wikipedia.org/wiki/Secure_Shell) conection we can alter easly the voice lines and gesture.


### Requirements
```
pip install edge-tts
pip install edge-tts pydub
sudo apt update && sudo apt install ffmpeg
```

##### This project is not finished yet
Functions to add:
* an live interaction where you dont use the map and only the console
* an [json](https://en.wikipedia.org/wiki/JSON) file for the map and other functions
* better and optimised code and modularisation

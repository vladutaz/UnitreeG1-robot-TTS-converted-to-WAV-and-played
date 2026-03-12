## UnitreeG1 Robot — TTS to WAV and Played

A brief introduction to the [UnitreeG1](https://www.unitree.com/g1), where the PCM (Pulse-Code Modulation) audio output is used to play text in Romanian. Since Unitree Robotics' TTS system doesn't support multiple languages, we use an alternative approach. When connecting via Ethernet, the robot doesn't support threading, so we use a two-process approach: one for converting the text to a WAV file and playing it, and another for performing a specified gesture. We use a map for each process:

```python
run_in_parallel([
  Process(target=play_text, args=(asyncio.run(text(TEXT["1"])),)),
  Process(target=gestures, args=("high wave",)),
])
```

Using an [SSH](https://en.wikipedia.org/wiki/Secure_Shell) connection, we can easily alter the voice lines and gestures.

### Requirements

```sh
pip install edge-tts
pip install edge-tts pydub
sudo apt update && sudo apt install ffmpeg
```

##### This project is not finished yet

Functions to add:

* a live interaction mode using only the console, without the predefined map
* a config file for the map and other settings
* better code structure and modularization
 

import os
import sys
import time
import asyncio
import subprocess
import edge_tts
from multiprocessing import Process
sys.path.append('/home/gaby/unitree_sdk2_python')


from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize, ChannelPublisher
from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient
from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient
from unitree_sdk2py.g1.arm.g1_arm_action_client import G1ArmActionClient
from unitree_sdk2py.g1.arm.g1_arm_action_client import action_map
from dataclasses import dataclass

INTERFACE = "enp4s0"
TEXT = {
    "1": "Bună ziua! Eu sunt Clara, noua membră a echipei de cercetare.",
    "2": "Sunt aici să lucrez alături de voi și să vă ajut cu experimentele și sarcinile care cer precizie și consecvență.",
    "3": "Nu obosesc, nu mă grăbesc și pot repeta un proces de câte ori este nevoie până când rezultatul este cel dorit.",
    "4": "Îmi place să cred că sunt o colegă de încredere: atentă, calmă și mereu pregătită să dau o mână de ajutor.",
    "5": "În același timp, vă urez bun venit în Centrul de Cercetare C 0 9 din Institutul de Cercetare-Dezvoltare al Universității Transilvania din Brașov.",
    "6": "Mă bucur să vă cunosc. Vă rog, poftiți în sală.",
    "7": "Eu mă retrag puțin ca să pregătesc niște cafeluțe. Ne revedem imediat.",
    "8": "Sunt încântată de cunoștință, mă bucur să fac parte din echipă și vă mulțumesc."
}
VOICE = "ro-RO-AlinaNeural"

async def text_to_pcm(text, voice):
    """Generates audio and converts it to G1-compatible PCM using ffmpeg.
    Args:
        text: what shoud it say
        voice: what voice should say it

    https://github.com/rany2/edge-tts/tree/master
    """
    # Generate temporary MP3
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("temp.mp3")
    
    # Convert MP3 to Raw PCM (16k, 16bit, mono)
    # G1 is extremely strict about these settings
    cmd = [
        "ffmpeg", "-y", "-i", "temp.mp3",
        "-f", "s16le", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1", "temp.pcm"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open("temp.pcm", "rb") as f:
        return f.read()

def play_text(pcm_data):
    """
    Plays the pcm_data from the text
    
    Args:
        pcm_data

        
    https://github.com/SYUCT-InfoEng/PCM_data
    """
    # Corrected Initialization
    ChannelFactoryInitialize(0, INTERFACE)
    
    client = AudioClient()
    client.Init()
    
    client.SetVolume(100)
    
    print("Streaming audio to G1...")
    # PlayStream arguments: (app_name, stream_id, pcm_data_list)
    # We convert pcm_data (bytes) to a list of integers
    client.PlayStream("tts_stream", "unique_id_123", list(pcm_data))

def gestures(gesture: str, remain=0):
    """
    Chose whitch gesture should play on the map
    
    gesture: "" string
    remain: if the emote remains up or goes automatically out


    https://github.com/unitreerobotics/unitree_sdk2_python/blob/master/example/g1/high_level/g1_arm_action_example.py
    """
    print(f"Gesture started: {gesture}")
    ChannelFactoryInitialize(0, sys.argv[1])

    armAction_client = G1ArmActionClient()  
    armAction_client.SetTimeout(10.0)
    armAction_client.Init()
    armAction_client.ExecuteAction(action_map.get(gesture))
    print(f"Gesture ended: {gesture}")
    time.sleep(2)
    if(remain == 0):
        armAction_client.ExecuteAction(action_map.get("release arm"))
    time.sleep(1)

def run_in_parallel(processes: list):
    # Start them all
    for p in processes:
        p.start()

    # Join them all
    for p in processes:
        p.join()


async def text(text=TEXT["1"], voice=VOICE):
    try:
        pcm = await text_to_pcm(text, voice)
        print("Success!")
        return pcm
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <network_interface>")
        sys.exit(1)
    

    print("# 1")
    run_in_parallel([
        
        Process(target=play_text, args=(asyncio.run(text(TEXT["1"])),)),
        Process(target=gestures, args=("high wave",)),
    ])

    print("# 2")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["2"])),)),
        Process(target=gestures, args=("x-ray",))
    ])

    print("# 3")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["3"])),)),  
        Process(target=gestures, args=("x-ray",))
    ])

    print("# 4")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["4"])),)),
        Process(target=gestures, args=("face wave",))
    ])

    print("# 5")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["5"])),)),
        Process(target=gestures, args=("high five",))
    ])

    print("# 6")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["6"])),)),
        Process(target=gestures, args=("right kiss",))
    ])

    print("# 7")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["7"])),)),
        Process(target=gestures, args=("right hand up",))
    ])

    print("# 8")
    run_in_parallel([
        Process(target=play_text, args=(asyncio.run(text(TEXT["8"])),)),
        Process(target=gestures, args=("two-hand kiss",))
    ])

    gestures("shake hand", handshake=1)
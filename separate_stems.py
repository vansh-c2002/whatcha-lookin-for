from pathlib import Path
import subprocess

def separate_stems(parent_folder):
    for song_file in Path(parent_folder).glob("*.mp3"):
        # y, sr = librosa.load(song_file)
        # duration = librosa.get_duration(y=y, sr=sr)
        
        command = [
                "demucs",
                "-n", "htdemucs",
                "-o", str(parent_folder), # maybe add a /trying or some subfolder here
                str(song_file)
            ]
        
        subprocess.run(command, check=True)
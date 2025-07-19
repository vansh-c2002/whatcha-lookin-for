from pathlib import Path
import subprocess

def separate_stems(song_file):

        command = [
                "demucs",
                "-n", "htdemucs",
                "-o", str(song_file.parent), # maybe add a /trying or some subfolder here
                str(song_file)
            ]
        
        try:
            subprocess.run(command, check=True)
            print(f"Stems separated for: {song_file.name}")
        except:
            print(f"Error running Demucs on {song_file.name}")

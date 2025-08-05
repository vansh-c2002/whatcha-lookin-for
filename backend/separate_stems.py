from pathlib import Path
import subprocess

def separate_stems(song_file): # consider inputting track name, to show that in the terminal too

        command = [
                "demucs",
                "-n", "htdemucs_6s",
                "-o", str(song_file.parent), # maybe add a /trying or some subfolder here
                str(song_file)
            ]
        
        try:
            subprocess.run(command, check=True)
            print(f"Stems separated for: {song_file.name}")
        except:
            print(f"Error running Demucs on {song_file.name}")
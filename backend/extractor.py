import librosa
import os
import numpy as np
import mutagen
from pathlib import Path

def detect_instrument_presence_stem(stem_audio, sr=22050):

    # Average loudness/energy
    mean_rms_energy = np.mean(librosa.feature.rms(y=stem_audio)[0])
    
    # Threshold (tune this!)
    energy_threshold = 0.01  # Found Empirically!
    
    return 1 if mean_rms_energy > energy_threshold else 0

def detect_instrument_presence_song(song_folder):
    
    song_folder = Path(song_folder)
    stem_files = {}
    for audio_file in song_folder.glob("*.wav"):
        stem_name = audio_file.stem  
        stem_files[stem_name] = audio_file 

    expected_stems = ['vocals', 'drums', 'bass', 'piano', 'guitar', 'other']
    results = {}
    
    # Check each expected stem
    for stem_name in expected_stems:
        if stem_name in stem_files:
            try:
                # Load the stem audio
                stem_audio, _ = librosa.load(stem_files[stem_name], sr=22050)
                
                # Run your detection method
                presence = detect_instrument_presence_stem(stem_audio)
                results[stem_name] = presence
                
            except Exception as e:
                print(f"  Error analyzing {stem_name}: {e}")
                results[stem_name] = 0
        else:
            print(f"  Warning: {stem_name}.wav not found")
            results[stem_name] = 0
    
    return int(results['vocals']), int(results['drums']), int(results['bass']), int(results['piano']), int(results['guitar']), int(results['other'])



# Claude's method with error handling
# def analyze_stems_in_folder(song_folder):
#     """
#     Analyze stems in a single song folder and return presence detection
    
#     Args:
#         song_folder: Path to folder containing piano.wav, bass.wav, drums.wav, others.wav
        
#     Returns:
#         tuple: (piano, drums, bass, others) - each value is 0 or 1
#     """
    
#     # Define the stem files to check
#     stem_files = {
#         'piano': song_folder / 'piano.wav',
#         'drums': song_folder / 'drums.wav', 
#         'bass': song_folder / 'bass.wav',
#         'others': song_folder / 'others.wav'
#     }
    
#     results = {}
    
#     # Check each stem file
#     for stem_name, stem_path in stem_files.items():
#         if stem_path.exists():
#             try:
#                 # Load the stem audio
#                 stem_audio, _ = librosa.load(stem_path, sr=22050)
                
#                 # Run your detection method
#                 presence = detect_instrument_presence_stem(stem_audio)
#                 results[stem_name] = presence
                
#                 print(f"  {stem_name}: {'present' if presence else 'absent'}")
                
#             except Exception as e:
#                 print(f"  Error analyzing {stem_name}: {e}")
#                 results[stem_name] = 0
#         else:
#             print(f"  Warning: {stem_path} not found")
#             results[stem_name] = 0
    
#     # Return in the order you specified
#     return results['piano'], results['drums'], results['bass'], results['others']

def detect_basic_info(song_folder):
    song_folder = Path(song_folder)
    
    try:
        artist, title = song_folder.name.split(" - ", 1)
    except ValueError:
        artist, title = "Unknown Artist", song_folder.name

    vocals_path = song_folder / 'vocals.wav'
    sample, _ = librosa.load(vocals_path, sr=22050)
    duration = librosa.get_duration(y=sample, sr=22050)

    return title.strip(), artist.strip(), duration


# Con - Website lists multiple genres per track, but metadata only takes one

def detect_genre(file_path):
    audio = mutagen.File(file_path)
    if audio and 'TCON' in audio: # this is where the genre is
        return audio['TCON'].text[0]
    else:
        return 'Unknown'
import os
import librosa
import numpy as np

DB_DIR = "/home/gvilag/Prova/Database"
OUTPUT_FILE = "/home/gvilag/Prova/audio_database.npz"

def extract_mfcc(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfcc.T  

def build_database(db_dir, output_file):
    db_mfcc = {}
    
    for file in os.listdir(db_dir):
        if file.endswith(".wav"):
            path = os.path.join(db_dir, file)
            print(f"Processing {file}...")
            db_mfcc[file] = extract_mfcc(path)
    
    
    np.savez_compressed(output_file, **db_mfcc)
    print(f"\nDatabase saved to {output_file}")

if __name__ == "__main__":
    build_database(DB_DIR, OUTPUT_FILE)

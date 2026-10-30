import numpy as np
import librosa
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from multiprocessing import Pool, cpu_count

DATABASE_FILE = "/home/gvilag/Prova/audio_database.npz"


def extract_mfcc(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfcc.T


def dtw_compare(args):
    filename, mfcc_db, mfcc_input = args
    distance, _ = fastdtw(mfcc_input, mfcc_db, dist=euclidean)
    return filename, distance


class AudioComparerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Comparació d'àudios")
        root.geometry("700x550")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

        self.title_label = ttk.Label(
            root,
            text="Comparació d'àudios",
            font=("Helvetica", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(15, 10))

        self.btn_load = ttk.Button(
            root,
            text="Tria àudio d'input",
            command=self.load_audio
        )
        self.btn_load.grid(row=1, column=0, pady=10)

        self.progress = ttk.Progressbar(root, length=450, mode="determinate")
        self.progress.grid(row=2, column=0, pady=10, sticky="ew", padx=20)

        self.frame_text = ttk.Frame(root, padding=10)
        self.frame_text.grid(row=3, column=0, sticky="nsew")
        root.rowconfigure(3, weight=1)

        self.frame_text.columnconfigure(0, weight=1)
        self.frame_text.rowconfigure(0, weight=1)

        self.text_area = scrolledtext.ScrolledText(
            self.frame_text,
            width=70,
            height=20,
            wrap="word"
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")

        self.input_audio_path = None

    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if path:
            self.input_audio_path = path
            self.text_area.insert(tk.END, f"Àudio d'input carregat:\n{path}\n\n")
            self.compare()

    def compare(self):
        if not self.input_audio_path:
            return

        self.text_area.insert(tk.END, "Carregant base de dades...\n")
        self.root.update()

        db_data = np.load(DATABASE_FILE, allow_pickle=True)
        mfcc_input = extract_mfcc(self.input_audio_path)

        files = list(db_data.files)
        total = len(files)
        self.progress["maximum"] = total

        pool = Pool(cpu_count())
        tasks = [(filename, db_data[filename], mfcc_input) for filename in files]

        results = []
        for i, res in enumerate(pool.imap(dtw_compare, tasks), 1):
            results.append(res)
            self.progress["value"] = i
            self.root.update_idletasks()

        pool.close()
        pool.join()

        results.sort(key=lambda x: x[1])

        self.text_area.insert(tk.END, "\n--- Resultats ---\n")
        for rank, (file, dist) in enumerate(results, start=1):
            self.text_area.insert(tk.END, f"{rank}. {file} - DTW: {dist:.2f}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioComparerGUI(root)
    root.mainloop()

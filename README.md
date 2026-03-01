# 🎵 Basic Audio Visualizer

## 📝 Project Description

This project is a **basic audio visualizer** that creates dynamic visual effects in real-time based on the beats and frequencies of an audio file. The visualizer analyzes the waveform and frequency data to generate visuals that respond to the rhythm and intensity of the music, offering an engaging, synchronized audio-visual experience.

> **Note:** The user must manually **copy and paste the path** of the audio file—there is **no graphical interface** for file selection.

---

## 🚀 Key Features

- 🎧 Upload and play audio files from local storage  
- 📊 Real-time audio analysis (frequency and amplitude)  
- 🎨 Visual effects that react to beats and sound dynamics  
- 🛠️ Basic playback and rendering loop (no GUI for file input)

---

## 📦 Libraries Used

- **OS** – Standard Python library for interacting with the operating system (e.g., file paths, folder management)  
- **Numpy** – Used for numerical computations and signal processing, like handling audio data arrays  
- **Pygame** – Handles rendering of real-time visual elements and basic audio playback  
- **Pydub** – Loads and processes audio files (e.g., converts MP3/WAV to raw audio data)  
- **Moviepy.editor** – Converts visualizer image frames into a video clip synchronized with the audio

---

## 📂 How to Use

1. Clone or download this repository.
2. Install the required Python libraries:
   ```bash
   pip install numpy pygame pydub moviepy

---
> **Note:** The first and last code files are the same audio visualizer. The only difference is that in the **first code**, after the visualizer plays, it **automatically downloads the video to the current directory** using `ImageSequenceClip` from the `moviepy` library.

> 🎬 **Here's a quick demo of my project in action:**
![image alt](https://github.com/bmsam/Audio_Visualizers_basic/blob/main/all%20mix.gif?raw=true)

---
## NOTE 
I completed this project in Oct 2024. The below img is the evidence to it. 

![img](https://github.com/bmsam/Audio_Visualizers_basic/blob/ef697ba1da364aa1a2a0acf627991c4383c25958/Proof.png)

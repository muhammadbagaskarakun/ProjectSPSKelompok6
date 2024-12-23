![image](https://github.com/user-attachments/assets/4848a643-4728-4254-b9ea-75358566438d)
This Python project is an audio recording application built using the PyQt5 framework for the user interface, PyAudio for audio input, and PyQtGraph for live signal visualization. The app allows users to record, save, visualize, and upload audio signals to Edge Impulse for further analysis, including classifying the signal as the PSU noise or not.
Features
Audio Recording:

Records audio using any available input device.
Adjustable input device selection.
Signal Visualization:

Displays the audio signal in both the time and frequency domains in real-time during recording.
Allows saved recordings to be visualized.
File Management:

Saves recordings in .wav format.
Tracks saved signals for easy retrieval.
Edge Impulse Integration:

Uploads audio recordings directly to the Edge Impulse platform using API keys.
Labels recordings for organized uploads.
Reset and Real-time Updates:

![image](https://github.com/user-attachments/assets/f0820e51-bf5e-414d-9277-c11a1b08cce2)
![image](https://github.com/user-attachments/assets/df778a2f-a6b6-4d5f-9664-ac59b1e010d8)


Clears plots for a fresh view.
Updates the signal visualization live during recording.

Requirements
Python Libraries:
PyQt5
PyAudio
Numpy
PyQtGraph
Requests
Additional:
Qt Designer for .ui file design (optional).
Proper configuration of the Edge Impulse API key and URL.

Setup Instructions
Install Dependencies:

pip install pyqt5 pyaudio numpy pyqtgraph requests
UI File: Place the yourscript.ui file in the appropriate directory as referenced in the script 

Run the Application: Execute the script:

python your_script_name.py

Usage Instructions
Start Recording:

Select an audio input device from the dropdown menu.
Click the "Rekam" button to start recording.
Click the "Berhenti" button to stop recording.
Save Recording:

Enter a filename in the text box.
Click "Simpan" to save the audio as a .wav file.
Visualize Saved Signals:

Select a saved file from the dropdown menu.
Click "Tampilkan Sinyal" to view the signal in the time and frequency domains.
Reset Graphs:

Click "Reset" to clear the plots.
Upload to Edge Impulse:

Record and save audio.
Ensure the API key and label are set correctly in the script.
The audio file will be uploaded automatically during saving.

File Structure
Main Script: Contains the PyQt5 application logic.
UI File (percobaan10.ui): User interface design loaded dynamically.

Key Points
Audio Settings:

Sampling rate: 44100 Hz
Chunk size: 1024
Edge Impulse Integration:

Modify self.api_key and self.api_url in the save_recording() method to match your project details.

Error Handling:

Ensure selected devices are valid before starting recording.
Display appropriate messages for missing input or errors.

Acknowledgements
PyQt5: For GUI development.
PyAudio: For audio recording capabilities.
Edge Impulse: For providing machine learning ingestion APIs.
PyQtGraph: For real-time plotting.

Author
Developed by Muhammad Bagaskara, Lusty Hanna Isyajidah, and Kanaya Revania.

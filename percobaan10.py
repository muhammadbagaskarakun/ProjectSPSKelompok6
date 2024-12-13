import sys
import numpy as np
import pyaudio
import wave
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import os
import requests


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi(r"C:\Users\bagas\projectSPSbagas\minprosps\sps_env\Lib\site-packages\qt5_applications\Qt\bin\percobaan10.ui", self)

        # Connect widgets
        self.pushButton.clicked.connect(self.toggle_recording)
        self.pushButton_2.clicked.connect(self.save_recording)
        self.pushButton_3.clicked.connect(self.reset_graphics)
        self.pushButton_4.clicked.connect(self.display_signal)

        # Initialize pyqtgraph PlotWidgets
        self.widget.setLayout(QtWidgets.QVBoxLayout())
        self.widget_2.setLayout(QtWidgets.QVBoxLayout())
        self.plot1 = pg.PlotWidget()
        self.plot2 = pg.PlotWidget()
        self.widget.layout().addWidget(self.plot1)
        self.widget_2.layout().addWidget(self.plot2)
        self.plot1.setBackground('w')
        self.plot2.setBackground('w')

        # Audio variables
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_live_plot)

        self.sample_rate = 44100  # Sampling rate
        self.chunk = 1024  # Chunk size
        self.saved_signals = {}

        # Populate audio input devices
        self.populate_audio_devices()

    def populate_audio_devices(self):
        """Populate comboBox with available input devices."""
        self.comboBox_2.clear()
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:  # Check for input capability
                self.comboBox_2.addItem(device_info['name'], i)
        print("Available audio input devices populated.")

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        selected_device_index = self.comboBox_2.currentData()
        if selected_device_index is None:
            print("Please select an audio input device.")
            return

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=selected_device_index,
            frames_per_buffer=self.chunk
        )
        self.recording = True
        self.frames = []
        self.timer.start(50)  # Update live plot every 50ms
        self.pushButton.setText("Berhenti")

    def stop_recording(self):
        self.recording = False
        self.timer.stop()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.pushButton.setText("Rekam")

    def save_recording(self):
        filename = self.lineEdit.text()
        if not filename:
            print("Please enter a filename.")
            return

        filename = f"{filename}.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.saved_signals[filename] = np.frombuffer(b''.join(self.frames), dtype=np.int16)
        self.comboBox.addItem(filename)  # Assume comboBox is used for saved signals
        print(f"Saved recording as {filename}")

        # Edge Impulse Settings
        # self.api_url = "https://ingestion.edgeimpulse.com/api/training/files"
        # self.api_key = "ei_3a0dc7928cc2f957750e1eda36f02d07514e3349724e0921"  # Ganti dengan API Key Anda
        self.api_url = "https://ingestion.edgeimpulse.com/api/testing/files"
        self.api_key = "ei_0d13965e830f2c1b930251c29f5e39cd4d0dcdde2b681547" 
        self.label = "Test"  # Ganti dengan label kategori audio

    # Upload the audio file to Edge Impulse
        self.upload_audio_to_edge_impulse(filename)

    def upload_audio_to_edge_impulse(self, filename):
        url = self.api_url

        with open(filename, "rb") as f:
            response = requests.post(
                url,
                headers={
                    "x-label": self.label,
                    "x-api-key": self.api_key,
                },
                files={"data": (os.path.basename(filename), f, "audio/wav")},
            )

        if response.status_code == 200:
            print(f"Uploaded {filename} successfully to Edge Impulse!")
        else:
            print(f"Failed to upload {filename}. Status code: {response.status_code}")
            print("Response text:", response.text)

    def reset_graphics(self):
        self.plot1.clear()
        self.plot2.clear()

    def display_signal(self):
        selected_file = self.comboBox.currentText()  # Assume comboBox is used for saved signals
        if not selected_file:
            print("Please select a signal.")
            return

        signal = self.saved_signals.get(selected_file)
        if signal is not None:
            self.plot1.clear()
            self.plot2.clear()

            time = np.linspace(0, len(signal) / self.sample_rate, num=len(signal))
            self.plot1.plot(time, signal, pen="b")

            # Frequency domain (DFT)
            freq = np.fft.rfftfreq(len(signal), 1 / self.sample_rate)
            fft_magnitude = np.abs(np.fft.rfft(signal))
            self.plot2.plot(freq, fft_magnitude, pen="r")

    def update_live_plot(self):
        if self.recording:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)
            signal = np.frombuffer(data, dtype=np.int16)
            time = np.linspace(0, len(signal) / self.sample_rate, num=len(signal))
            self.plot1.clear()
            self.plot1.plot(time, signal, pen="g")

            # Update DFT graph live
            freq = np.fft.rfftfreq(len(signal), 1 / self.sample_rate)
            fft_magnitude = np.abs(np.fft.rfft(signal))
            self.plot2.clear()
            self.plot2.plot(freq, fft_magnitude, pen="m")

    def closeEvent(self, event):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

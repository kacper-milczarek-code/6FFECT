import os
import tempfile
import uuid
import shutil
import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal


class VideoExporter(QObject):
    """Manages video frame export to an MP4 file using OpenCV and Qt signals.

    Frames are buffered to a temporary file during recording and moved to the final
    destination upon completion or safely removed if canceled.

    Signals:
        export_finished_signal: Emitted when the video file is successfully saved.
        update_progress_bar_value (int): Emitted after each frame write with the current frame count.
    """
    export_finished_signal = Signal()
    update_progress_bar_value = Signal(int)

    def __init__(self):
        super().__init__()
        self._writer = None
        self.filename = None
        self.temp_filepath = None
        self.max_frames = 0
        self.recorded_frames = 0
        self._is_recording = False
        self.recording_canceled = False

    def start_recording(self, file_path: str, fps: int, frame_size: tuple, total_frames: int):
        """Initializes the video writer and opens a unique temporary output file.

        Args:
            file_path: The final output destination path for the MP4 video.
            fps: Frames per second of the output video.
            frame_size: Dimensions of the video frames as a (width, height) tuple.
            total_frames: Total number of frames expected to be written.
        """
        self.filename = file_path

        temp_dir = tempfile.gettempdir()
        unique_filename = f"export_cache_{uuid.uuid4().hex}.mp4"
        self.temp_filepath = os.path.join(temp_dir, unique_filename)

        self.max_frames = total_frames
        self.recorded_frames = 0
        self.recording_canceled = False

        fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        self._writer = cv2.VideoWriter(self.temp_filepath, fourcc, fps, frame_size)
        self._is_recording = True

    def add_frame(self, frame_np: np.ndarray):
        """Converts and writes an RGB frame to the temporary video file.

        Automatically calls `stop()` once `max_frames` limit is reached

        Args:
            frame_np: A numpy array representing the image frame in RGB format.
        """
        if self._is_recording and self._writer is not None and self._writer.isOpened():
            frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
            self._writer.write(frame_bgr)

            self.recorded_frames += 1
            self.update_progress_bar_value.emit(self.recorded_frames)
            if self.recorded_frames >= self.max_frames:
                self.stop()

    def stop(self):
        """Finalizes video rendering, releases file resources, and cleans up cache.

        If not canceled, replaces the destination file with the temp file and emits
        `export_finished_signal`. If canceled, removes the temp file.
        """
        self._is_recording = False
        if self._writer is not None:
            self._writer.release()
            self._writer = None

        if self.recording_canceled:
            if self.temp_filepath and os.path.exists(self.temp_filepath):
                try:
                    os.remove(self.temp_filepath)
                except OSError:
                    pass
        else:
            if self.temp_filepath and os.path.exists(self.temp_filepath):
                if os.path.exists(self.filename):
                    try:
                        os.remove(self.filename)
                    except OSError:
                        pass

                shutil.move(self.temp_filepath, self.filename)
                self.export_finished_signal.emit()

        self.filename = None
        self.temp_filepath = None

    def cancel(self):
        """Cancels the ongoing video export and cleans up temporary files."""
        self.recording_canceled = True
        self.stop()

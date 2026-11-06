from PySide6.QtCore import QUrl, QElapsedTimer
from PySide6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from src.paths import SFX_DIR


class SoundManager:
    def __init__(self):
        self.muted = False
        self.sound_volume = 0.5
        self.cooldowns = {"hover": 150, "click": 50, "success": 50, "info": 50}

        self.loaded_sounds = {}

        self.sounds_config = {
            "btn": {
                "click": SFX_DIR / "button-click.wav",
                "hover": SFX_DIR / "button-hover.wav",
            },
            "example_img_btn": {
                "click": SFX_DIR / "example_image_button-click.wav",
                "hover": SFX_DIR / "example_image_button-hover.wav",
            },
            "slider": {
                "hover": SFX_DIR / "slider-whoosh.wav",
            },
            "export": {
                "success": SFX_DIR / "export_success.wav",
                "info": SFX_DIR / "export_info.wav",
            },
        }

        self.timer = QElapsedTimer()
        self.timer.start()

        self._keep_alive_player = None
        self._keep_alive_output = None

    def load_sounds(self, parent_object):
        for wgt_type, events in self.sounds_config.items():
            self.loaded_sounds[wgt_type] = {}

            for event_type, path in events.items():
                sound = QSoundEffect(parent_object)
                sound.setSource(QUrl.fromLocalFile(str(path)))
                sound.setVolume(self.sound_volume)

                self.loaded_sounds[wgt_type][event_type] = sound

        self._init_keep_alive(parent_object)

    def _init_keep_alive(self, parent_object):
        """Opens a soundless audio stream. Prevents Windows from disconnecting application's audio"""
        self._keep_alive_output = QAudioOutput(parent_object)
        self._keep_alive_output.setVolume(0.0)

        self._keep_alive_player = QMediaPlayer(parent_object)
        self._keep_alive_player.setAudioOutput(self._keep_alive_output)

        silent_sound = self.sounds_config["btn"]["click"]
        self._keep_alive_player.setSource(QUrl.fromLocalFile(str(silent_sound)))
        self._keep_alive_player.setLoops(QMediaPlayer.Loops.Infinite)
        self._keep_alive_player.play()

    def play(self, wgt_type, event_type):
        if self.muted:
            return

        sound = self.loaded_sounds.get(wgt_type, {}).get(event_type)
        if not sound:
            return

        if sound.isPlaying():
            if not self.timer.hasExpired(self.cooldowns[event_type]):
                return
            sound.stop()

        sound.play()
        self.timer.restart()

    def toggle_mute(self):
        self.muted = not self.muted
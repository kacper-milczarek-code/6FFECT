from PySide6.QtCore import QUrl, QElapsedTimer
from PySide6.QtMultimedia import QSoundEffect

SOUND_VOLUME = 0.5
SOUND_COOLDOWNS = {"hover": 150, "click": 50}

muted = False

timer = QElapsedTimer()
timer.start()

sounds = {
    "btn": {
        "click": "assets/sfx/button-click.wav",
        "hover": "assets/sfx/button-hover.wav",
    },

    "example_img_btn": {
        "click": "assets/sfx/example_image_button-click.wav",
        "hover": "assets/sfx/example_image_button-hover.wav",
    },

    "slider": {
        "hover": "assets/sfx/slider-whoosh.wav",
    },
}

loaded_sounds = {}


def create_sound(path):
    sound = QSoundEffect()
    sound.setSource(QUrl.fromLocalFile(path))
    sound.setVolume(SOUND_VOLUME)
    return sound


def load_sounds():
    for wgt_type, events in sounds.items():
        loaded_sounds[wgt_type] = {}

        for event_type, path in events.items():
            loaded_sounds[wgt_type][event_type] = create_sound(path)


def play(wgt_type, event_type):
    if muted:
        return

    sound = loaded_sounds[wgt_type][event_type]

    if sound:
        if sound.isPlaying():
            if not timer.hasExpired(SOUND_COOLDOWNS[event_type]):
                return
            sound.stop()
        sound.play()
        timer.restart()


def toggle_mute():
    global muted
    muted = not muted

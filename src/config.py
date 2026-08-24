DEFAULT_VALUES = {
    "NO MODE": {
        "BRIGHTNESS": 20,
        "SATURATION": 20,
        "CONTRAST": 20
    },
    "FLIPPER": {
        "SPEED": 50,
        "BLOCK SIZE": 5
    },
    "FADER": {
        "SPEED": 50,
        "HOLE SIZE": 30,
        "COVERAGE": 1
    },
    "NUKER": {
        "SPEED": 60
    },
    "PUZZLER": {
        "SPEED": 80,
        "BLOCK SIZE": 5
    },
    "LINER": {
        "STRENGTH": 5,
        "GLITCH": False
    },
    "RAINBOWER": {
        "SPEED": 70,
        "BLOCK SIZE": 5,
        "SPREAD": 128
    },
}

current_effect = "NO MODE"
current_values = {mode: settings.copy() for mode, settings in DEFAULT_VALUES.items()}
current_sliders = ("BRIGHTNESS", "SATURATION", "CONTRAST")

SLIDERS_SETTINGS = {
    "NO MODE": {
        # "PARAMETR": ((raw_min, raw_max), (ui_min, ui_max), decimals)
        "BRIGHTNESS": ((0.1, 5.0), (1, 100), 1),
        "SATURATION": ((0.1, 5.0), (1, 100), 1),
        "CONTRAST": ((0.1, 5.0), (1, 100), 1)
    },

    "FLIPPER": {
        "SPEED": ((0.7, 0.9), (1, 100), 3),
        "BLOCK SIZE": ((1, 5), (1, 5), 0)
    },

    "FADER": {
        "SPEED": ((0.85, 0.95), (1, 100), 3),
        "HOLE SIZE": ((10, 100), (10, 100), 0),
        "COVERAGE": ((0.1, 0.7), (1, 100), 3)
    },

    "NUKER": {
        "SPEED": ((0.93, 1.0), (1, 100), 3)
    },

    "PUZZLER": {
        "SPEED": ((0.82, 0.92), (1, 100), 3),
        "BLOCK SIZE": ((1, 5), (1, 5), 0)
    },

    "LINER": {
        "STRENGTH": ((1, 15), (1, 15), 0),
        "GLITCH": False
    },

    "RAINBOWER": {
        "SPEED": ((0.83, 0.93), (1, 100), 3),
        "BLOCK SIZE": ((1, 5), (1, 5), 0),
        "SPREAD": ((1, 255), (1, 255), 0)
    }
}

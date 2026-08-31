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

# raw_range, ui_range, decimals
NO_MODE_SLIDERS_SETTINGS = ((0.1, 5.0), (1, 100), 1)

# convert_args contains tuple (raw_range, ui_range, decimals) used in ui_to_raw function (utils.py)
SLIDERS_SETTINGS = {
    "NO MODE": {
        "BRIGHTNESS": {
            "ui_range": (1, 100)
        },
        "SATURATION": {
            "ui_range": (1, 100)
        },
        "CONTRAST": {
            "ui_range": (1, 100)
        }
    },

    "FLIPPER": {
        "SPEED": {
            "ui_range": (1, 100),
            "convert_args": ((0.7, 0.9), (1, 100), 3)
        },
        "BLOCK SIZE": {
            "ui_range": (1, 5),
            "convert_args": ((1, 5), (1, 5), 0)
        }
    },

    "FADER": {
        "SPEED": {
            "ui_range": (1, 100),
            "convert_args": ((0.85, 0.95), (1, 100), 3)
        },
        "HOLE SIZE": {
            "ui_range": (10, 100),
            "convert_args": ((10, 100), (10, 100), 0)
        },
        "COVERAGE": {
            "ui_range": (1, 100),
            "convert_args": ((0.1, 0.7), (1, 100), 3)
        }
    },

    "NUKER": {
        "SPEED": {
            "ui_range": (1, 100),
            "convert_args": ((0.93, 1.0), (1, 100), 3)
        }
    },

    "PUZZLER": {
        "SPEED": {
            "ui_range": (1, 100),
            "convert_args": ((0.82, 0.92), (1, 100), 3)
        },
        "BLOCK SIZE": {
            "ui_range": (1, 5),
            "convert_args": ((1, 5), (1, 5), 0)
        }
    },

    "LINER": {
        "STRENGTH": {
            "ui_range": (1, 15),
            "convert_args": ((1, 15), (1, 15), 0)
        },
        "GLITCH": False
    },

    "RAINBOWER": {
        "SPEED": {
            "ui_range": (1, 100),
            "convert_args": ((0.83, 0.93), (1, 100), 3)
        },
        "BLOCK SIZE": {
            "ui_range": (1, 5),
            "convert_args": ((1, 5), (1, 5), 0)
        },
        "SPREAD": {
            "ui_range": (1, 255),
            "convert_args": ((1, 255), (1, 255), 0)
        }
    }
}

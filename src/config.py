DEFAULT_VALUES = {
    "NO MODE": {
        "BRIGHTNESS": 20,
        "SATURATION": 20,
        "CONTRAST": 20
    },
    "FLIPPER": {
        "SPEED": 10,
        "BLOCK SIZE": None
    },
    "FADER": {
        "SPEED": 10,
        "HOLE SIZE": 30,
        "COVERAGE": 1
    },
    "NUKER": {
        "SPEED": 40
    },
    "PUZZLER": {
        "SPEED": 10,
        "BLOCK SIZE": None
    },
    "LINER": {
        "SPEED": 20,
    },
    "RAINBOWER": {
        "SPEED": 10,
        "BLOCK SIZE": None,
        "SPREAD": 128
    }
}

current_effect = "NO MODE"
current_values = {m: s.copy() for m, s in DEFAULT_VALUES.items()}
current_sliders_parameters = ["BRIGHTNESS", "SATURATION", "CONTRAST"]

# raw_range, ui_range, decimals. Used in ui_to_raw function (utils.py)
NO_MODE_SLIDERS_SETTINGS = ((0.1, 5.0), (1, 100), 1)

sliders_settings = {
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
            "ui_range": (1, 20),
        },
        "BLOCK SIZE": {
            "ui_range": None,
            "range_values": None
        }
    },

    "FADER": {
        "SPEED": {
            "ui_range": (1, 20),
        },
        "HOLE SIZE": {
            "ui_range": (1, 100),
        },
        "COVERAGE": {
            "ui_range": (1, 70),
        }
    },

    "NUKER": {
        "SPEED": {
            "ui_range": (1, 100),
        }
    },

    "PUZZLER": {
        "SPEED": {
            "ui_range": (1, 20),
        },
        "BLOCK SIZE": {
            "ui_range": None,
            "range_values": None
        }
    },

    "LINER": {
        "SPEED": {
            "ui_range": (1, 100),
        }
    },

    "RAINBOWER": {
        "SPEED": {
            "ui_range": (1, 20),
        },
        "BLOCK SIZE": {
            "ui_range": None,
            "range_values": None
        },
        "SPREAD": {
            "ui_range": (1, 255),
        }
    }
}

"""
'controls.py' module
Used to update control buttons if changed in the Options scene.
"""
from constants import DEFAULT_CONTROLS, CONTROLS_DICT


class Controls:
    """Controls instance class implementation."""
    controls_str = DEFAULT_CONTROLS  # Controls as strings (initialized to default)
    controls = [CONTROLS_DICT[btn] for btn in controls_str]  # Controls as Pygame keys

    @staticmethod
    def update(controls):
        """
        Update control buttons.
        :param controls: control buttons list (string)
        """
        Controls.controls_str = controls
        Controls.controls = [CONTROLS_DICT[btn] for btn in controls]

    @staticmethod
    def get_controls():
        """Get the control buttons Pygame key list."""
        return Controls.controls

    @staticmethod
    def get_controls_str():
        """Get the control buttons strings list."""
        return Controls.controls_str

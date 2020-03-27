"""
'controls.py' module
Used to update control buttons if changed in the Options scene.
"""
from constants import  DEFAULT_CONTROLS


class Controls:
    """Controls instance class."""
    controls = DEFAULT_CONTROLS  # Initially set to default ones

    @staticmethod
    def update(controls):
        """
        Update control buttons
        :param controls: control buttons list (string)
        """
        Controls.controls = controls

    @staticmethod
    def get_controls():
        """Get the control buttons list"""
        return Controls.controls

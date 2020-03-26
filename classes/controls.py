"""
'controls.py' module
"""
import constants


class Controls:

    controls = constants.DEFAULT_CONTROLS

    @staticmethod
    def update(controls):
        Controls.controls = controls

    @staticmethod
    def get_controls():
        return Controls.controls

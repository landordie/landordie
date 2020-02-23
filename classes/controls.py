import constants


class Controls:

    controls = constants.DEFAULT_CONTROLS

    @staticmethod
    def update(ctrls):
        Controls.controls = ctrls

    @staticmethod
    def get_controls():
        return Controls.controls


class Cfg:

    WINDOW_NAME = "Remote control"
    SIZE = "1136x640"
    SIZE_MULT = 0.71

    MAIN_COLOR = "#353535"
    SUBCOLOR = "#464646"
    BUTTON_COLOR = "#505050"
    BUTTON_ACTIVE_COLOR = "#606060"
    TEXT_COLOR = "#b5b5b5"
    LINE_COLOR = "#616161"
    POINT_SELECTED_COLOR = "#ed552b"
    POINT_COLOR = "#edb62b"

    class ManipulatorConfig:

        SEND_LIMIT = 0.1

        START_POS = {'x': 300, 'y': 0, 'z': 450, 'q': 170, 'e': 90, 'f': 90}

        LIMIT_X = (0, 600)
        LIMIT_Y = (0, 600)
        LIMIT_Z = (0, 600)
        Z_ANGLE_LIMIT = (0, 300)

        Q_LIMIT = (-40, 180)
        E_LIMIT = (0, 180)
        F_LIMIT = (0, 180)
        G_LIMIT = (0, 180)

        F_POINTS = (60, 90, 120)
        G_POINTS = (60, 90, 120)

        DEFAULT_NAME = '10.10.11.72'

        #10.10.11.72


    class GloveConfig:
        LIMIT_X = (400, 770)
        LIMIT_Y = (-770, 790)
        LIMIT_Z = (-40, 860)



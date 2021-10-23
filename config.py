
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

        SEND_LIMIT = 0.3

        START_POS = {'x': -150, 'y': -150, 'z': 450, 'q': 170, 'e': 90, 'f': 90}

        LIMIT_X = (150, 600)
        LIMIT_Y = (150, 600)
        LIMIT_Z = (0, 600)
        Z_ANGLE_LIMIT = (0, 300)

        Q_LIMIT = (0, 180)
        E_LIMIT = (0, 180)
        F_LIMIT = (0, 180)
        G_LIMIT = (0, 180)

        F_POINTS = (60, 90, 120)
        G_POINTS = (60, 90, 120)

        DEFAULT_NAME = '192.168.1.182'





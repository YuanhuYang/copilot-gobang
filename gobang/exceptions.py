class GobangError(Exception):
    pass

class InvalidMove(GobangError):
    pass

class GameFinished(GobangError):
    pass

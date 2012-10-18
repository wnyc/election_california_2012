class StateException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class UnknownState(StateException):
    def __init__(self, *args, **kwargs):
        StateException.__init__(self, *args, **kwargs)

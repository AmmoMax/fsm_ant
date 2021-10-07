class FSM:
    def __init__(self):
        self.active_state = None

    def set_state(self, state):
        self.active_state = state

    def update(self, *args, **kwargs):
        if self.active_state:
            self.active_state(*args, **kwargs)

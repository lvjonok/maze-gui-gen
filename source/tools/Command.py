"""Module provides work of Edit part"""

class Command:
    def __init__(self, wl_last_state, ct_last_state):
        self.wl_last_state = wl_last_state
        self.ct_last_state = ct_last_state
        self.history = [[wl_last_state, ct_last_state]]

    def setLastState(self, wl_last_state=False, ct_last_state=False):
        """Function accepts two optional parameters and updates last state"""
        if wl_last_state:
            if self.wl_last_state == wl_last_state:
                return False
            self.wl_last_state = wl_last_state
        if ct_last_state:
            if self.ct_last_state == ct_last_state:
                return False
            self.ct_last_state = ct_last_state
        self.history.append([self.wl_last_state, self.ct_last_state])
        print(len(self.history))
        return True

    def getLastState(self):
        """get list of two matrixes 0 - WallMatrix, 1 - CellsMatrix"""
        if len(self.history) > 1:
            self.history.pop()
            return self.history[-1]
        return False

    def resetHistory(self):
        """delete history"""
        self.history = []

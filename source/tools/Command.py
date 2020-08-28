"""Module provides work of Edit part"""


class Command:
    def __init__(self, wl_last_state, ct_last_state):
        self.current = [wl_last_state, ct_last_state]
        self.past = []
        self.future = []

    def setLastState(self, wl_last_state=False, ct_last_state=False):
        """Function accepts two optional parameters and updates last state"""
        if not (wl_last_state or ct_last_state):  # at least one part should be updated
            return False
        new_wl_state, new_ct_state = self.current
        if wl_last_state:
            if self.current[0] == wl_last_state:  # it should have a new value
                return False
            new_wl_state = wl_last_state
        if ct_last_state:
            if self.current[1] == ct_last_state:  # it should have a new value
                return False
            new_ct_state = ct_last_state

        self.past.append(self.current)
        self.current = [new_wl_state, new_ct_state]

        # we erase this stack because we have a new action
        self.future = []
        return True

    def undo(self):
        """get list of two matrixes 0 - WallMatrix, 1 - CellsMatrix"""

        if (
            len(self.past) < 1
        ):  # we can return redo action if there are at least 1 action
            return False
        self.future.append(self.current)
        self.current = self.past.pop()

        return self.current

    def redo(self):
        """get last state from redo stack"""

        if (
            len(self.future) < 1
        ):  # we can return redo action if there are at least 1 action
            return
        self.past.append(self.current)
        self.current = self.future.pop()

        return self.current

    def resetHistory(self, wl_last_state, ct_last_state):
        """delete history"""
        # print('resetted history')
        self.past = []
        self.future = []
        self.current = [wl_last_state, ct_last_state]

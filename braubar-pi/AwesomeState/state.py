class State:
    finished = False
    name = None


    def run(self):
        assert 0, "run not implemented"

    def next(self):
        if self.finished:
            pass
        else:
            assert 0, "not finished"

    def progress(self):
        assert 0, "progress not implemented"

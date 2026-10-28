class ErreurAmont(Exception):
    def __init__(self, statut):
        super().__init__(f'amont {statut}')
        self.statut = statut


class ErreurBlocage(ErreurAmont):
    pass

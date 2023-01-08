class NotFoundIdVacancy(Exception):
    def __init__(self, *args):
        self.msg = args[0] if args else ""

    def __str__(self):
        return self.msg
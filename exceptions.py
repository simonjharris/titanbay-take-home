class NotFoundError(Exception):
    def __init__(self, resource: str):
        self.resource = resource
        super().__init__(f"{resource} not found")


class ConflictError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)

class ModelValidationError(ValueError):

    def __init__(self, errors):
        super().__init__("Invalid model data")
        self.errors = errors 
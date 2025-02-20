class AppDTO:
    def __init__(
        self, name: str, version: str,
        environment: str, debug_mode: bool
    ):
        self.name = name
        self.version = version
        self.environment = environment
        self.debug_mode = debug_mode

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment,
            "debug_mode": self.debug_mode
        }

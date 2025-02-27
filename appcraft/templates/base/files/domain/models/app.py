from domain.models.interfaces import ModelInterface


class App(ModelInterface):
    def __init__(
        self, name: str, version: str, environment: str, debug_mode: bool
    ):
        self._name = name
        self._version = version
        self._environment = environment
        self._debug_mode = debug_mode

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value: str):
        if not value:
            raise ValueError("Version cannot be empty")
        self._version = value

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value: str):
        if value not in ['development', 'production']:
            raise ValueError(
                "Environment must be 'development' or 'production'"
            )
        self._environment = value

    @property
    def debug_mode(self):
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Debug mode must be a boolean")
        self._debug_mode = value

    def __repr__(self):
        return (
            f"App(name={self.name}, version={self.version}, "
            f"environment={self.environment}, debug_mode={self.debug_mode})"
        )

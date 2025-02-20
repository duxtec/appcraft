class App:
    def __init__(
        self, name: str, version: str, environment: str,
        debug_mode: bool, log_level: str,
        language: str, language_preference: str, supported_languages: list,
    ):
        self._name = name
        self._version = version
        self._environment = environment
        self._debug_mode = debug_mode
        self._log_level = log_level
        self._language = language
        self._language_preference = language_preference
        self._supported_languages = supported_languages

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

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, value: str):
        if value not in ['info', 'debug', 'warning', 'error']:
            raise ValueError(
                "Log level must be one of: 'info', 'debug', 'warning', 'error'"
            )
        self._log_level = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value: str):
        if not value:
            raise ValueError("Language cannot be empty")
        self._language = value

    @property
    def language_preference(self):
        return self.__lang_preference

    @language_preference.setter
    def language_preference(self, value: str):
        if not value:
            raise ValueError("Language preference cannot be empty")
        self._language_preference = value

    @property
    def supported_languages(self):
        return self._supported_languages

    @supported_languages.setter
    def supported_languages(self, value: list):
        if not isinstance(value, list):
            raise ValueError(
                "Supported languages must be a list"
            )
        if len(value) == 0:
            raise ValueError(
                "Supported languages list cannot be empty"
            )
        self._supported_languages = value

    def __repr__(self):
        return (
            f"App(name={self.name}, version={self.version}, "
            f"environment={self.environment}, debug_mode={self.debug_mode}, "
            f"log_level={self.log_level}, "
            f"language={self.language}, "
            f"language_preference={self.language_preference}"
            f"supported_languages={self.supported_languages})"
        )

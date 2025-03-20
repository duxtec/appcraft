from domain.models.interfaces import ModelInterface


class GitHubRepository(ModelInterface):

    def __init__(
        self,
        name: str,
        url: str,
        description: str,
        is_private: bool,
    ):
        super().__init__(1)
        self.name = name
        self.url = url
        self.description = description
        self.is_private = is_private

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def url(self) -> str | None:
        return self._name

    @url.setter
    def url(self, name: str):
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def is_private(self) -> bool:
        return self._is_private

    @is_private.setter
    def is_private(self, is_private: bool):
        self._is_private = is_private

    def __repr__(self):
        return f"\
GitHubRepository(name={self._name}, description={self._description})"

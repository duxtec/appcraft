from abc import abstractmethod


class DTOInterface:
    @abstractmethod
    def to_dict(self):
        pass

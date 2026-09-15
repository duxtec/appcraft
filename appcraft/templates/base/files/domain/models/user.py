from domain.models import Model, NewModel
from domain.models.core.field import Field
from domain.value_objects.id import Id


class UserId(Id):
    pass


class NewUser(NewModel):
    username: Field[str]


class User(NewUser, Model[UserId]):
    pass

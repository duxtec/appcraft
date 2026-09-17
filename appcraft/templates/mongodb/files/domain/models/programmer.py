from domain.models import Model, NewModel
from domain.models.core.field import Field
from domain.value_objects.id import Id


class ProgrammerId(Id):
    pass


class NewProgrammer(NewModel):
    name: Field[str]
    country: Field[str]
    technologies: Field[list[str]]
    main_projects: Field[list[str]]
    bio: Field[str]


class Programmer(NewProgrammer, Model[ProgrammerId]):
    pass

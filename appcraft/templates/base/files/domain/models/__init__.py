from abc import ABC
from typing import Annotated, Generic

from domain.models.core.field import Field
from domain.models.core.pk import PK
from domain.models.core.pydantic import IdType, PydanticNewModel

NewModel = PydanticNewModel


class Model(NewModel, ABC, Generic[IdType]):
    id: Annotated[Field[IdType], PK]

from typing import TypeVar

from domain.models.core.pydantic import PydanticSchema


class Schema(PydanticSchema):
    # NOTE:
    # This base class is intended to work in two exclusive modes:
    #
    # 1. Pydantic mode (default):
    #    Keep inheritance from PydanticSchema and do NOT use __init_subclass__.
    #
    # 2. Dataclass mode (no Pydantic dependency):
    #    Remove the PydanticSchema inheritance and uncomment/enable the
    #    __init_subclass__ implementation below.
    #
    # This setup is designed to support environments
    # that do not support Pydantic.

    """
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        dataclass(frozen=True)(cls)
    """


TSchema = TypeVar("TSchema", bound=Schema)

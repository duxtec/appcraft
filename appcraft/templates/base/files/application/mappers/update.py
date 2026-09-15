from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from application.core.changes import Changes
from application.core.keys import Keys
from application.schemas import Schema
from domain.models import Model
from domain.models.core.field import Field


@dataclass(frozen=True)
class UpdateData:
    keys: Keys
    changes: Changes


class UpdateMapper:
    @staticmethod
    def from_schema(
        model: type[Model[Any]],
        schema: Schema,
    ) -> UpdateData:
        keys = Keys()
        changes = Changes()

        pks = model.primary_keys()

        for field_name in schema.model_fields_set:
            field = cast(Field[Any], getattr(model, field_name))

            value = getattr(schema, field_name)

            if field in pks:
                keys.set(field, value)
            else:
                changes.set(field, value)

        return UpdateData(
            keys=keys,
            changes=changes,
        )

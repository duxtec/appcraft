from typing import Annotated, get_args, get_origin


class _PrimaryKey:
    def is_pk(self, annotation: object) -> bool:
        if get_origin(annotation) is not Annotated:
            return False

        _, *metadata = get_args(annotation)

        return PK in metadata


PK = _PrimaryKey()

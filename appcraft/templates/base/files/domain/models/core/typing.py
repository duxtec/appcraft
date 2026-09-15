from typing import Annotated, Any, TypeVar, get_args, get_origin


def resolve_annotation(
    annotation: Any,
    mapping: dict[TypeVar, Any],
) -> Any:
    if isinstance(annotation, TypeVar):
        return mapping.get(annotation, annotation)

    origin = get_origin(annotation)

    if origin is None:
        return annotation

    if origin is Annotated:
        value, *metadata = get_args(annotation)

        return Annotated[
            resolve_annotation(value, mapping),
            *metadata,
        ]

    args = tuple(
        resolve_annotation(arg, mapping) for arg in get_args(annotation)
    )

    try:
        return origin[args]
    except TypeError:
        return annotation

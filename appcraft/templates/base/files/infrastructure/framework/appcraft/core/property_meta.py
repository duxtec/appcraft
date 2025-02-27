from abc import ABCMeta
from typing import get_origin


class PropertyMeta(ABCMeta):
    _props = []

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        params = []
        if cls is not PropertyMeta:
            if hasattr(cls, "_props"):
                props = cls._props
            else:
                props = []

        else:
            props = []

        if props and isinstance(props, list):
            if '__orig_bases__' in dct:
                for origin in dct["__orig_bases__"]:
                    origin_cls = get_origin(origin)
                    if isinstance(origin_cls, type) and origin.__args__:
                        for arg in origin.__args__:
                            params.append(arg)
                            if len(params) >= len(props):
                                break
                    if len(params) >= len(props):
                        break

            for i, param in enumerate(params):
                setattr(cls, props[i], param)

from typing import Any, Callable, Optional

from domain.value_objects.exceptions import ValueObjectError
from domain.value_objects.interfaces import ValueObjectInterface
from infrastructure.framework.appcraft.utils.printer import Printer


class InputCLIValidator:
    @staticmethod
    def get_valid_input(
        prompt: str,
        value_object: type[ValueObjectInterface],
        value: Optional[str] = None,
        error_action: Optional[Callable[[ValueObjectError], None]] = None,
        error_message: Optional[str] = None,
        max_attempts: Optional[int] = 3,
    ) -> Any:
        attempts = 0

        while max_attempts is None or attempts < max_attempts:
            if value is None:
                value = input(prompt)
                print()
            try:
                value_object_instance = value_object(value)
                return value_object_instance.value
            except ValueObjectError as e:
                value = None
                attempts += 1
                if error_action:
                    error_action(e, value)
                elif error_message:
                    Printer.warning(error_message)
                    print()
                else:
                    Printer.warning(str(e))
                    print()
                if max_attempts is not None and attempts >= max_attempts:
                    raise e
        return None

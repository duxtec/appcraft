import builtins
import gettext
import locale
import os
from abc import ABCMeta
from typing import TextIO

import polib
from infrastructure.framework.appcraft.core.app_manager import AppManager
from infrastructure.framework.appcraft.core.config import Config
from infrastructure.framework.appcraft.utils.logger import Logger
from infrastructure.framework.appcraft.utils.printer import Printer


class MessageManager:
    def __init__(self, module_name="core", locale_dir="locale"):
        self.locale_dir = os.path.join(os.getcwd(), locale_dir)
        self.module_name = module_name
        self.domain = module_name
        self._logger = Logger("MessageManager")
        self.debug = AppManager.debug_mode()
        self.language_preference = AppManager.lang_preference()
        self.load_translations()

        if not hasattr(builtins, "original_print"):
            builtins.original_print = builtins.print

        builtins.print = self.print

    @classmethod
    def build_locale_dir(cls, locale_dir="locale"):
        for root, dirs, files in os.walk(locale_dir):
            for file in files:
                if file.endswith('.po'):
                    cls.build(os.path.join(root, file))

    def build(po_file_path):
        if po_file_path.endswith('.po'):
            mo_file_path = po_file_path[:-3] + '.mo'

            if not os.path.exists(mo_file_path) or \
                os.path.getmtime(po_file_path) > \
                    os.path.getmtime(mo_file_path):
                try:
                    po = polib.pofile(po_file_path)
                    po.save_as_mofile(mo_file_path)
                    Printer.success(
                        f"Built {mo_file_path} from {po_file_path}",
                        if_debug=True
                    )
                except Exception as e:
                    Printer.error(
                        f"Failed to build {mo_file_path}: {e}",
                        if_debug=True
                    )

    def load_prefer_languages(self):
        try:
            self.sys_lang, _ = locale.getlocale()
        except Exception:
            self.sys_lang = None
        try:
            self.config_lang = Config().get("app")["lang"]
        except Exception:
            self.config_lang = None

    def load_translations(self):
        self.load_prefer_languages()

        if self.language_preference == "config":
            languages = [self.config_lang]
        else:
            languages = [self.sys_lang]

        if self.config_lang not in languages:
            languages.append(self.config_lang)

        if self.sys_lang not in languages:
            languages.append(self.sys_lang)

        if "en" not in languages:
            languages.append("en")

        for lang in languages:
            if lang is not None:
                try:
                    translation = gettext.translation(
                        self.domain,
                        localedir=self.locale_dir,
                        languages=[lang],
                    )
                    translation.install()
                    self._ = translation.gettext
                    return
                except FileNotFoundError as e:
                    self._logger.warning(
                        f"[Error] translation file not found for {str(e)}."
                    )
                except Exception as e:
                    self._logger.warning(
                        f"""\
When trying to load translation to \
{lang}: {e}\
"""
                    )

        self._logger.warning(
            f"""\
Translation file not found for: \
{', '.join(filter(None, languages))}\
"""
        )

    def get_message(self, message_name):
        try:
            if message_name == "":
                return message_name

            message = self._(message_name)

            if not message:
                message = message_name
        except Exception:
            message = message_name

        return message

    def print(
        self,
        *values: object,
        sep: str | None = " ",
        end: str | None = "\n",
        file: TextIO | None = None,
        flush: bool = False,
        **kwargs
    ):
        translated_args = [self.get_message(str(value)) for value in values]

        if hasattr(builtins, "original_print"):
            builtins.original_print(
                *translated_args, sep=sep, end=end, file=file, flush=flush,
                **kwargs
            )
        else:
            builtins.print(
                *translated_args, sep=sep, end=end, file=file, flush=flush,
                **kwargs
            )

    class TranslateMethodsMeta(ABCMeta):
        def __new__(mcs, name, bases, class_dict):
            cls = super().__new__(mcs, name, bases, class_dict)

            for attr_name in dir(Printer):
                if attr_name.startswith("__"):
                    continue

                attr = getattr(Printer, attr_name)
                if callable(attr) and attr_name not in class_dict:
                    setattr(cls, attr_name, cls._wrap_method(attr_name))

            return cls

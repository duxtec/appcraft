Locales Template
=============================
The **Locales Template** provides a **built-in internationalization (i18n) system** for managing multilingual support in applications. It automatically handles **language detection, message translation, and formatted output**, ensuring seamless adaptation to different locales.  

At its core, the **MessageManager** class manages **gettext-based translations**, loading the preferred language dynamically based on system settings or user configuration. It supports **.po and .mo files**, automatically compiling translation files when necessary.  

This template also enhances **CLI interactions** by intercepting the standard print function, ensuring that messages are automatically translated before being displayed. Integrated directly into the framework’s **Core**, the **Locales Template** requires no additional setup, providing a modular and efficient solution for multilingual applications.

# Appcraft

**Appcraft** is a framework designed to simplify the development and management of applications. It provides a structured approach to creating projects, running scripts, and testing your code.

## Installation

To get started with **Appcraft**, follow the installation instructions specific to your environment. Ensure you have Python installed, and then install Appcraft using pip:

```bash
pip install appcraft
```

## Create a New Project

To create a new project, use the following command:

```bash
appcraft init <templates>
```

Replace `<templates>` with the name of the template you wish to use.

## Available Templates

To show the list of available templates, run:

```bash
appcraft list-templates
```

## Testing and Documentation

**Appcraft** comes with built-in support for:

- **Pytest**: For running tests and ensuring your code is reliable.
- **Sphinx**: For generating documentation, making it easy to document your project.

## Running Applications

To execute the apps within your project, use:

```bash
python run
```

## Running Project Scripts

To execute helper scripts in your project, use:

```bash
python run_tools
```

Make sure that your scripts are located in the `scripts` folder and your apps are in the `app` folder.

### App and Scripts Structures

To be recognized by **Appcraft**, apps and scripts must inherit from the `App` class and use the `@App.runner` decorator. Here's an example:

```python
from infrastructure.framework.appcraft.core.app_runner import AppRunner

class MyApp(AppRunner):

    @AppRunner.runner
    def runner1(self):
        # Code for runner1
        pass

    def non_runner1(self):
        # This method does not show in the runner.
        pass
```

## Conclusion

**Appcraft** provides a streamlined approach to application development, allowing you to focus on building features while managing your projects efficiently. Happy coding!

--- 
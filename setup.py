from setuptools import setup, find_packages
import toml

with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

project = pyproject.get("project", {})

project["url"] = "https://github.com/duxtec/appcraft"

project["package_data"] = {
    'appcraft': [
        'templates/**/*',
        'scripts/**/*',
        'utils/**/*',
    ],
}


setup(
    url=project["url"],
    packages=find_packages(),
    package_data=project["package_data"],
    include_package_data=True,
)

import argparse
import os


class RunnerGenerator:
    DEFAULT_APP_NAME = "MyApp"
    DEFAULT_RUNNER_COUNT = 1
    DEFAULT_NON_RUNNER_COUNT = 1

    TEMPLATE = """\
from infrastructure.framework.appcraft.core.runner import Runner


class {app_name}(Runner):
    {runner_methods}

    {non_runner_methods}
    """

    DEFAULT_TARGET = "main"

    def __init__(
        self,
        app_name: str | None = None,
        runner_count: int | None = None,
        non_runner_count: int | None = None,
        target: str | None = None,
    ):
        self.app_name = app_name or self.DEFAULT_APP_NAME
        self.runner_count = runner_count or self.DEFAULT_RUNNER_COUNT
        self.non_runner_count = (
            non_runner_count or self.DEFAULT_NON_RUNNER_COUNT
        )
        self.target = target or self.DEFAULT_TARGET

    def generate_methods(self, method_type: str, count: int):
        methods: list[str] = []
        for i in range(1, count + 1):
            if method_type == "runner":
                methods.append(
                    f"""
    @Runner.runner
    def runner{i}(self):
        pass

"""
                )
            else:
                methods.append(
                    f"""
    def non_runner{i}(self):
        # This method does not show in the runner.
        pass

"""
                )
        return "\n".join(methods)

    def create_runner(self):
        runner_methods = self.generate_methods("runner", self.runner_count)
        non_runner_methods = self.generate_methods(
            "non-runner", self.non_runner_count
        )

        app_content = self.TEMPLATE.format(
            app_name=self.app_name,
            runner_methods=runner_methods,
            non_runner_methods=non_runner_methods,
        )

        app_directory = os.path.join("runners", self.target)
        if not os.path.exists(app_directory):
            os.makedirs(app_directory)
        app_file_path = self.get_unique_file_path(app_directory, self.app_name)

        with open(app_file_path, 'w') as f:
            f.write(app_content)

        print(
            f"\
Runner '{self.app_name}' created with {self.runner_count} runner(s) and \
{self.non_runner_count} non-runner(s) methods."
        )

    def get_unique_file_path(self, directory: str, base_name: str):
        index = 1
        file_name = f"{base_name.lower()}.py"
        file_path = os.path.join(directory, file_name)

        while os.path.exists(file_path):
            file_name = f"{base_name.lower()}{index}.py"
            file_path = os.path.join(directory, file_name)
            index += 1

        return file_path


def create_runner():
    parser = argparse.ArgumentParser(
        description="\
Create a new app with specified runner and non-runner methods."
    )
    parser.add_argument(
        "app_name",
        nargs="?",
        default=RunnerGenerator.DEFAULT_APP_NAME,
        help="Name of the app (default: MyApp).",
    )
    parser.add_argument(
        "-r",
        type=int,
        default=RunnerGenerator.DEFAULT_RUNNER_COUNT,
        help="Number of runner methods (default: 1).",
    )
    parser.add_argument(
        "-n",
        type=int,
        default=RunnerGenerator.DEFAULT_NON_RUNNER_COUNT,
        help="Number of non-runner methods (default: 1).",
    )
    parser.add_argument(
        "-t",
        "--target",
        choices=["main", "tools"],
        default=RunnerGenerator.DEFAULT_TARGET,
        help="\
Which runners folder to generate into, runners/main or runners/tools \
(default: main).",
    )

    args = parser.parse_args()

    app_gen = RunnerGenerator(
        app_name=args.app_name,
        runner_count=args.r,
        non_runner_count=args.n,
        target=args.target,
    )

    app_gen.create_runner()


if __name__ == "__main__":
    create_runner()

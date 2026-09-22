from infrastructure.docker.adapter import DockerAdapter
from infrastructure.docker.compose_generator import generate_compose_file
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.framework.appcraft.utils.printer import Printer


class Docker(Runner):
    def __init__(self) -> None:
        self.adapter = DockerAdapter()

    @Runner.runner
    def generate_compose(self):
        services = generate_compose_file()

        if not services:
            Printer.warning(
                "No runners/main Runner with a `start` action was found — "
                "wrote an empty docker-compose.yml."
            )
            return

        Printer.success(
            f"docker-compose.yml regenerated with {len(services)} "
            "service(s):"
        )
        for module_name, class_name in services:
            print(f"  - {module_name} ({class_name}.start)")

    @Runner.runner
    def build(self, service: str | None = None):
        self.adapter.build(service)

    @Runner.runner
    def up(self, service: str | None = None):
        self.adapter.up(service)

    @Runner.runner
    def down(self):
        self.adapter.down()

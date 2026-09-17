from domain.models.programmer import Programmer
from infrastructure.database.mongodb.adapter import get_mongodb_adapter
from infrastructure.database.mongodb.seeder import ProgrammerSeeder
from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.framework.appcraft.utils.printer import Printer


class Programmers(Runner):
    @Runner.runner
    def seed(self):
        ProgrammerSeeder(get_mongodb_adapter()).seed()
        Printer.success("Programmers collection seeded!")
        self.list()

    @Runner.runner
    def list(self):
        adapter = get_mongodb_adapter()
        programmers = adapter.get(Programmer)

        if not programmers:
            Printer.warning("\
No programmers seeded yet — run the 'seed' method first.")
            return

        for programmer in programmers:
            Printer.title(programmer.name, end=": ")
            print(programmer.country)
            Printer.info("Technologies", end=": ")
            print(", ".join(programmer.technologies))
            Printer.info("Main projects", end=": ")
            print(", ".join(programmer.main_projects))
            print(programmer.bio)
            print("")

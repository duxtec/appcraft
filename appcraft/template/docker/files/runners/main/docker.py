from infrastructure.framework.appcraft.core.app_runner import AppRunner


class Docker(AppRunner):
    @AppRunner.runner
    def build(self):
        pass

    @AppRunner.runner
    def start(self):
        pass

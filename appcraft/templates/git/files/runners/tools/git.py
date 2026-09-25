from infrastructure.framework.appcraft.core.runner import Runner
from infrastructure.git.adapter import GitAdapter


class GitRunner(Runner):
    def __init__(self) -> None:
        self.adapter = GitAdapter()

    @Runner.runner
    def init(self):
        self.adapter.init_local_repo()
        version = "0.0.1"
        dev = version + "-dev"
        alpha = version + "-alpha"
        beta = version + "-beta"
        main = version
        self.adapter.create_branch(dev)
        self.adapter.create_branch(alpha, dev)
        self.adapter.create_branch(beta, alpha)
        self.adapter.create_branch(main, beta)

    def set_remote_repo(self, repo_url: str):
        self.adapter.remote_repo = repo_url

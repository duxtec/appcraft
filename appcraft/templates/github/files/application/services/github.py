from typing import List

from application.services.interfaces import ServiceAdapterInterface
from domain.filters import EqualFilter
from domain.filters.interface import FilterInterface
from domain.github.models.repository import GitHubRepository
from infrastructure.github.adapter import GitHubAdapter


class GitHubRepositoryService(ServiceAdapterInterface):
    def __init__(self, adapter: GitHubAdapter):
        self.adapter = adapter

    def get(
        self, filters: List[FilterInterface] = []
    ) -> List[GitHubRepository]:
        return self.adapter.get_repository(filters)

    def create(
        self, name: str, description: str, is_private: bool
    ) -> GitHubRepository:
        return self.adapter.create_repository(
            repo_name=name, is_private=is_private
        )

    def update(
        self, name: str, repository: GitHubRepository
    ) -> GitHubRepository:
        return repository

    def delete(self, name: str) -> None:
        repository = self.adapter.get_repository(
            [EqualFilter(GitHubRepository.name, name)]
        )[0]
        self.adapter.delete_repository(repository)

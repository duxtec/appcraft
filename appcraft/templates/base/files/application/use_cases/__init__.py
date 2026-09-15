from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from domain.filters.interface import FilterInterface

TInput = TypeVar("TInput", contravariant=True)
TOutput = TypeVar("TOutput", covariant=True)
TEntity = TypeVar("TEntity", covariant=True)
TFilter = TypeVar("TFilter", contravariant=True)
TId = TypeVar("TId", contravariant=True)
TCreateInput = TypeVar("TCreateInput", contravariant=True)
TUpdateInput = TypeVar("TUpdateInput", contravariant=True)


class UseCase(ABC, Generic[TInput, TOutput]):
    @abstractmethod
    def execute(self, input_data: TInput) -> TOutput: ...


class ReadUseCase(
    UseCase[Sequence[FilterInterface], Sequence[TEntity]],
    ABC,
):
    """Receives a sequence of filters and returns a list of entities."""

    @abstractmethod
    def execute(
        self, input_data: Sequence[FilterInterface]
    ) -> list[TEntity]: ...


class ReadOneUseCase(
    UseCase[TId, TEntity],
    ABC,
):
    """Receives an id and returns the corresponding entity."""

    @abstractmethod
    def execute(self, input_data: TId) -> TEntity: ...


class CreateUseCase(
    UseCase[TCreateInput, TEntity],
    ABC,
):
    """Receives the creation data and returns the created entity."""

    @abstractmethod
    def execute(self, input_data: TCreateInput) -> TEntity: ...


class DeleteUseCase(UseCase[TInput, None], ABC):
    """Receives filters to locate and delete the matching entities."""

    @abstractmethod
    def execute(self, input_data: TInput) -> None: ...


class UpdateUseCase(
    UseCase[TUpdateInput, TEntity],
    ABC,
):
    """Receives the update data (id + fields) and returns the entity."""

    @abstractmethod
    def execute(self, input_data: TUpdateInput) -> TEntity: ...

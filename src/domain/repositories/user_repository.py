from domain.entities.user import User, UserRole
from domain.repositories.base_repository import BaseRepository


class IUserRepository(BaseRepository[User]):

    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    def get_by_role(self, role: UserRole) -> list[User]:
        raise NotImplementedError

    def get_children_ids(self, parent_id: int) -> list[int]:
        raise NotImplementedError

    def is_parent_of(self, parent_id: int, child_id: int | str) -> bool:
        raise NotImplementedError

    def create_parent_child_relationship(self, parent_id: int, child_id: int, relationship: str = 'parent') -> bool:
        raise NotImplementedError

    def remove_parent_child_relationship(self, parent_id: int, child_id: int) -> bool:
        raise NotImplementedError

from domain.entities.user import User, UserRole
from domain.entities.student import Student
from domain.repositories.user_repository import IUserRepository
from domain.repositories.student_repository import IStudentRepository


class AuthService:

    def __init__(self, user_repo: IUserRepository, student_repo: IStudentRepository):
        self.user_repo = user_repo
        self.student_repo = student_repo

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.user_repo.get_by_username(username)
        if user and user.is_active and user.check_password(password):
            return user
        return None

    def register_user(self, username: str, email: str, password: str,
                      first_name: str, last_name: str, role: UserRole) -> tuple[User | None, str | None]:
        # Проверяем, что пользователь с таким username или email не существует
        if self.user_repo.get_by_username(username):
            return None, "Пользователь с таким именем уже существует"

        if self.user_repo.get_by_email(email):
            return None, "Пользователь с таким email уже существует"

        # Создаем нового пользователя
        user = User(
            id=None,
            username=username,
            email=email,
            password_hash="",  # Будет установлен через set_password
            role=role,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        user.set_password(password)

        try:
            user = self.user_repo.create(user)
            return user, None
        except Exception as e:
            return None, f"Ошибка при создании пользователя: {str(e)}"

    def can_view_student_data(self, user: User, student_id: int) -> bool:
        if not user or not user.is_active:
            return False

        if user.is_admin():
            return True

        if user.is_student():
            # Школьник может видеть только свои данные
            student = self.student_repo.get_by_user_id(user.id)
            return student and student.id == student_id

        if user.is_parent():
            # Родитель может видеть данные своих детей
            return True  # DEBUG
            # return self.user_repo.is_parent_of(user.id, student_id)

        if user.is_teacher():
            # Учитель может видеть всех учеников
            return True

        return False

    def can_edit_student_data(self, user: User, student_id: int) -> bool:
        if not user or not user.is_active:
            return False

        if user.is_admin():
            return True

        if user.is_teacher():
            # Учитель может редактировать данные учеников
            return True

        return False

    def get_user_students(self, user: User) -> list[Student]:
        if not user or not user.is_active:
            return []

        if user.is_admin():
            # Админ видит всех студентов
            return self.student_repo.get_all()

        if user.is_student():
            # Школьник видит только себя
            student = self.student_repo.get_by_user_id(user.id)
            return [student] if student else []

        if user.is_parent():
            # Родитель видит своих детей
            children_ids = self.user_repo.get_children_ids(user.id)
            if children_ids:
                return []
            return [self.student_repo.get_by_id(child_id) for child_id in children_ids]

        if user.is_teacher():
            # Учитель видит всех студентов
            return self.student_repo.get_all()

        return []

    def manage_parent_child_relationship(self, action: str, parent_id: int, child_id: int, admin_user: User = None) -> \
        tuple[bool, str]:
        if not admin_user or not admin_user.is_admin():
            return False, "Только администратор может управлять связями"

        if action == 'create':
            if self.user_repo.is_parent_of(parent_id, child_id):
                return False, "Связь уже существует"
            if not self.user_repo.get_by_id(parent_id) or not self.student_repo.get_by_id(child_id):
                return False, "Родитель или ребенок не найден"
            return self.user_repo.create_parent_child_relationship(parent_id, child_id), "Связь создана"

        elif action == 'remove':
            return self.user_repo.remove_parent_child_relationship(parent_id, child_id), "Связь удалена"

        return False, "Неизвестное действие"

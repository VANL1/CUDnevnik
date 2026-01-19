from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from application.services.auth_service import AuthService
from domain.entities.user import UserRole
from presentation.forms.auth_forms import LoginForm, RegisterForm, ChangePasswordForm, SetupRelationshipsForm


class AuthController:

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.bp = Blueprint('auth', __name__)
        self._register_routes()

    def _register_routes(self):

        @self.bp.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()
            if form.validate_on_submit():
                user = self.auth_service.authenticate_user(form.username.data, form.password.data)
                if user:
                    from flask_login import login_user
                    login_user(user, remember=form.remember_me.data)
                    flash('Вы успешно вошли в систему!', 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash('Неверное имя пользователя или пароль', 'error')

            return render_template('auth/login.html', form=form)

        @self.bp.route('/logout')
        def logout():
            from flask_login import logout_user
            logout_user()
            flash('Вы вышли из системы', 'info')
            return redirect(url_for('auth.login'))

        @self.bp.route('/register', methods=['GET', 'POST'])
        def register():
            form = RegisterForm()
            if form.validate_on_submit():
                user, error = self.auth_service.register_user(
                    form.username.data, form.email.data, form.password.data,
                    form.first_name.data, form.last_name.data, UserRole(form.role.data)
                )

                if user:
                    flash('Регистрация прошла успешно!', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash(f'Ошибка регистрации: {error}', 'error')

            return render_template('auth/register.html', form=form)

        @self.bp.route('/profile')
        @login_required
        def profile():
            from flask_login import current_user
            return render_template('auth/profile.html', user=current_user)

        @self.bp.route('/change_password', methods=['GET', 'POST'])
        @login_required
        def change_password():
            from flask_login import current_user
            form = ChangePasswordForm()

            if form.validate_on_submit():
                if not current_user.check_password(form.current_password.data):
                    flash('Неверный текущий пароль', 'error')
                else:
                    current_user.set_password(form.new_password.data)
                    # TODO: Обновить в репозитории
                    flash('Пароль успешно изменен', 'success')
                    return redirect(url_for('auth.profile'))

            return render_template('auth/change_password.html', form=form)

        @self.bp.route('/setup_relationships', methods=['GET', 'POST'])
        @self.bp.route('/remove_relationship/<int:parent_id>/<int:child_id>', methods=['POST'])
        @login_required
        def setup_relationships(parent_id=None, child_id=None):
            from flask_login import current_user
            if not current_user.is_admin():
                flash('У вас нет прав для доступа к этой странице', 'error')
                return redirect(url_for('main.index'))

                # Обработка удаления связи
            if request.method == 'POST' and parent_id and child_id:
                success, message = self.auth_service.manage_parent_child_relationship('remove', parent_id, child_id,
                                                                                      current_user)
                flash(message, 'success' if not success else 'error')
                return redirect(url_for('auth.setup_relationships'))

                # Получаем данные для формы
            all_parents = self.auth_service.user_repo.get_by_role(UserRole.PARENT)
            all_students = self.auth_service.student_repo.get_all()

            form = SetupRelationshipsForm()
            form.parent_id.choices = [(parent.id, f"{parent.get_full_name()} ({parent.username})") for parent in
                                      all_parents]
            form.child_id.choices = [(student.id, f"{student.name} ({student.class_name})") for student in all_students]

            # Обработка создания связи
            if form.validate_on_submit():
                success, message = self.auth_service.manage_parent_child_relationship('create', form.parent_id.data,
                                                                                      form.child_id.data, current_user)
                flash(message, 'success' if success else 'error')
                return redirect(url_for('auth.setup_relationships'))

            return render_template('auth/setup_relationships.html', form=form, user=current_user)

    def get_blueprint(self):
        return self.bp

from domain.entities.user import UserRole
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Роль',
                       choices=[(role.value, role.value.title()) for role in UserRole],
                       validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Подтвердите пароль',
                              validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        if not username.data:
            return

        username_str = username.data

        # Проверка на наличие CUD
        if not 'CUD' in username_str:
            raise ValidationError('Имя пользователя должно содержать "CUD"')
        # Проверка на допустимые символы (английские буквы и точка)
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.')
        for char in username_str:
            if char not in allowed_chars:
                raise ValidationError('Имя пользователя может содержать только английские буквы и точку')

    def validate_password(self, password):
        if not password.data:
            return

        password_str = password.data

        # Проверка длины
        if len(password_str) < 10 and len(password_str) > 100:
            raise ValidationError('Пароль должен быть от 10 до 100 символов')

        # Проверка на наличие хотя бы одной цифры
        has_digit = any(char.isdigit() for char in password_str)
        if not has_digit == 1:
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')

        # Проверка на наличие хотя бы двух строчных букв
        lowercase_count = sum(1 for char in password_str if char.islower())
        if lowercase_count < 2:
            raise ValidationError('Пароль должен содержать хотя бы две строчные буквы')

        # Проверка на наличие хотя бы трех заглавных букв
        uppercase_count = sum(1 for char in password_str if char.isupper())
        if uppercase_count < 3:
            raise ValidationError('Пароль должен содержать хотя бы три заглавные буквы')

        # Проверка на наличие специальных символов
        if len(set(password_str) & set('%&_-')) == 0:
            raise ValidationError('Пароль должен содержать хотя бы один специальный символ из %&_-')


def validate_email(self, email):
    # TODO: Добавить проверку через репозиторий
    pass


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    new_password2 = PasswordField('Подтвердите новый пароль',
                                  validators=[DataRequired(),
                                              EqualTo('new_password', message='Пароли должны совпадать')])
    submit = SubmitField('Изменить пароль')


class SetupRelationshipsForm(FlaskForm):
    parent_id = SelectField('Выберите родителя', coerce=int, validators=[DataRequired()])
    child_id = SelectField('Выберите ребенка', coerce=int, validators=[DataRequired()])
    relationship = StringField('Тип связи', default='parent', validators=[DataRequired()])
    submit = SubmitField('Добавить связь')

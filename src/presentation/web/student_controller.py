from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import time
from application.services.student_service import StudentService


class StudentController:

    def __init__(self, student_service: StudentService):
        self.student_service = student_service
        self.bp = Blueprint('students', __name__)
        self._register_routes()

    def _register_routes(self):

        @self.bp.route('/<int:student_id>')
        @login_required
        def student_diary(student_id):
            from flask_login import current_user

            data = self.student_service.get_student_diary_data(student_id, current_user)
            if data is None:
                flash('У вас нет прав для просмотра данных этого студента', 'error')
                return redirect(url_for('main.index'))

                # Обработка фильтров для расписания
            if request.args.get('tab') == 'schedule':
                day_filter = request.args.get('day')
                subject_filter = request.args.get('subject')
                time_start_filter = request.args.get('time_start')

                # Парсим фильтры
                subject_id = int(subject_filter) if subject_filter and subject_filter.isdigit() else None
                day_of_week = int(day_filter) if day_filter and day_filter.isdigit() else None
                time_start = time.fromisoformat(time_start_filter) if time_start_filter else None

                # Получаем отфильтрованное расписание
                if any([day_of_week, subject_id, time_start]):
                    data['schedule'] = self.student_service.get_filtered_schedule(
                        subject_id, day_of_week, time_start
                    )
            return render_template('student_diary.html', **data)

        @self.bp.route('/<int:student_id>/add_grade', methods=['POST'])
        @login_required
        def add_grade(student_id):
            from flask_login import current_user

            subject_id = request.form['subject_id']
            grade = request.form['grade']
            comment = request.form.get('comment', '')

            result = self.student_service.add_grade(student_id, int(subject_id), int(grade), comment, current_user)
            if result:
                flash('Оценка добавлена успешно!', 'success')
            else:
                flash('У вас нет прав для добавления оценок', 'error')
            return redirect(url_for('students.student_diary', student_id=student_id))

        @self.bp.route('/<int:student_id>/add_attendance', methods=['POST'])
        @login_required
        def add_attendance(student_id):
            from flask_login import current_user

            subject_id = request.form['subject_id']
            present = 'present' in request.form
            reason = request.form.get('reason', '')

            result = self.student_service.add_attendance(student_id, int(subject_id), present, reason, current_user)
            if result:
                flash('Посещаемость отмечена!', 'success')
            else:
                flash('У вас нет прав для отметки посещаемости', 'error')
            return redirect(url_for('students.student_diary', student_id=student_id))

    def get_blueprint(self):
        return self.bp

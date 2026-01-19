from domain.entities.schedule import Schedule
from domain.repositories.base_repository import BaseRepository
from datetime import time


class IScheduleRepository(BaseRepository[Schedule]):

    def get_by_day(self, day_of_week: int) -> list[Schedule]:
        raise NotImplementedError

    def get_by_subject(self, subject_id: int) -> list[Schedule]:
        raise NotImplementedError

    def get_filtered(self, day_of_week: int = None, subject_id: int = None,
                     time_start: time = None) -> list[Schedule]:
        raise NotImplementedError

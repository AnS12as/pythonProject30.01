from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


def create_periodic_task():
    """
    Создаёт периодическую задачу для проверки и блокировки неактивных пользователей.
    """
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Deactivate inactive users",
        task="lms.tasks.deactivate_inactive_users",
        defaults={
            "args": json.dumps([]),
        },
    )


def setup_periodic_tasks(sender, **kwargs):
    create_periodic_task()


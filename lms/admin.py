from django_celery_beat.models import PeriodicTask, IntervalSchedule

schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)


def create_periodic_task():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='My Periodic Task',
        task='my_app.tasks.my_task',
    )


def setup_periodic_tasks():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Sample Celery Task",
        task="lms.tasks.sample_task",
    )

from celery.schedules import crontab


from tasks.models import STATUS_CHOICES, Task, TaskEmail


from django.core.mail import send_mail
from task_manager.celery import app

from django.contrib.auth.models import User


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for user in User.objects.all():
        obj, _ = TaskEmail.objects.get_or_create(user=user)

    #     sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )
        sender.add_periodic_task(
            crontab(hour=obj.mail_time),
            task_mail.s(user.id),
        )


@app.task
# def test(arg):
#     print(arg)
def task_mail(user):
    subject = f"{user}'s Report"
    content = "***************** Your tasks report **********:\n\n"
    email = "tasks@taskmanager.org",
    sendingto_email = user.email
    for choice in STATUS_CHOICES:
        pending_qs = Task.objects.filter(
            user=user, status=choice[0], deleted=False)
        content += f"-Task Status:{choice[0]}:\n\n Task count:{pending_qs.count}\n"

    send_mail(
        subject,
        content,
        email,
        sendingto_email,
        fail_silently=False,
    )

    print(f"{user} email sent!!")

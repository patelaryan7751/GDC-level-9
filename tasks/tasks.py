from celery.decorators import periodic_task
from datetime import datetime, timedelta

from tasks.models import STATUS_CHOICES, Task, TaskEmail


from django.core.mail import send_mail
from task_manager.celery import app

from django.contrib.auth.models import User


@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    now = datetime.now().hour
    if TaskEmail.objects.filter(mail_time=now):
        for userReport in TaskEmail.objects.filter(mail_time=now):
            user = User.objects.get(id=userReport.user.id)

            # Create content and subject
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

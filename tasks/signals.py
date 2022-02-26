from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from tasks.models import Task, TaskEmail, TaskHistory, User


@receiver(post_save, sender=User)
def mailSchedule(sender, instance, created, **kwargs):
    if created:
        TaskEmail.objects.create(user=instance)


@receiver(pre_save, sender=Task)
def taskhistory_Update(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        current = instance
        previous = Task.objects.get(id=instance.id)
        if previous.status != current.status:
            print("old task: ", previous.status)
            print("current:", current.status)
            TaskHistory.objects.create(
                task=instance, old_status=previous.status, new_status=current.status)

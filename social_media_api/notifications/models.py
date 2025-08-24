from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications_sent')
    verb = models.CharField(max_length=255)  # e.g. "liked", "followed"
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.actor.username} {self.verb}"






# class Notification(models.Model):
#     recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
#     actor = models.ForeignKey(User, related_name='actor_notifications', on_delete=models.CASCADE)
#     verb = models.CharField(max_length=255)  # e.g., 'liked', 'followed', etc.
#     target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
#     target_object_id = models.PositiveIntegerField(null=True, blank=True)
#     target = GenericForeignKey('target_content_type', 'target_object_id')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.actor} {self.verb} {self.target}'

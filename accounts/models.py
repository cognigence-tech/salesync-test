from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Application(models.Model):
  SENDER = 'sender'
  RECEIVER = 'receiver'

  ROLE_CHOICES = [
      (SENDER, 'Sender'),
      (RECEIVER, 'Receiver'),
  ]

  app_name = models.CharField(max_length=255, unique=True)
  role = models.CharField(max_length=8, choices=ROLE_CHOICES, default=SENDER)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.app_name


class Connection(models.Model):
  sender = models.ForeignKey(Application,
                             on_delete=models.CASCADE,
                             related_name='sent_connections',
                             limit_choices_to={'role': Application.SENDER})
  receiver = models.ForeignKey(Application,
                               on_delete=models.CASCADE,
                               related_name='received_connections',
                               limit_choices_to={'role': Application.RECEIVER})
  user = models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name='connections')  # Associate with a user
  is_active = models.BooleanField(default=False)

  class Meta:
    unique_together = ('sender', 'receiver', 'user'
                       )  # Ensure uniqueness of connection per user

  def clean(self):
    # Custom validation to ensure both sender and receiver are active
    if not self.sender.is_active or not self.receiver.is_active:
      raise ValidationError(
          "Connection can only be active if both sender and receiver are active."
      )

  def save(self, *args, **kwargs):
    # Set is_active to True only if both sender and receiver are active
    self.is_active = self.sender.is_active and self.receiver.is_active
    super().save(*args, **kwargs)

  def __str__(self):
    return f"Connection from {self.sender.app_name} to {self.receiver.app_name} by {self.user.username}"

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
    # Add country choices (this can be expanded or linked with a package like `django-countries`)
    COUNTRY_CHOICES = [
        ('IN', 'India'),
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        # Add more countries as needed
    ]

    app_name = models.CharField(max_length=255)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default=SENDER)
    is_active = models.BooleanField(default=True)
    is_user_active = models.BooleanField(default=False)

    country = models.CharField(
        max_length=2,
        choices=COUNTRY_CHOICES,
    )

    class Meta:
        # Enforce the uniqueness of app_name and country combination
        constraints = [
            models.UniqueConstraint(fields=['app_name', 'country'],
                                    name='unique_app_name_country')
        ]

    def __str__(self):
        return f"{self.app_name} - {self.country}"


class Connection(models.Model):
    sender = models.ForeignKey(Application,
                               on_delete=models.CASCADE,
                               related_name='sent_connections',
                               limit_choices_to={'role': Application.SENDER})
    receiver = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='received_connections',
        limit_choices_to={'role': Application.RECEIVER})
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='connections')  # Associate with a user
    is_active = models.BooleanField(default=False)
    # Country should match between sender and receiver
    country = models.CharField(
        max_length=2, null=True,
        blank=True)  # Automatically set to sender's and receiver's country

    def clean(self):
        # Custom validation to ensure both sender and receiver are from the same country
        if self.sender.country != self.receiver.country:
            raise ValidationError(
                "Sender and receiver must be from the same country.")
        if not self.sender.is_active or not self.receiver.is_active:
            raise ValidationError(
                "Connection can only be active if both sender and receiver apps are globally active."
            )
        # Check if the sender and receiver are active for the user
        # if not self.sender.is_user_active or not self.receiver.is_user_active:
        #     raise ValidationError(
        #         "Connection can only be active if both sender and receiver are active for the user."
        #     )

    def save(self, *args, **kwargs):
        # Set country based on the sender's and receiver's country
        if self.sender.country == self.receiver.country:
            self.country = self.sender.country
        else:
            raise ValidationError(
                "Sender and receiver must be from the same country.")
        self.is_active = self.sender.is_active and self.receiver.is_active
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Connection {self.sender.app_name} to {self.receiver.app_name} - {self.country} - by {self.user.username}"

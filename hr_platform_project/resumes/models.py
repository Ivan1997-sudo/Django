from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="users")
    position = models.CharField(max_length=255)
    experience = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    #Не позволяет создать одному пользователю больше одного резюме на одну позицию
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'position'], name='unique user and position')
        ]

    def __str__(self):
        return f"{self.user} - {self.position}"
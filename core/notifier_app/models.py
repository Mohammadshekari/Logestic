from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.id}"

    class Meta:
        ordering = ['-created_date']
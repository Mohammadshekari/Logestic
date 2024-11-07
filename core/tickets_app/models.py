from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TicketPriorityType(models.IntegerChoices):
    normal = 1, "normal"
    urgent = 2, "urgent"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class TicketStatusType(models.IntegerChoices):
    opened = 1 , "new ticket"
    user_pending = 2, "pending for user answer"
    support_pending = 3, "pending for support answer"
    fixed = 4, "fixed"
    closed = 5, "closed"


class AttachmentModel(models.Model):
    file = models.FileField(upload_to="ticket/attachments/")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]


class TicketModel(models.Model):
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    attachments = models.ManyToManyField(AttachmentModel)
    priority = models.IntegerField(choices=TicketPriorityType.choices, default=TicketPriorityType.normal.value)
    status = models.IntegerField(choices=TicketStatusType.choices, default=TicketStatusType.opened.value)

    title = models.CharField(max_length=255)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
    def is_closed(self):
        return self.status in [TicketStatusType.closed.value ,TicketStatusType.fixed.value]
    
    def get_priority(self):
        return {
            "id": self.priority,
            "title": TicketPriorityType(self.priority).name,
            "label": TicketPriorityType(self.priority).label,
        }
    def get_status(self):
        return {
            "id": self.status,
            "title": TicketStatusType(self.status).name,
            "label": TicketStatusType(self.status).label,
        }
    



class TicketMessageModel(models.Model):
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name="user_answer")
    ticket = models.ForeignKey(TicketModel, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    attachments = models.ManyToManyField(AttachmentModel)
    description = models.TextField()

    is_support = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

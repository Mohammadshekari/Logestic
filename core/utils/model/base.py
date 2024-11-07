from django.db import models
from django.utils import timezone


class AccessType(models.IntegerChoices):
    """
    Access types for each item which user creates
    """

    Private = 0
    Public = 1


class BaseManager(models.Manager):
    def create(self, *args, **kwargs):
        # kwargs['created_by'] = kwargs.get('user_id')
        return super(BaseManager, self).create(**kwargs)


class BaseModel(models.Model):
    """
    Base Model for all objects which needs to have default attributes
    """

    is_deleted = models.BooleanField(
        default=False,
        help_text="indicates if the object has been deleted or not",
    )
    access = models.IntegerField(
        choices=AccessType.choices,
        default=AccessType.Public,
        help_text="indicates if this object is Public or not",
    )

    created_by = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="keeper of the user who created this object",
    )
    modified_by = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="keeper of the user who modified this object",
    )
    deleted_by = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="keeper of the user who deleted this object",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="time which this object was created"
    )
    modified_at = models.DateTimeField(
        auto_now=True, help_text="time which this object was modified"
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, help_text="time which this object was deleted"
    )
    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self, user_id=None):
        self.is_deleted = True
        self.deleted_by = user_id
        self.deleted_at = timezone.now()
        self.save()

    def create(self, user_id=None, *args, **kwargs):
        if not self.pk:
            self.modified_by = user_id
        super(BaseModel, self).save(*args, **kwargs)

    def soft_recycle(self, user_id=None):
        self.is_deleted = False
        self.deleted_by = None
        self.deleted_at = None
        self.modified_by = user_id
        self.save()

    def soft_change_access(self, user_id=None, access_type=None):
        self.access = access_type
        self.modified_by = user_id
        self.save()

    def save(self, force_insert=False, force_update=False, using=None):
        self.full_clean()
        super(BaseModel, self).save(force_insert, force_update, using)

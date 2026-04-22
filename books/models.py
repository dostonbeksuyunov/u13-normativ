from django.db import models


# 1. Custom QuerySet
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        # real delete emas, is_deleted=True qiladi.
        return super().update(is_deleted=True)


# 2. Custom Manager
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # faqat aktiv (o'chirilmagan) obyektlar
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete flag
    is_deleted = models.BooleanField(default=False)

    # Managerlar
    objects = SoftDeleteManager()   # faqat active
    all_objects = models.Manager()  # hammasi (kerak bo'lsa)

    def __str__(self):
        return self.title

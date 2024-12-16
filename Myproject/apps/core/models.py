from django.db import models
from django.utils import timezone

# Create your models here.
class BaseQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())


class PostManager(models.Manager):
    def get_queryset(self):
        # Filtre les posts qui ne sont pas supprimés
        return BaseQuerySet(model=self.model, using=self._db).filter(deleted_at=None)


class Post(models.Model):
    created_by = models.ForeignKey(
       "newsletters.CustomUser", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateField(null=True, auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)

    objects = PostManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()



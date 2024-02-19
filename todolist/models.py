from django.conf import settings
from django.db import models
import datetime


# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(default=datetime.date.today)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'({self.id}) {self.title}'
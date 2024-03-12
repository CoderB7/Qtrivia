from django.db import models
from account.models import CustomUser
from django.utils.text import slugify


class Sources(models.Model):
    name = models.CharField(max_length=250)
    types = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    slug = models.SlugField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Quiz(models.Model):
    source_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, blank=True)
    amount = models.IntegerField()
    category = models.CharField(max_length=250)
    difficulty = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    quiz_data = models.JSONField(max_length=700, default=dict)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user_answers = models.CharField(max_length=700, null=True)
    solved = models.DateField(null=True)
    user_score = models.IntegerField(null=True)
    user_mistakes = models.JSONField(max_length=700, default=dict)

    def __str__(self):
        return self.source_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.source_name)
        super().save(*args, **kwargs)


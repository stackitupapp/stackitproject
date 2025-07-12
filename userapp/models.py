from django.db import models
from ckeditor.fields import RichTextField

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    tags = models.ManyToManyField(Tag, related_name='questions')

    def __str__(self):  # <-- This was indented incorrectly and named wrong
        return self.title

from django.db import models

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.content[:50]

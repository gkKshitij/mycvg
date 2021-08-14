from django.db import models
from django.utils import timezone


# Create your models here.
class Student(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.title) + ' by ' + str(self.author)


class Comment(models.Model):
    student = models.ForeignKey('cvg.Student', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text
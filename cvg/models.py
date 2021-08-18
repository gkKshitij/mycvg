from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

genders= (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Bisesual','Bisesual'),
    ('None','None'),
)

years= [tuple([x,x]) for x in range(2017,2067)]

months=(
    ('January','January'),
    ('Feburary', 'Feburary'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December'),
)


# Create your models here.
class Cv(models.Model):
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    edited_by=models.CharField(max_length=11, blank=True)

    sap_id=models.IntegerField()
    first_name=models.CharField(max_length=20 )
    last_name=models.CharField(max_length=20 )
    keywords=models.CharField(max_length=100 ,blank=True)
    mobile_number=models.IntegerField()
    college_email_id=models.CharField(max_length=30 )
    personal_email_id=models.CharField(max_length=30 )
    git_profile_url=models.URLField(max_length=50 ,blank=True)
    linkedin_profile_url=models.URLField(max_length=50 ,blank=True)
    address=models.TextField(max_length=100 )
    age=models.IntegerField()
    gender=models.CharField(max_length=10, choices=genders, default='None')
    published_date = models.DateTimeField(blank=True, null=True)

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.sap_id)


class Comment(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

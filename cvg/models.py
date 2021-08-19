
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Bisexual', 'Bisexual'),
    ('None', 'None'),
)

years = [tuple([x, x]) for x in range(2017, 2067)]

months = (
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
)


# Create your models here.
class Cv(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    edited_by = models.CharField(max_length=11, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    sap_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    keywords = models.CharField(max_length=100, blank=True)
    mobile_number = models.IntegerField()
    college_email_id = models.CharField(max_length=30)
    personal_email_id = models.CharField(max_length=30)
    git_profile_url = models.URLField(max_length=50, blank=True)
    linkedin_profile_url = models.URLField(max_length=50, blank=True)
    address = models.TextField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=genders, default='None')

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.sap_id)


class Academics(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='academics')
    admission_year = models.IntegerField(choices=years)
    graduation_year = models.IntegerField(choices=years)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[MaxValueValidator(4), MinValueValidator(2)])
    tenth_percentile = models.DecimalField(max_digits=4, decimal_places=2)
    twelfth_percentile = models.DecimalField(max_digits=4, decimal_places=2)

    approved = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=timezone.now)
    edited_by = models.CharField(max_length=11, blank=True)

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def unapprove(self):
        self.approved = False
        self.save()

    def __str__(self):
        return str(self.cv)


class Skills(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='skills')
    programming_languages = models.TextField(max_length=100)
    tools_familiar_with = models.TextField(max_length=100)
    core_skills = models.TextField(max_length=100)

    approved = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=timezone.now)
    edited_by = models.CharField(max_length=11, blank=True)

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def unapprove(self):
        self.approved = False
        self.save()

    def __str__(self):
        return str(self.cv)


class Extracurricular(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='extracurricular')
    hobbies = models.TextField(max_length=50)
    certificates = models.TextField(max_length=100)

    approved = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=timezone.now)
    edited_by = models.CharField(max_length=11, blank=True)

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def unapprove(self):
        self.approved = False
        self.save()

    def __str__(self):
        return str(self.cv)


class Internships(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='internships')
    organization = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    start_month = models.CharField(max_length=10, choices=months, default='January')
    start_year = models.IntegerField(choices=years, blank=True, null=True)
    end_month = models.CharField(max_length=10, choices=months, default='January')
    end_year = models.IntegerField(choices=years, blank=True, null=True)
    description = models.TextField(max_length=200)

    approved = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=timezone.now)
    edited_by = models.CharField(max_length=11, blank=True, null=True)

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def unapprove(self):
        self.approved = False
        self.save()

    def __str__(self):
        return str(self.cv)


class Projects(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='projects')
    name = models.TextField(max_length=100)
    tools_and_tech = models.TextField(max_length=100)
    start_month = models.CharField(max_length=10, choices=months, default='January')
    start_year = models.IntegerField(choices=years, blank=True, null=True)
    end_month = models.CharField(max_length=10, choices=months, default='January')
    end_year = models.IntegerField(choices=years, blank=True, null=True)
    description = models.TextField(max_length=200)

    approved = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=timezone.now)
    edited_by = models.CharField(max_length=11, blank=True, null=True)

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def unapprove(self):
        self.approved = False
        self.save()

    def __str__(self):
        return str(self.cv)


class Roles(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='roles')
    organization = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    start_month = models.CharField(max_length=10, choices=months, default='January')
    start_year = models.IntegerField(choices=years, blank=True, null=True)
    end_month = models.CharField(max_length=10, choices=months, default='January')
    end_year = models.IntegerField(choices=years, blank=True, null=True)
    description = models.TextField(max_length=200)

    approved = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=timezone.now)
    edited_by = models.CharField(max_length=11, blank=True)

    def modified(self):
        self.modified_date = timezone.now()
        self.save()

    def unapprove(self):
        self.approved = False
        self.save()

    def __str__(self):
        return str(self.cv)


# to be discarded safely
class Comment(models.Model):
    cv = models.ForeignKey('cvg.Cv', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    # edited_by = models.CharField(max_length=11, blank=True)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

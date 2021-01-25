from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User


class Bird(models.Model):
    bird_id = models.AutoField(primary_key=True)
    bird_type = models.CharField(max_length=30)
    bird_name = models.CharField(max_length=30)
    bird_gender = models.CharField(max_length=10)
    bird_color = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Bird'

    def __str__(self):
        return self.bird_name

class Images(models.Model):
    title = models.CharField(max_length=50)
    document = models.ImageField(upload_to='images')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Images'

    def __str__(self):
        return self.title


class Videos(models.Model):
    title = models.CharField(max_length=50)
    video_file = models.FileField(upload_to='videos')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Videos'

    def __str__(self):
        return self.title


class Cage(models.Model):
    cage_num = models.AutoField(primary_key=True)
    bird_id = models.ForeignKey(Bird, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Cage'

    def __int__(self):
        return self.cage_num


class Breeding(models.Model):
    bird_id = models.ForeignKey(Bird, on_delete=models.CASCADE, default=1)
    cage_num = models.ForeignKey(Cage, on_delete=models.CASCADE, default=1)
    breeding_date = models.DateTimeField()
    hatch_date = models.DateTimeField()

    class Meta:
        db_table = 'Breeding'

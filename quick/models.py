from django.contrib.auth.models import User

from django.db import models


class Interest(models.Model):
    INTERESTS = (
        ('CAR', 'Cars'),
        ('MUSIC', 'Music'),
        ('TECHNOLOGY', 'Technology'),
        ('HIKING', 'Hiking'),
        ('BIKING', 'Biking'),
        ("TRAIL", 'Trail'),
        ('COMEDY', 'Comedy'),
        ('FOOD', 'Food'),
        ('SPORTS', 'Sports'),)
    interests = models.CharField(max_length=10, choices=INTERESTS, null=True, blank=True)


    def __unicode__(self):
        return self.interests


class Profile(models.Model):
    oauth_token = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name="profile")
    zipcode = models.IntegerField(max_length=5, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    interests = models.ManyToManyField(Interest, null=True, blank=True)


    def __unicode__(self):
        return self.email


class Event(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    INTERESTS = (
        ('CAR', 'Cars'),
        ('MUSIC', 'Music'),
        ('TECHNOLOGY', 'Technology'),
        ('HIKING', 'Hiking'),
        ('BIKING', 'Biking'),
        ("TRAIL", 'Trail'),
        ('COMEDY', 'Comedy'),
        ('FOOD', 'Food'),
        ('SPORTS', 'Sports'),)
    category = models.CharField(max_length=10, choices=INTERESTS, null=True, blank=True)
    venue = models.CharField(null=True, blank=True, max_length=200)
    description = models.TextField(max_length=8000, null=True, blank=True)
    latitude = models.FloatField(max_length=100, null=True, blank=True)
    longitude = models.FloatField(max_length=100, null=True, blank=True)
    start_time = models.CharField(max_length=50, null=True, blank=True)
    end_time = models.CharField(max_length=50, null=True, blank=True)
    picture = models.URLField(null=True, blank=True)
    event_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    start_dateTime = models.DateTimeField(null=True, blank=True)
    end_dateTime = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class FreeTimes(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    free_time_start = models.CharField(max_length=50, null=True, blank=True)
    free_time_end = models.CharField(max_length=50, null=True, blank=True)
    free_time_amount = models.CharField(max_length=50, null=True, blank=True)
    previous_event = models.CharField(max_length=200, null=True, blank=True)
    free_start_dateTime = models.DateTimeField(null=True, blank=True)
    free_end_dateTime = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "Free from {} to {}".format(self.free_time_start, self.free_time_end)


class Friend(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.CharField(max_length=6000, null=True, blank=True)

    def __unicode__(self):
        return "{} friends {}".format(self.user, self.email)




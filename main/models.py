from django.db import models

class Entry(models.Model):
    time = models.DateTimeField()
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        formated_time = self.time.strftime("%d/%m/%Y | %H:%M")
        return f"{formated_time} - {self.title}"


class APIData(models.Model):
    accessToken = models.CharField(max_length=255)
    accessTokenExpireDate = models.DateTimeField()
    subscriptionID = models.CharField(max_length=255, default="0")
    verificationSecret = models.CharField(max_length=255, default="0")


class EntryFilter(models.Model):
    name = models.CharField(max_length=255)
    entryIDs = models.JSONField(default=list)
    lastChanged = models.DateTimeField()

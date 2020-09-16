from django.db import models

class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField()
    projector = models.BooleanField(default=False)


class Reservation(models.Model):
    date = models.DateTimeField(unique=True)
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    comment = models.TextField()


class Meta:
    unique_together = ("date", "name")
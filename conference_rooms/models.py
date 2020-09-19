from django.db import models


class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField()
    projector = models.BooleanField(default=False)


class Reservation(models.Model):
    class Meta:
        ordering = ["date"]

    date = models.DateField()
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    comment = models.TextField()


class Meta:
    unique_together = ("room_id", "name")

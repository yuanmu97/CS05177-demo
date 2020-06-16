from uuid import uuid4

from django.db import models
from django.shortcuts import resolve_url


def uuid_name(instance=None, filename=None):
    return str(uuid4())


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    file = models.FileField(upload_to=uuid_name)
    scanned = models.BooleanField(default=False)
    corrected = models.FileField(upload_to=uuid_name)

    def get_absolute_url(self):
        return resolve_url('image', id=self.id)

    def json(self):
        return {
            'id': self.id,
            'file': self.file.url,
            'scanned': self.scanned,
            'corrected': self.corrected.url if self.corrected else None,
            'rects': [r.json() for r in self.rect_set.all()],
        }


class Rect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image = models.ForeignKey(Image, models.PROTECT)
    type = models.TextField()
    description = models.TextField()
    top = models.IntegerField()
    left = models.IntegerField()
    right = models.IntegerField()
    bottom = models.IntegerField()
    level = models.IntegerField()
    level_corrected = models.IntegerField(null=True, blank=True)

    def json(self):
        return {
            'id': self.id,
            'type': self.type,
            'description': self.description,
            'top': self.top,
            'left': self.left,
            'right': self.right,
            'bottom': self.bottom,
            'level': self.level,
            'level_corrected': self.level_corrected,
        }

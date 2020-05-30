from django.contrib import admin

from demo.models import Image, Rect

admin.site.register((Image, Rect))

from django.contrib import admin

from .models import Bird, Cage, Images, Videos

admin.site.register(Bird)
admin.site.register(Cage)
admin.site.register(Images)
admin.site.register(Videos)
# Register your models here.

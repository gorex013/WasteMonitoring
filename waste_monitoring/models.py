from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models


class WasteType(models.IntegerChoices):
    MIXT = 0, 'Mixt'
    PLASTIC = 1, 'Platic'
    STICLA_METAL = 2, 'Sticlă/metal'
    BIO = 3, 'Biodegradabile'


class WasteData(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=1.0)
    waste_type = models.IntegerField(WasteType.choices)
    date_of_count = models.DateField(default=date.today)
    register_time = models.DateTimeField(default=datetime.now)

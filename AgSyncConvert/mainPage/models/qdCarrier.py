from django.db import models
from django.contrib.auth.models import User
from .qdWorkOrder import QDWorkOrder


class QDCarrier(models.Model):

    Name = models.CharField(max_length=50, null=True, blank=True)
    EPAID = models.CharField(max_length=50, null=True, blank=True)
    Rate = models.IntegerField(default=0)
    LoadOrder = models.IntegerField(default=0)
    WorkOrder = models.ForeignKey(QDWorkOrder, null=True, blank=True, related_name="Carriers", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "qdCarriers"

    def __str__(self):
        return "Carrier: {}".format(self.Name)

    def create(self, **obj_data):
        return super().create(**obj_data)


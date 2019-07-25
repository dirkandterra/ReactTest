from django.db import models
from django.contrib.auth.models import User
from .qdWorkOrder import QDWorkOrder


class QDProd(models.Model):

    Name = models.CharField(max_length=50, null=True, blank=True)
    EPAID = models.CharField(max_length=50, null=True, blank=True)
    Rate = models.IntegerField(default=0)
    RateUnits = models.IntegerField(default=0)
    LoadOrder = models.IntegerField(default=0)
    Total = models.IntegerField(default=0)
    TotalizerUnits = models.IntegerField(default=0)
    WorkOrder = models.ForeignKey(QDWorkOrder, null=True, blank=True, related_name="Prods", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "qdProds"

    def __str__(self):
        return "Product: {}".format(self.Name)



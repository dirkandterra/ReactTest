from django.db import models
from django.contrib.auth.models import User

# QD and AgSync constants
MAX_PRODUCTS_IN_BATCH = 17
MAX_CARRIERS_IN_BATCH = 4

class QDWorkOrder(models.Model):

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    WOID = models.CharField(max_length=50, null=True, blank=True)
    Date = models.CharField(max_length=50, null=True, blank=True)
    Client = models.CharField(max_length=50, null=True, blank=True)
    Farm = models.CharField(max_length=50, null=True, blank=True)
    Field = models.CharField(max_length=50, null=True, blank=True)
    State = models.CharField(max_length=50, null=True, blank=True)
    County = models.CharField(max_length=50, null=True, blank=True)
    Legal = models.CharField(max_length=50, null=True, blank=True)
    Crop = models.CharField(max_length=50, null=True, blank=True)
    Pest = models.CharField(max_length=50, null=True, blank=True)

    #Carrier, 4
    TotalCarrierRate = models.IntegerField(default=0)
    Acres = models.IntegerField(default=0)
    CarrierUnits = models.IntegerField(default=0)
    TotalCarrier = models.IntegerField(default=0)

    #Products, 17

    EffectiveApplicationRate = models.IntegerField(default=0)
    PreLoad = models.IntegerField(default=0)
    ProdRinseDelay = models.IntegerField(default=0)
    PostRinseDelay = models.IntegerField(default=0)
    Carrier2Preload = models.IntegerField(default=0)
    Completed = models.IntegerField(default=0)
    Sent2Website = models.IntegerField(default=0)
    ControllerUpToDate = models.IntegerField(default=0)         # Will be set to 1 if sent to controller

    username = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        ordering = ["WOID"]
        verbose_name_plural = "qdWorkOrders"

    def __unicode__(self):
        return self.WOID

    def __str__(self):
        return "WO: {}, User: {}".format(self.Date, self.WOID)


from django.db import models
from django.contrib.auth.models import User


class AgSyncCredential(models.Model):

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, null=True, blank=True)
    code=models.CharField(max_length=150, null=True, blank=True)
    nonce=models.CharField(max_length=150, null=True, blank=True)
    state=models.CharField(max_length=150, null=True, blank=True)
    id_token = models.CharField(max_length=1500, null=True, blank=True)
    access_token = models.CharField(max_length=1500, null=True, blank=True)
    expires_in = models.IntegerField(default=0)
    refresh_token = models.CharField(max_length=150, null=True, blank=True)
    token_type = models.CharField(max_length=150, null=True, blank=True)
    assetId = models.CharField(max_length=150, null=True, blank=True)
	
    def __str__(self):
        return self.username

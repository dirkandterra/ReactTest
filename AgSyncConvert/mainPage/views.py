from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .models import AgSyncCredential
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import WorkOrderSerializer
from .serializers import AgSyncCredentialSerializer
from rest_framework import generics
import requests
import json
import string
import random
import os
from django.shortcuts import redirect
from .models import QDWorkOrder


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        url = "https://auth.agsync.com/core/connect/authorize"
        userid = request.GET.get('g', "")
        u = AgSyncCredential.objects.filter(username=userid)
        if(not u):
            return HttpResponse(userid + ", No User Exists!")
        else:
            u.update(nonce=rndstr())
            u.update(state=rndstr())
            m = AgSyncCredential.objects.get(username=userid)
            params = url+"?client_id=sure_fire_ag_hybrid&redirect_uri=http://www.surefireag.com/Sandbox/AgSync_Callback.php&response_mode=form_post&response_type=code+id_token+token&scope=openid+profile+email+agsync+roles+offline_access&state" + m.state+"&nonce="+m.nonce
            template = loader.get_template('index.html')
            context = {'urlAgSyncLogin': params}
            return render(request, 'index.html', context)

class GetOrders(TemplateView):
    def get(self, request, **kwargs):
        userid = str(request.user)
        u = AgSyncCredential.objects.filter(username=userid)[0].access_token
        if not u:
            return HttpResponse("No User Exists!")
        else:
            response = getWOData(u)
            if response.status_code == 200:
                response2 = storeWO(request, response.text)
                return response2
            elif response.status_code == 401:
                # access token problem, try refreshing
                refResponse =tryRefresh(userid)
                result = json.loads(refResponse.text)
                if 'error' in result:
                    # refresh token didn't work, throw error
                    return HttpResponse("Refresh token invalid, please log in again")
                else:
                    # store codes and try again
                    storeAuthStuff(userid, result.items())
                    u = AgSyncCredential.objects.filter(username=userid)[0].access_token
                    response = getWOData(u)
                    if response.status_code == 200:
                        response2 = storeWO(request, response.text)
                        return response2
                    elif response.status_code == 401:
                        return HttpResponse("Error has occurred, please log in again")
            else:
                return HttpResponse("Error has occurred: " + response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class recCode(TemplateView):
    def post(self, request, **kwargs):
        userid = 'dricker'
        result = storeAuthStuff(userid, request.POST.items())
        strang = ""
        for key, value in request.POST.items():
            strang = strang + key + ": " + value + "<br>"
        if result != 0:
            #for key, value in request.POST.items():
                # strang += key + ":" + value + "<br>"
            # return HttpResponse(strang)
            return HttpResponse(strang)
            # return redirect('getOrders')
        else:
            strang="Can't Find User"
            return HttpResponse(strang)


class CredCreate(generics.ListCreateAPIView):
    queryset = AgSyncCredential.objects.all()
    serializer_class = AgSyncCredentialSerializer

def rndstr():
    return ''.join([random.choice(string.ascii_letters + string.digits) for x in range(10)])

def login(request):
    url = "https://auth.agsync.com/core/connect/authorize"
    userid = str(request.user)
    u = AgSyncCredential.objects.filter(username=userid)
    if(not u):
        return HttpResponse("No User Exists!")
    else:
        u.update(nonce=rndstr())
        u.update(state=rndstr())
        m = AgSyncCredential.objects.get(username=userid)
        params = url+"?client_id=sure_fire_ag_hybrid&redirect_uri=http://www.surefireag.com/Sandbox/AgSync_Callback.php&response_mode=form_post&response_type=code+id_token+token&scope=openid+profile+email+agsync+roles+offline_access&state" + m.state+"&nonce="+m.nonce
        template = loader.get_template('index.html')
        context = {'urlAgSyncLogin': params}
        return render(request, 'index.html', context)


def storeWO(request, data):
    json_data = json.loads(data)
    jj = 0
    strang = "{}, there was an issue with the data or all were duplicates, no records were saved".format(request.user)
    for x in json_data:
        serializer = WorkOrderSerializer(data=x)
        if serializer:
            if serializer.is_valid():
                if serializer == None:
                    strang = "{}, execute order 66.....{} Orders saved".format(request.user, jj)
                else:
                    obj = serializer.save()
                    obj.save()
                    jj += 1
                    strang = "{}, execute order 66.....{} Orders saved".format(request.user, jj)

    return HttpResponse(strang)

def tryRefresh(userid):
    u = AgSyncCredential.objects.filter(username=userid)[0].refresh_token
    if not u:
        return HttpResponse("{'error': 'NoUser'}")
    else:
        if u != "":
            url = "https://auth.agsync.com/core/connect/token"

            payload = "refresh_token=" + u + "&grant_type=refresh_token"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'Authorization': "Basic c3VyZV9maXJlX2FnX2h5YnJpZDo0ODVkYmIxZS0xOWUyLTQ0NDUtOWEwZC0yZDFjZjMxZDhiNWI="
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            return response
        else:
            return HttpResponse("{'error': 'NoRefresh'}")


def storeAuthStuff(userid,items):
    u = AgSyncCredential.objects.filter(username=userid)
    aId = "Nope"
    if not u:
        return 0
    else:
        for key, value in items:
            if(key == 'refresh_token'):
                u.update(refresh_token=value)
            elif(key == 'code'):
                u.update(code=value)
            elif (key == 'access_token'):
                u.update(access_token=value)
            elif (key == 'id_token'):
                u.update(id_token=value)
            elif (key == 'expires_in'):
                u.update(expires_in=value)
            elif (key == 'token_type'):
                u.update(token_type=value)
            elif (key == 'assetId'):
                u.update(assetId=value)
    return "Asset ID: " + aId


def getWOData(accesstoken):
    url = "https://dispatch.agsync.com/api/workorders/operator"
    accesstoken = "Bearer " + accesstoken
    headers = {
        'cache-control': "no-cache",
        'Authorization': accesstoken
    }
    return requests.request("GET", url, headers=headers)


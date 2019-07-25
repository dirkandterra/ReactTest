from rest_framework import serializers
from .models.units import AgSyncRateUnits
from .models import AgSyncCredential
from .models import QDWorkOrder
from .models import qdWorkOrder
from .models import QDProd
from .models import QDCarrier


class WorkOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = QDWorkOrder
        fields = '__all__'

    def to_representation(self, obj):
        """
        Returns a blank string, so that no data is sent back to a controller after uploading a status
        """
        return ''

    def to_internal_value(self, data):
        """
        Converts status binary data to a python dictionary.
        """
        agSyncWO_dict = data
        qdWO_dict={}
        #numProducts = len(agSyncWO_dict['Mix']['Products'])
        qdWO_dict['WOID'] = agSyncWO_dict['OrderExtendedData']['OrderId']
        rawAgSyncDate = agSyncWO_dict['ModifiedDateTime']
        qdDateTime = rawAgSyncDate
        qdWO_dict['Date'] = qdDateTime
        existingWORecord=QDWorkOrder.objects.filter(WOID=qdWO_dict['WOID'])
        if existingWORecord.count():
            diffDateRecord=QDWorkOrder.objects.filter(WOID=qdWO_dict['WOID'], Date=qdDateTime)
            if diffDateRecord.count() == 0:
                # delete, we have a newer one.
                existingWORecord.delete()
                # delete old WO?
            else:
                raise serializers.ValidationError('Duplicate WO')
                return

        qdWO_dict['Client'] = agSyncWO_dict['Field']['Grower']['Name']
        qdWO_dict['Farm'] = agSyncWO_dict['Field']['Farm']['Name']
        qdWO_dict['Field'] = agSyncWO_dict['Field']['Name']
        qdWO_dict['State'] = agSyncWO_dict['Field']['State']
        qdWO_dict['County'] = agSyncWO_dict['Field']['County']
        qdWO_dict['Legal'] = agSyncWO_dict['Field']['Plss'] + " " + agSyncWO_dict['Field']['Section']
        qdWO_dict['Crop'] = agSyncWO_dict['Field']['Crop']['Name']
        pests = ""
        for x in agSyncWO_dict['Services'][0]['Mix']['Products']:
            kk = 0
            for y in x['Pests']:
                pests = pests + x['Pests'][kk]['Name'] + ", "
                kk += 1
        qdWO_dict['Pest'] = pests

        # Carrier & Products
        #qdWO_dict['Carrier'] = models.CharField(max_length=1200, null=True, blank=True)  # Array of 4 dictionaries
        totalCarrierRate = 0
        # We need to find totalCarrierRate first
        for x in agSyncWO_dict['Services'][0]['Mix']['Products']:
            if x['IsCarrier']:
                totalCarrierRate += int(x['Rate']['Value']) * 10  # one decimal
        ii = 0
        jj = 0
        qdWO_dict["Prods"] = []
        qdWO_dict["Carriers"] = []
        for x in agSyncWO_dict['Services'][0]['Mix']['Products']:
            n = x['Name']
            e = ''       # can't find EPAID from AgSync yet
            if x['IsCarrier']:
                ii += 1
                carrier = QDCarrier.objects.create(Name=n, EPAID=e, Rate=int(x['Rate']['Value'])*10/totalCarrierRate*10000, LoadOrder=ii)
                qdWO_dict["Carriers"].append(carrier)
                # Take in first carrier rate unit as all carrier rate units
                if ii == 1:
                    carrierUnit = AgSyncRateUnits.ConvertToQDRate(AgSyncRateUnits(x['Rate']['Measure']['Ordinal']))
                if ii > qdWorkOrder.MAX_CARRIERS_IN_BATCH:
                    continue        # out of carrier slots, skip to the next product/carrier
            else:
                jj += 1
                product = QDProd.objects.create(Name=n, EPAID=e, Rate=int(x['Rate']['Value'])*100,
                                           RateUnits=AgSyncRateUnits.ConvertToQDRate(AgSyncRateUnits(x['Rate']['Measure']['Ordinal'])),
                                           LoadOrder=jj, Total=0,
                                           TotalizerUnits=AgSyncRateUnits.ConvertRateUnitsToQDTotalUnits(AgSyncRateUnits(x['Rate']['Measure']['Ordinal'])))
                qdWO_dict["Prods"].append(product)
                if jj > qdWorkOrder.MAX_PRODUCTS_IN_BATCH:
                    continue        # out of product slots, skip to the next product/carrier

        # Fill up the rest of the empty carrier and products
        while ii < qdWorkOrder.MAX_CARRIERS_IN_BATCH:
            carrier = QDCarrier.objects.create(Name='', EPAID='', Rate=0, LoadOrder=0)
            qdWO_dict["Carriers"].append(carrier)
            ii += 1

        while jj < qdWorkOrder.MAX_PRODUCTS_IN_BATCH:
            product = QDProd.objects.create(Name='', EPAID='', Rate=0, RateUnits=0, LoadOrder=jj, Total=0, TotalizerUnits=0)
            qdWO_dict["Prods"].append(product)
            jj += 1

        qdWO_dict['TotalCarrierRate'] = totalCarrierRate
        qdWO_dict['CarrierUnits'] = carrierUnit
        qdWO_dict['TotalCarrier'] = 0           # Leave 0, let QD calculate
        qdWO_dict['Acres'] = agSyncWO_dict['Field']['Area']*10
        qdWO_dict['EffectiveApplicationRate'] = agSyncWO_dict['Services'][0]['Mix']['Rate']['Value']*10
        qdWO_dict['PreLoad'] = 0
        qdWO_dict['ProdRinseDelay'] = 3
        qdWO_dict['PostRinseDelay'] = 10
        qdWO_dict['Carrier2Preload'] = 0        # just one carrier for now (Carrier 0)
        qdWO_dict['Completed'] = 0
        qdWO_dict['Sent2Website'] = 0
        qdWO_dict['ControllerUpToDate'] = 0

        return qdWO_dict


class AgSyncCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgSyncCredential
        fields = '__all__'

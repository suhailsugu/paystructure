from rest_framework import serializers
from apps.client.models import Client,PaymentMaster



"""Client Schemas"""
class GetPaymentTypeDropdownSchemas(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk',allow_null=True)
    label = serializers.CharField(source='salary_type',allow_null=True)
    
    class Meta:
        model = PaymentMaster
        fields = ['value','label']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas



"""Client Schemas"""
class GetClientListSchema(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','company_name','phone_number','city','state','country']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
    
class GetClientDetailSchema(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id','company_name','phone_number','city','state','country','pay_structure','is_active']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    

class GetClientDropdownSchemas(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk',allow_null=True)
    label = serializers.CharField(source='company_name',allow_null=True)
    
    class Meta:
        model = Client
        fields = ['value','label']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
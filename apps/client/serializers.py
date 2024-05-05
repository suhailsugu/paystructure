from rest_framework import serializers
from apps.client.models import Client,ClientPayRoles
from paystructure.helpers.designation_salary_finder import SalaryFinder
from paystructure.helpers.helper import  get_token_user_or_none


"""Client Serializers"""
class CreateOrUpdateClientSerializer(serializers.ModelSerializer):
    id              = serializers.IntegerField(allow_null=True, required=False)
    company_name    = serializers.CharField(required=True)
    phone_number    = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city            = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    state           = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    country         = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    pay_structure   = serializers.CharField(required=False,allow_null=True,allow_blank=True)

    class Meta:
        model = Client 
        fields = ['id','company_name','phone_number','city','state','country','pay_structure']
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    
    def create(self, validated_data):
        request = self.context.get('request',None)
        user_instance = get_token_user_or_none(request)

        instance                = Client()
        instance.company_name   = validated_data.get('company_name')
        instance.phone_number   = validated_data.get('phone_number')
        instance.city           = validated_data.get('city')
        instance.state          = validated_data.get('state')
        instance.country        = validated_data.get('country')
        instance.pay_structure  = validated_data.get('pay_structure')
        instance.created_by     = user_instance
        instance.modified_by    = user_instance
        instance.save()
  
        return instance

    
    def update(self, instance, validated_data):
        request = self.context.get('request',None)
        
        instance.company_name   = validated_data.get('company_name')
        instance.phone_number   = validated_data.get('phone_number')
        instance.city           = validated_data.get('city')
        instance.state          = validated_data.get('state')
        instance.country        = validated_data.get('country')
        instance.pay_structure  = validated_data.get('pay_structure')
        instance.modified_by    = get_token_user_or_none(request)
        instance.save()
                
        return instance


class ActiveOrDeactivateClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    
    class Meta:
        model = Client
        fields = ['id']
    
    def validate(self, attrs):
        return super().validate(attrs)


    def update(self, instance , validated_data):
        instance.is_active = True if not instance.is_active else False
        instance.save()
        return instance 


"""Designation Serializers"""
class CreateOrUpdateDesignationSerializer(serializers.ModelSerializer):
    id            = serializers.IntegerField(allow_null=True, required=False)
    company       = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(),required=True)
    designation   = serializers.CharField(required=True)
    pay_values    = serializers.JSONField(required=True)
   
    class Meta:
        model = ClientPayRoles 
        fields = ['id','company','designation','pay_values']
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    
    def create(self, validated_data):
        instance                = ClientPayRoles()
        instance.company        = validated_data.get('company')
        instance.designation    = validated_data.get('designation')
        instance.pay_values     = validated_data.get('pay_values')
        instance.save()

        SalaryFinder(payrole=instance).total_salary()
  
        return instance

    
    def update(self, instance, validated_data):
        
        instance.company        = validated_data.get('company')
        instance.designation    = validated_data.get('designation')
        instance.pay_values     = validated_data.get('pay_values')
        instance.save()

        SalaryFinder(payrole=instance).total_salary()
                
        return instance

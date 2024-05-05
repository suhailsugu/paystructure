from rest_framework import serializers
from apps.employee.models import EmployeeMaster

    

"""Employee Schemas"""
class GetEmployeeListSchema(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['id','designation','employee_id','employee_name','phone_number']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
    
class GetEmployeeDetailSchema(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMaster
        fields = ['id','designation','employee_id','employee_name','phone_number']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

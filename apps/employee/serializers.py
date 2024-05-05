from rest_framework import serializers
from apps.employee.models import EmployeeMaster, MonthlySalary
from apps.client.models import ClientPayRoles
from paystructure.helpers.helper import  get_token_user_or_none


"""Employee Serializers"""
class CreateOrUpdateEmployeeSerializer(serializers.ModelSerializer):
    id            = serializers.IntegerField(allow_null=True, required=False)
    employee_id   = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    employee_name = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    phone_number  = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    salary_str    = serializers.JSONField(required=False,allow_null=True)

    class Meta:
        model = EmployeeMaster 
        fields = ['id','employee_id','employee_name','phone_number','salary_str']
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    
    def create(self, validated_data):
        request = self.context.get('request',None)
        user_instance = get_token_user_or_none(request)

        instance                = EmployeeMaster()
        instance.employee_id    = validated_data.get('employee_id')
        instance.employee_name  = validated_data.get('employee_name')
        instance.phone_number   = validated_data.get('phone_number')
        instance.salary_str     = validated_data.get('salary_str')
        instance.created_by     = user_instance
        instance.modified_by    = user_instance
        instance.save()
  
        return instance

    
    def update(self, instance, validated_data):
        request = self.context.get('request',None)
        
        instance.employee_id    = validated_data.get('employee_id')
        instance.employee_name  = validated_data.get('employee_name')
        instance.phone_number   = validated_data.get('phone_number')
        instance.salary_str     = validated_data.get('salary_str')
        instance.modified_by    = get_token_user_or_none(request)
        instance.save()
                
        return instance
    
    
class AddDesignationToEmployeeSerializer(serializers.ModelSerializer):
    employee    = serializers.IntegerField(required=True)
    designation = serializers.PrimaryKeyRelatedField(queryset=ClientPayRoles.objects.all(), required=True)

    class Meta:
        model = EmployeeMaster 
        fields = ['employee','designation']
    
    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        designation             = validated_data.get('designation')
        
        instance.designation    = designation
        instance.final_salary   = designation.final_salary if designation.final_salary is not None else 0
        instance.save()
                
        return instance
    
    
class GenerateMonthlySalarySerializer(serializers.ModelSerializer):
    employee        = serializers.PrimaryKeyRelatedField(queryset=EmployeeMaster.objects.all(), required=True)
    working_days    = serializers.IntegerField(required=True)
    present_days    = serializers.IntegerField(required=True)

    class Meta:
        model = MonthlySalary 
        fields = ['employee','working_days','present_days']
    
    def validate(self, attrs):
        return super().validate(attrs)


    def create(self, validated_data):

        employee,working_days,present_days = validated_data.get('employee',None),validated_data.get('working_days',1),validated_data.get('present_days',1)
        salary          = employee.final_salary or 1

        print(salary)
        print(working_days)
        print(present_days)
        
        final_salary    = (salary/working_days)*present_days
        
        instance                = MonthlySalary()
        instance.employee       = employee
        instance.working_days   = working_days
        instance.present_days   = present_days
        instance.final_salary   = final_salary
        instance.save()


        return instance


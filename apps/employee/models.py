from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.client.models import ClientPayRoles
from apps.user.models import Users
from django_acl.models import AbstractDateFieldMix



class EmployeeMaster(AbstractDateFieldMix):
    designation     = models.ForeignKey(ClientPayRoles, on_delete=models.CASCADE, related_name='employee_company',null=True,blank=True)
    employee_id     = models.CharField(_('Employee ID'), max_length=255, blank = True, null = True)
    employee_name   = models.CharField(_('Employee Name'), max_length=255, blank = True, null = True)
    phone_number    = models.CharField(_('Phone Number'), max_length=255, blank = True, null = True)
    final_salary    = models.DecimalField(_('Final Salary'),max_digits=10,decimal_places=2, blank = True, null = True)
    is_active       = models.BooleanField(_('Is Active'),default=True)
    created_by      = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='employee_createdby',null=True,blank=True)
    modified_by     = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='employee_modified_by',null=True,blank=True)

    class Meta:
        verbose_name = 'EmployeeMaster'
        verbose_name_plural = 'EmployeeMaster'

        
class MonthlySalary(AbstractDateFieldMix):
    employee        = models.ForeignKey(EmployeeMaster, on_delete=models.CASCADE, related_name='salaried_employee',null=True,blank=True)
    working_days    = models.IntegerField(_('Working Days'), blank = True, null = True)
    present_days    = models.IntegerField(_('Present Days'), blank = True, null = True)
    final_salary    = models.DecimalField(_('Final Salary'),max_digits=10,decimal_places=5, blank = True, null = True)
    is_paid         = models.BooleanField(_('Is Paid'),default=True)

    class Meta:
        verbose_name = 'MonthlySalary'
        verbose_name_plural = 'MonthlySalary'



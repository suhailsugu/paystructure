from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.user.models import Users
from django_acl.models import AbstractDateFieldMix


class PaymentMaster(AbstractDateFieldMix):
    salary_type   = models.CharField(_('Salary Type'), max_length=255, blank = True, null = True)
    is_active     = models.BooleanField(_('Is Active'),default=True)
  
    class Meta: 
        verbose_name = 'PaymentMaster'
        verbose_name_plural = "PaymentMaster"

    def __str__(self):
        return self.salary_type
    


class Client(AbstractDateFieldMix):
    company_name    = models.CharField(_('Company Name'), max_length=255, blank = True, null = True)
    phone_number    = models.CharField(_('Phone Number'), max_length=255, blank = True, null = True)
    city            = models.CharField(_('City'), max_length=255, blank = True, null = True)
    state           = models.CharField(_('State'), max_length=255, blank = True, null = True)
    country         = models.CharField(_('Country'), max_length=255, blank = True, null = True)
    pay_structure   = models.CharField(_('Pay Structure'), max_length=255, blank = True, null = True)
    is_active       = models.BooleanField(_('Is Active'),default=True)
    created_by      = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='client_createdby',null=True,blank=True)
    modified_by     = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='client_modified_by',null=True,blank=True)

  
    class Meta: 
        verbose_name = 'Client'
        verbose_name_plural = "Client"

    def __str__(self):
        return self.phone_number
    

    
class ClientPayRoles(AbstractDateFieldMix):
    company       = models.ForeignKey(Client,on_delete=models.CASCADE, blank = True, null = True)
    designation   = models.CharField(_('Designation'), max_length=255, blank = True, null = True)
    pay_values    = models.JSONField(_('pay_structure'), blank = True, null = True)
    final_salary  = models.DecimalField(_('Final Salary'),max_digits=10,decimal_places=2, blank = True, null = True)


    class Meta: 
        verbose_name = 'ClientPayRoles'
        verbose_name_plural = "ClientPayRoles"

    def __str__(self):
        return self.designation




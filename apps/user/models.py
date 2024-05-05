
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_acl.models import Group
from django_acl.utils.helper import acl_has_perms
from django_acl.models import AbstractDateFieldMix




class UserManager(BaseUserManager):
    def create_user(self, username, password = None, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))

        user = self.model(username = username, **extra_fields)
        if password:
            user.set_password(password.strip())
            
        user.save()
        return user


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_admin', True)
     
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(username, password, **extra_fields)



class Users(AbstractBaseUser, PermissionsMixin, AbstractDateFieldMix):

        
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self.original_password = self.password
        
    email                         = models.EmailField(_('email'), unique = True, max_length = 255, blank = True, null = True)
    username                      = models.CharField(_('username'), max_length = 300, unique = True, blank = True, null = True)
    password                      = models.CharField(_('password'), max_length=255, blank = True, null = True)
    slug                          = models.SlugField(_('slug'),  max_length=255, unique=True, editable=False, blank = True, null = True)
    date_joined                   = models.DateTimeField(_('date_joined'),  auto_now_add = True, blank = True, null = True)
    last_login                    = models.DateTimeField(_('last_login'), blank = True, null = True)
    last_logout                   = models.DateTimeField(_('last_logout'),  blank = True, null = True)
    last_active                   = models.DateTimeField(_('last_active'),  blank = True, null = True)
    last_password_reset           = models.DateTimeField(_('last_password_reset'),  blank = True, null = True)
    is_verified                   = models.BooleanField(default = False)
    is_admin                      = models.BooleanField(default = False)
    is_staff                      = models.BooleanField(default = False)
    is_superuser                  = models.BooleanField(default = False)
    is_logged_in                  = models.BooleanField(default = False)
    failed_login_attempts         = models.IntegerField(_('Failed Login Attempts'),  blank = True, null = True)
    is_active                     = models.BooleanField(_('Is Active'), default=True)
    is_password_reset_required    = models.BooleanField(default=False)
    name                          = models.CharField(_('name'), max_length=255, blank = True, null = True)
    
    user_groups = models.ManyToManyField(
        Group,verbose_name=_("groups"),blank=True,help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),related_name="user_set",related_query_name="user",)
    

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    
    def __str__(self):
        return "{username}".format(username=self.username)
    

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj = None):
        "Does the user have a specific permission?"
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    
    
    def has_acl_perms(self, perm, obj = None):
        return acl_has_perms(self, perm, obj=obj)
    
            
            
    def _password_has_been_changed(self):
        return self.original_password != self.password
    




class GeneratedAccessToken(AbstractDateFieldMix):
    token = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.token


class ERPModelCatalog(models.Model):
    
    module      = models.CharField(_('Catalog'),max_length=255, blank=True, null= True)
    is_active   = models.BooleanField(_('Is Active'),default=False)

    class Meta: 
        verbose_name = 'ERP Model Catalog'
        verbose_name_plural = "ERP Model Catalogs"

    
    

from django.contrib import admin

from apps.user.models import GeneratedAccessToken,Users,ERPModelCatalog


# Register your models here.



@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email','username','name','is_admin','is_staff','is_superuser','is_logged_in','is_verified','is_active', )
    list_display_links = ['email']
    search_fields = ('email','username', )
    list_filter = ('created_date', 'is_active', )
    
    
    

@admin.register(ERPModelCatalog)
class ERPModelCatalogAdmin(admin.ModelAdmin):
    list_display = ('id','module','is_active' )
    list_display_links = ['id']
    








@admin.register(GeneratedAccessToken)
class GeneratedAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token','user')
    list_filter  = ('user',)
    
    

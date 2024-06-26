from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [

    path('retrieve-permissions', views.RetrievePermissionsApiView.as_view()),

    re_path(r'^users/', include([
        path('create-or-update-user', views.CreateOrUpdateUserApiView.as_view()),
        path('create-or-update-password', views.UpdateUserPasswordApiView.as_view()),
        path('activate-or-deactivate-users', views.ActiveOrDeactivateUsersApiView.as_view()),
        path('retrieve-users', views.RetrieveUsersApiView.as_view()),
        path('retrieve-user-dropdown-options', views.RetrieveUserDropdownOptionsApiView.as_view()),
        path('retrieve-user-info', views.RetrieveUserInfoApiView.as_view()),
    ])),

    re_path(r'^roles/', include([
        path('create-or-update-role', views.CreateOrUpdateRoleApiView.as_view()),
        path('retrieve-roles', views.RetrieveRolesApiView.as_view()),
        path('retrieve-role-info', views.RetrieveRoleInfoApiView.as_view()),
        path('destroy-role', views.DestroyRoleApiView.as_view()),
    ])),
    
    re_path(r'^groups/', include([
        path('retrieve-groups', views.RetrieveGroupsApiView.as_view()),
        path('create-or-update-group', views.CreateOrUpdateGroupApiView.as_view()),
        path('retrieve-group-info', views.RetrieveGroupInfoApiView.as_view()),
        path('destroy-group', views.DestroyGroupsApiView.as_view()),
    ])),

]
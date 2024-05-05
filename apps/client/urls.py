from django.urls import path,include,re_path
from . import views



urlpatterns = [

    re_path(r'^v1/', include([

        re_path(r'^payment-type/', include([
            path('get-payment-type-dropdown', views.GetPaymentTypeDropdownApiView.as_view()),
        ])),

        re_path(r'^client/', include([
            path('create-or-update-client',views.CreateorUpdateClientApiView.as_view()),
            path('get-client-list', views.GetClientListApiView.as_view()),
            path('get-client-details', views.GetClientDetailApiView.as_view()),
            path('get-client-dropdown', views.GetClientDropdownApiView.as_view()),
            path('activate-or-deactivate-client', views.ActiveOrDeactivateClientApiView.as_view()),
        ])),

        re_path(r'^designation/', include([
            path('create-or-update-designation',views.CreateorUpdateDesignationApiView.as_view()),
        ])),

        
    ])),


]
from django.urls import path,include,re_path
from . import views



urlpatterns = [

    re_path(r'^v1/', include([

        re_path(r'^employee/', include([
            path('create-or-update-employee',views.CreateorUpdateEmployeeApiView.as_view()),
            path('add-employee-designation',views.AddDesignationToEmployeeApiView.as_view()),
            path('get-employee-list', views.GetEmployeeListApiView.as_view()),
            path('get-employee-details', views.GetEmployeeDetailApiView.as_view()),
            path('generate-monthly-salary', views.GenerateMonthlySalaryApiView.as_view()),
        ])),
        
    ])),


]
from rest_framework import generics,status
from drf_yasg.utils import swagger_auto_schema
from apps.client.models import Client, ClientPayRoles,PaymentMaster
from paystructure.helpers.helper import get_object_or_none
from paystructure.helpers.pagination import RestPagination
from paystructure.helpers.response import ResponseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from paystructure.helpers.custom_messages import _success,_record_not_found
from drf_yasg import openapi
import  os,sys
from django.db.models import Q

from apps.client.schemas import (
        GetClientListSchema, 
        GetClientDetailSchema, 
        GetClientDropdownSchemas,
        GetPaymentTypeDropdownSchemas,

    )

from apps.client.serializers import (
        ActiveOrDeactivateClientSerializer,
        CreateOrUpdateClientSerializer,
        CreateOrUpdateDesignationSerializer
    )


"""Payment Type Views"""
class GetPaymentTypeDropdownApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPaymentTypeDropdownApiView, self).__init__(**kwargs)
          
    serializer_class = GetPaymentTypeDropdownSchemas
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Payment Type"])
    def get(self, request):
        
        try:
            payment_queyset   = PaymentMaster.objects.all().filter(is_active = True)
            serializer        = self.serializer_class(payment_queyset, many=True, context={"request": request})
            self.response_format['status_code'] = status.HTTP_200_OK

            self.response_format["data"] = serializer.data 
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


"""Client Views"""

class CreateorUpdateClientApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateorUpdateClientApiView, self).__init__(**kwargs)
        
    serializer_class = CreateOrUpdateClientSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Client"])
    def post(self, request):
        try:
            
            client_instance = get_object_or_none(Client,pk=request.data.get('id', None))

            serializer = self.serializer_class(client_instance, data=request.data, context = {'request' : request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GetClientListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetClientListApiView, self).__init__(**kwargs)
    
    serializer_class    = GetClientListSchema
    permission_classes = (IsAuthenticated,)
    pagination_class    = RestPagination
  
    search        = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="The search value ", required=False)
  
    @swagger_auto_schema(tags=["Client"], manual_parameters=[search], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            search_value    = request.GET.get('search', None)

            filter_set = Q()
            if search_value not in ['',None]:
                filter_set = Q(company_name=search_value)
     
            queryset    = Client.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GetClientDetailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetClientDetailApiView, self).__init__(**kwargs)
        
    serializer_class = GetClientDetailSchema
    permission_classes = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description="Enter the id")
    
    @swagger_auto_schema(tags=["Client"], manual_parameters=[id])
    def get(self, request):
        
        try:
            
            client_instance = get_object_or_none(Client, pk=request.GET.get('id', None))

            if client_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)
                
            data = self.serializer_class(client_instance, context={'request': request}).data 
            
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = data 
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GetClientDropdownApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetClientDropdownApiView, self).__init__(**kwargs)
          
    serializer_class = GetClientDropdownSchemas
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Client"])
    def get(self, request):
        
        try:
            client_queyset    = Client.objects.all().filter(is_active = True)
            serializer        = self.serializer_class(client_queyset, many=True, context={"request": request})
            self.response_format['status_code'] = status.HTTP_200_OK

            self.response_format["data"] = serializer.data 
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class ActiveOrDeactivateClientApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ActiveOrDeactivateClientApiView, self).__init__(**kwargs)
        
    serializer_class = ActiveOrDeactivateClientSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Client"])
    def put(self, request):
            
        try:
            client_instance = get_object_or_none(Client,pk=request.data.get('id', None))

            serializer = self.serializer_class(client_instance, data=request.data, context = {'request' : request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



"""Designation Views"""
class CreateorUpdateDesignationApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateorUpdateDesignationApiView, self).__init__(**kwargs)
        
    serializer_class = CreateOrUpdateDesignationSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Designation"])
    def post(self, request):
        try:
            
            designation_instance = get_object_or_none(ClientPayRoles,pk=request.data.get('id', None))

            serializer = self.serializer_class(designation_instance, data=request.data, context = {'request' : request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


from typing import Any
from django.shortcuts import render
from rest_framework import generics, status
from apps.authentication.schemas import LoginResponseSchema
from apps.authentication.serializers import LoginSerializer, LogoutSerializer
from apps.user.models import GeneratedAccessToken
from paystructure.helpers.helper import get_token_user_or_none, update_last_logout
from paystructure.helpers.response import ResponseInfo
from paystructure.helpers.custom_messages import _account_tem_suspended, _invalid_credentials
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.contrib import auth
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from paystructure.middleware.JWTAuthentication import BlacklistedJWTAuthentication
from django.utils import timezone




class LoginApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs: Any):
        self.response_format = ResponseInfo().response
        super(LoginApiView, self).__init__(**kwargs)
        
    serializer_class = LoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            
            if not serializer.is_valid():
                self.response_format['status']      = True
                self.response_format['errors']      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            
            
            user = auth.authenticate(
                username=serializer.validated_data.get("username", ""),
                password=serializer.validated_data.get("password", ""),
            )
            
            if user:
                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = status.HTTP_406_NOT_ACCEPTABLE
                    self.response_format['stauts']      = False
                    self.response_format['data']        = data
                    self.response_format['message']     = _account_tem_suspended
                    return Response(self.response_format, status=status.HTTP_200_OK)
                
                else:
                    
                    user.is_logged_in = True
                    user.last_login   = timezone.now()
                    user.save(update_fields=['is_logged_in', 'last_login'])
                    
                    serializer    = LoginResponseSchema(user, context={"request": request})
                    refresh       = RefreshToken.for_user(user)
                    token         = str(refresh.access_token)
                    data          = {'user': serializer.data, 'token':token, 'refresh': str(refresh)}
                    GeneratedAccessToken.objects.create(user=user, token=token)
                    
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format['status']      = True
                    self.response_format['data']        = data
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)
            
        except Exception as es:
            
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(es)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                
                
                
class LogoutApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs: Any):
        self.response_format = ResponseInfo().response
        super(LogoutApiView, self).__init__(**kwargs)
        
    serializer_class          = LogoutSerializer
    permission_classes        = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        
        
        try:
            user = get_token_user_or_none(request)
            if user is not None:
                GeneratedAccessToken.objects.using('reader').filter(user=user).delete()
                update_last_logout(None, user)
            
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserModel
from .serializers import RegisterUserSerializer
from rest_framework.throttling import ScopedRateThrottle



# Create your views here.

#register class with Generic view
class RegisterApiView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'register'

    # rewrite create function with another message and response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message' : 'This user is registered'}, status=status.HTTP_201_CREATED)



#register class with API View
# class RegisterView(APIView):
#     throttle_classes = [ScopedRateThrottle]
#     throttle_scope = 'register'
#     def post(self, request):
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
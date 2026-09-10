from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import ProjectModel
from Projects.serializers import CreateProjectSerializer


# Create your views here.


# create new project with GenericView
class CreateProjectAPIView(CreateAPIView):
    queryset = ProjectModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateProjectSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)




# create new project with APIView
# class CreateProjectAPIView( APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#
#         serializer = CreateProjectSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
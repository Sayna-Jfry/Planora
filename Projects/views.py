from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from Users.models import UserModel

from .models import ProjectModel
from Projects.serializers import ProjectSerializer


# Create your views here.


# create new project with GenericView
class CreateProjectAPIView(CreateAPIView):
    queryset = ProjectModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)




# create new project with APIView
# class CreateProjectAPIView( APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#
#         serializer = ProjectSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user')
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response({"message": 'This user is not found'},status=status.HTTP_404_NOT_FOUND)
        if project.members.filter(id=user_id).exists():
            return Response({"message": 'This user is already added to this project'},status=status.HTTP_400_BAD_REQUEST)
        project.members.add(user)
        return Response({"message": "member added successfully"},status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user')
        user = UserModel.objects.filter(id=user_id).first()
        if not user:
            return Response({"message": 'This user is not found'},status=status.HTTP_404_NOT_FOUND)

        if project.members.filter(id=user_id).exists():
            project.members.remove(user)
            return Response({"message": "member removed successfully"},status=status.HTTP_200_OK)

        return Response({"message": "This user is not in this project already"},status=status.HTTP_400_BAD_REQUEST)

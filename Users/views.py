from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserModel
from .serializers import RegisterUserSerializer, ProfileUserSerializer
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken



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


# روش اول لاگ اوت کردن از حساب ، در این روش کاربر فقط acces توکن خود را در هدر درخواست میقرسته و تمام رفرش توکن هایی ک مربوط به اون کاربر هست مسدود میشه
class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        tokens = OutstandingToken.objects.filter(user=user)

        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({'message' : 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)



#  روش دو لاگ اوت کردن ، در این روش کاربر علاوه بر اکسس توکن ، رفرش توکن خود را هم در بادی ارسال میکنه و ما مستقیما فقط اون رفرش توکن رو مسدود میکنیم
# class LogOutApiView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         refresh_token = request.data.get('refresh')
#
#         if not refresh_token:
#             return Response({'message' : 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#
#         try :
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response ( {'message' : 'Successfully logged out.'}, status=status.HTTP_200_OK)
#
#         except Exception:
#             return Response({'message' : 'Failed to log in'}, status=status.HTTP_400_BAD_REQUEST)


# user profile with Generic View
class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUserSerializer

    def get_object(self):
        return self.request.user



# user profile with APIView
# class UserInfoView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         return Response({
#             'username': user.username,
#             'email': user.email,
#
#         }, status=status.HTTP_200_OK)
#
#     def patch(self, request):
#         user = request.user
#         serializer = ProfileUserSerializer(user, data=request.data, partial = True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


# delete account with Generic View
# class DeleteAccountAPIView(DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#
#
#     def get_object(self):
#         return self.request.user
#
#     def destroy(self, request, *args, **kwargs):
#         user = self.get_object()
#         user.delete()
#         return Response({'message' : 'Successfully deleted account'}, status=status.HTTP_202_ACCEPTED)


# delete account with APIView
class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user = request.user
        user.delete()

        return Response({'message': 'Successfully deleted account'}, status=status.HTTP_202_ACCEPTED)

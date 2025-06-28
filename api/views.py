from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from .models import TestItem
from .serializers import TestItemSerializer
from firebase_admin import auth

class TestItemViewSet(viewsets.ModelViewSet):
    queryset = TestItem.objects.all()
    serializer_class = TestItemSerializer

class StatusCheckView(APIView):
    def get(self, request, format=None):
        return Response({"status": "DRF is working!"})

class FirebaseLoginView(APIView):
    def post(self, request):
        id_token = request.data.get('idToken')
        if not id_token:
            return Response({'error': 'ID token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the ID token using Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')

            User = get_user_model()

            # Get or create the Django user
            try:
                user = User.objects.get(username=uid)
            except User.DoesNotExist:
                user = User(username=uid, email=email)
                user.set_unusable_password()
                user.save()

            # Log in the Django user
            login(request, user, backend='accounts.backends.FirebaseAuthenticationBackend')
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

        except FirebaseError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileAPIView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username' # Look up by username
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

class FirebaseAuthenticationBackend(BaseBackend):
    def authenticate(self, request, firebase_id_token=None):
        if not firebase_id_token:
            return None

        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(firebase_id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            display_name = decoded_token.get('name')

            User = get_user_model()

            # Get or create the Django user
            try:
                user = User.objects.get(username=uid) # Use UID as username
            except User.DoesNotExist:
                # Create a new user if not found
                user = User(username=uid) # Use UID as username
                if email:
                    user.email = email
                if display_name:
                    user.first_name = display_name # Or another appropriate field
                user.set_unusable_password() # Firebase handles passwords
                user.save()

            return user

        except FirebaseError:
            # Token is invalid or expired
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

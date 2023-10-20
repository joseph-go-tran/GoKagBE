from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthenticationPermissionMixins:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

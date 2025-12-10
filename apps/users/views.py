from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    Endpoint to register a new SaaS Tenant (User + Organization).
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return the user data in the response
        return Response({
            "user": UserSerializer(user).data,
            "message": "Account created successfully."
        }, status=status.HTTP_201_CREATED)
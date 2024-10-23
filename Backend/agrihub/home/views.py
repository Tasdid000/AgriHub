from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import Userrenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [Userrenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'User created successfully'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [Userrenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'User logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'non_field_error': ['Invalid email or password']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [Userrenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


    
class UserChangePasswordView(APIView):
    renderer_classes = [Userrenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)


# class SendPasswordResetEmailView(APIView):
#     renderer_classes = [Userrenderer]

#     def post(self, request, format=None):
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg': 'Password reset link sent successfully. Please check the Email.'}, status=status.HTTP_200_OK)
       

class SendPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'Password reset link sent successfully.'})

class UserPasswordResetView(APIView):
    renderer_classes = [Userrenderer]

    def post(self, request, email, token, format=None):
        serializer = UserPasswordResetSerializer(
        data=request.data, context={'email': email, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ContactAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        contact_list = Contact.objects.all()
        contact_serializers = Contactserializers(contact_list, many=True)
        return Response(contact_serializers.data)

    def post(self, request, format=None):
        contact_serializers = Contactserializers(data=request.data)
        if contact_serializers.is_valid():
            contact_serializers.save()
            return Response(contact_serializers.data, status=status.HTTP_201_CREATED)
        return Response(contact_serializers.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
class CreateBlogView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

# Detail View for retrieving a single blog post
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'id'

class Video_conference_appointmentAPIView(APIView):
    def get(self, request, format=None):
        Video_conference_appointment_list = Video_conference_appointment.objects.all()
        Video_conference_appointment_serializers = Video_conference_appointmentSerializer(Video_conference_appointment_list, many=True)
        return Response(Video_conference_appointment_serializers.data)

    def post(self, request, format=None):
        Video_conference_appointment_serializers = Video_conference_appointmentSerializer(data=request.data)
        if Video_conference_appointment_serializers.is_valid():
            Video_conference_appointment_serializers.save()
            return Response(Video_conference_appointment_serializers.data, status=status.HTTP_201_CREATED)
        return Response(Video_conference_appointment_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateGovernment_SupportView(generics.ListCreateAPIView):
    queryset = Government_Support.objects.all()
    serializer_class = Government_SupportSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

# Detail View for retrieving a single Government_Support post
class Government_SupportDetailView(generics.RetrieveAPIView):
    queryset = Government_Support.objects.all()
    serializer_class = Government_SupportSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    lookup_field = 'SupportId'


class VideoConferenceAppointmentView(APIView):
    def post(self, request):
        serializer = Video_conference_appointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve all video conference appointments from the database
        appointments = Video_conference_appointment.objects.all()
        serializer = Video_conference_appointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_Video_conference_appointment(request, id):
    try:
        Video_conference_appointments = Video_conference_appointment.objects.get(id=id)
        Video_conference_appointments.delete()
        return JsonResponse({'message': 'Video_conference_appointments deleted successfully'}, status=204)
    except Video_conference_appointment.DoesNotExist:
        return JsonResponse({'message': 'Video_conference_appointments not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

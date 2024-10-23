from django.urls import path
from .views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('update_profile/<str:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<email>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('delete_user/', delete_user, name='delete_user'),
    path('Contact/feedback', ContactAPIView.as_view()),
    path('blogs/', CreateBlogView.as_view(), name='blog-list-create'),
    path('blogs/<int:id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('Video_conference_appointment/', Video_conference_appointmentAPIView.as_view()),
    path('Government_Support/', CreateGovernment_SupportView.as_view(), name='Government_Support-list-create'),
    path('Government_Support/<str:SupportId>/', Government_SupportDetailView.as_view(), name='Government_Support-detail'),
    path('video-conference-appointment/', VideoConferenceAppointmentView.as_view(), name='video-conference-appointment'),
    path('delete_Video_conference_appointment/<int:id>/', delete_Video_conference_appointment, name='delete_Video_conference_appointment'),    
]
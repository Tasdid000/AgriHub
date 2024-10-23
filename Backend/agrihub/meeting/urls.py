from django.urls import path
from .views import ZoomAuthorizeView, ZoomCallbackView, CreateZoomMeetingView

urlpatterns = [
    path('zoom/authorize/', ZoomAuthorizeView.as_view(), name='zoom_authorize'),
    path('zoom/callback/', ZoomCallbackView.as_view(), name='zoom_callback'),
    path('zoom/create-meeting/', CreateZoomMeetingView.as_view(), name='zoom_create_meeting'),
]

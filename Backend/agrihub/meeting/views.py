from django.shortcuts import redirect
from rest_framework.views import APIView
from django.conf import settings
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework import status

class ZoomAuthorizeView(APIView):
    """
    Redirects the user to Zoom's OAuth authorization page.
    """
    def zoom_authorize(request):
        authorize_url = "https://zoom.us/oauth/authorize"
        client_id = "EyDKBIk3T7wY3bp07Fpig"
        redirect_uri = "http://127.0.0.1:8000/apiv2/user/zoom/callback/"
        
        # Build the full authorization URL
        full_authorize_url = f"{authorize_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
        
        return JsonResponse({'authorize_url': full_authorize_url})
    

def zoom_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    # Prepare the request to exchange the authorization code for an access token
    token_url = 'https://zoom.us/oauth/token'
    client_id = 'EyDKBIk3T7wY3bp07Fpig'
    client_secret = 'NKcmcsLZ0BL4RN1FShxjRLhfIX1jUyuv'
    redirect_uri = 'http://127.0.0.1:8000/apiv2/user/zoom/callback/'

    try:
        response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }, auth=(client_id, client_secret))

        token_data = response.json()

        if 'access_token' in token_data:
            return JsonResponse({"access_token": token_data['access_token']})
        else:
            return JsonResponse({"error": token_data}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


class CreateZoomMeetingView(APIView):
    """
    Creates a Zoom meeting using the Zoom API.
    Requires 'topic', 'start_time', and 'duration' in the request body.
    """
    def post(self, request):
        access_token = request.session.get('zoom_access_token')
        if not access_token:
            return Response({"error": "Zoom access token is missing."}, status=status.HTTP_401_UNAUTHORIZED)

        zoom_create_meeting_url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Extract meeting data from the request body
        meeting_data = {
            "topic": request.data.get("topic", "Default Meeting Title"),
            "type": 2,  # Scheduled meeting
            "start_time": request.data.get("start_time"),  # Format: YYYY-MM-DDTHH:MM:SSZ
            "duration": request.data.get("duration", 30),  # Duration in minutes
            "timezone": "UTC",
            "agenda": request.data.get("agenda", "Default Agenda"),
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False,
                "mute_upon_entry": True,
                "approval_type": 1,  # Automatically approve
            }
        }

        response = requests.post(zoom_create_meeting_url, json=meeting_data, headers=headers)

        if response.status_code == 201:
            return Response(response.json(), status=status.HTTP_201_CREATED)
        else:
            return Response(response.json(), status=response.status_code)

import jwt
import time
from django.conf import settings

def generate_zoom_signature(meeting_number, role):
    iat = int(time.time())  # current timestamp
    exp = iat + 60 * 5  # Signature valid for 5 minutes

    payload = {
        'sdkKey': settings.ZOOM_SDK_KEY,
        'mn': meeting_number,
        'role': role,
        'iat': iat,
        'exp': exp,
        'appKey': settings.ZOOM_SDK_KEY,
        'tokenExp': exp
    }

    signature = jwt.encode(payload, settings.ZOOM_SDK_SECRET, algorithm='HS256')
    return signature.decode('utf-8') if isinstance(signature, bytes) else signature

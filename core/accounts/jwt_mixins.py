import jwt
from datetime import datetime, timedelta
from django.conf import settings

def create_jwt_token(user_id):
    # Set the expiration time to one day from the current time
    expiration_time = datetime.utcnow() + timedelta(days=1)

    # Create the payload containing the user ID and expiration time
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }

    # Generate the JWT token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # Return the JWT token
    return token

def decode_jwt_token(self,token):
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_payload['user_id']
            # Return the user ID
            return user_id
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.DecodeError:
            # Handle invalid token
            return None
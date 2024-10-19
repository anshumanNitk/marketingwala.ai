# Make sure to install firebase-admin with: 
# sudo pip install firebase-admin
#auth2.0 token
#ya29.a0AcM612wpwXj6Pi4xdhBeYNkFe3lgDh9Ydn28ol1X4fQ3oSkAOhh85IkT7Rqvx1lFnzqYY_6M5X3xtpVqyJ1sjFJRqf8EbPIiPRLHoExi0SWRyr3qFmVqfM7nmS5MdntIJf9JSomiYyhpvzj0SJG-BWJ--BAtH-QvITs_2UXdaCgYKAe4SARASFQHGX2MiRP7nIAShQLvGaMP1olXArw0175
import firebase_admin
from firebase_admin import credentials, messaging

# Initialize the Firebase app with the service account key
cred = credentials.Certificate("/Users/mohammedarfath/PROGRAMING/AllPython/mlh_hack/marketfcm2-firebase-adminsdk-q4z7u-e91f2f94ef.json")
firebase_admin.initialize_app(cred)

# This registration token comes from the client FCM SDKs.
registration_token = 'ehpsqpATS-OwHdCToPkffh:APA91bF_IgAv-x2LgfFRbDkIXvFflCFeVsm5arY90KSvBBYyc6gchS98klTCNGjgzyo6UBEtFdDR1b76hKs8Qj3i-JRlNyFdA51IeZABpWRoDRsAI2aJnc0EIEgcBhJ8SozU3weWi_73'

# Function to send a single push notification
def sendPush(title, msg, registration_token, dataObject=None):
    # Create a single message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,  # Optional data payload
        token=registration_token,  # Single registration token
        android=messaging.AndroidConfig(
            priority='high'  # Set priority to high for immediate delivery
        )
    )

    # Send the message
    try:
        response = messaging.send(message)
        print('Successfully sent message:', response)
    except Exception as e:
        print('Error sending message:', e)

# Example usage
sendPush("Hi", "This is my next message arfathv2", registration_token)

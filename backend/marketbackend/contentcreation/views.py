import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import scheduleData
from .serializers import CampaignSerializer
from .serializers import ScheduleDataSerializer
import base64
from io import BytesIO
from PIL import Image
import os
import traceback
import firebase_admin
from firebase_admin import credentials, messaging
import boto3
import requests


def decode_base64_image(encoded_image):
    """
    Decodes the base64 image and returns the image binary (or saves it temporarily).
    """
    # Decode the base64 string
    image_data = base64.b64decode(encoded_image.split(',')[1])  # Remove the data URI scheme
    return image_data

def save_image(decoded_image, filename="uploaded_image.png"):
    """
    Save the decoded image to a temporary file.
    """
    with open(filename, "wb") as f:
        f.write(decoded_image)
    return filename

openai.api_key = settings.OPENAI_API_KEY

class CampaignContentGeneratorView(APIView):
    def post(self, request):
        
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Extract data from the request
        content_preferences = request.data.get('contentPreferences', {})
        campaign_scheduling = request.data.get('campaignScheduling', {})
        customer_data = request.data.get('customerData', {})
        brand_guidelines = request.data.get('brandGuidelines', {})
        
        uploaded_images = content_preferences.get('uploadedImages', [])
        if uploaded_images:
            base64_image = uploaded_images[0]
            decoded_image = decode_base64_image(base64_image)
            image_filename = save_image(decoded_image)  # Save the decoded image
        else:
            image_filename = "no image provided"
        
        
        
        


        # Build prompts for Variation 1 and 2
        variation1_prompt = f"""
    Create a captivating image for a marketing campaign targeting {content_preferences.get('targetAudience', 'a broad audience')}. 
    This campaign should resonate with their interests in {customer_data.get('interests', 'general topics of interest')}. 
    The behavior data for this audience spans from {customer_data.get('behaviorDateRange', {}).get('start', 'no start date')} 
    to {customer_data.get('behaviorDateRange', {}).get('end', 'no end date')}, 
    and the engagement data is as follows: {customer_data.get('engagementData', 'unspecified')}.

    The visuals must comply with brand guidelines: 
    - put this Logo on right top corner: {'none' if brand_guidelines.get('logo') is None else "no image"}
    - Colors: {brand_guidelines.get('colors', 'standard brand colors')}
    - Fonts: {brand_guidelines.get('fonts', 'standard fonts')}
    - Key Messages: {brand_guidelines.get('keyMessages', 'emphasizing product quality and reliability')}
    - Tone: {brand_guidelines.get('tone', 'playful and engaging')}

    For the content, ensure the creative style is {content_preferences.get('creativeStyle', 'modern')}, 
    focusing on {content_preferences.get('postTheme', 'product-focused')} themes. 
    Include {content_preferences.get('characters', 'necessary characters')} in the visuals, supported by {content_preferences.get('backgroundInfo', 'relevant background information')}. 
    Add additional elements like {content_preferences.get('additionalItems', 'props and items to enhance the product')}, 
    and incorporate the following text in the post: '{content_preferences.get('inPostText', 'high-quality product on display')}'.
    
    Ensure the output image have similarities with this: {image_filename}.

    The overall visual aesthetic should be {content_preferences.get('visualAesthetic', 'clean and visually striking')}, 
    featuring a color scheme of {content_preferences.get('colorScheme', 'on-brand colors')}, 
    typography: {content_preferences.get('typography', 'aligned with brand fonts')}, 
    and textures/patterns that follow {content_preferences.get('texturePatterns', 'minimalist style')}. 
    Make sure to combine text and images to create a compelling visual narrative.
"""
        print(variation1_prompt)
        
        
        
        variation2_prompt = f"""
    Create a captivating image for a marketing campaign targeting {content_preferences.get('targetAudience', 'a broad audience')}. 
    This campaign should resonate with their interests in {customer_data.get('interests', 'general topics of interest')}. 
    The behavior data for this audience spans from {customer_data.get('behaviorDateRange', {}).get('start', 'no start date')} 
    to {customer_data.get('behaviorDateRange', {}).get('end', 'no end date')}, 
    the Previous engagement data is as follows: {customer_data.get('engagementData', 'unspecified')}, based on this data try to improve the generation.

    The visuals must comply with brand guidelines: 
    - put this Logo on right top corner: {'none' if brand_guidelines.get('logo') is None else "no image"}
    - Colors: {brand_guidelines.get('colors', 'standard brand colors')}
    - Fonts: {brand_guidelines.get('fonts', 'standard fonts')}
    - Key Messages: {brand_guidelines.get('keyMessages', 'emphasizing product quality and reliability')}
    - Tone: {brand_guidelines.get('tone', 'playful and engaging')}

    For the content, ensure the creative style is {content_preferences.get('creativeStyle', 'modern')}, 
    focusing on {content_preferences.get('postTheme', 'product-focused')} themes. 
    Include {content_preferences.get('characters', 'necessary characters')} in the visuals, supported by {content_preferences.get('backgroundInfo', 'relevant background information')}. 
    Add additional elements like {content_preferences.get('additionalItems', 'props and items to enhance the product')}, 
    and incorporate the following text in the post: '{content_preferences.get('inPostText', 'high-quality product on display')}'.
    
     Ensure the output image have similarities with this: {image_filename}.

    The overall visual aesthetic should be {content_preferences.get('visualAesthetic', 'clean and visually striking')}, 
    featuring a color scheme of {content_preferences.get('colorScheme', 'on-brand colors')}, 
    typography: {content_preferences.get('typography', 'aligned with brand fonts')}, 
    and textures/patterns that follow {content_preferences.get('texturePatterns', 'minimalist style')}. 
    Make sure to combine text and images to create a compelling visual narrative.
"""

        try:
            # Generate images for Variation 1
            response_variation1 = client.images.generate(
                model="dall-e-3",
                prompt=variation1_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_variation1_urls = [image.url for image in response_variation1.data]
            
            # Generate caption for Variation 1
            caption_variation1_prompt = f"Write an engaging Instagram caption for the following: {variation1_prompt}"
            caption_response1 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative social media marketer."},
                    {"role": "user", "content": caption_variation1_prompt}
                ]
            )
            caption_variation1 = caption_response1.choices[0].message.content

            # Generate images for Variation 2
            response_variation2 = client.images.generate(
                model="dall-e-3",
                prompt=variation2_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_variation2_urls = [image.url for image in response_variation2.data]

            # Generate caption for Variation 2
            caption_variation2_prompt = f"Write an engaging Instagram caption for the following: {variation2_prompt}"
            caption_response2 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative social media marketer."},
                    {"role": "user", "content": caption_variation2_prompt}
                ]
            )
            caption_variation2 = caption_response2.choices[0].message.content

            # Return the generated content for both variations
            return Response({
                "variation1": {
                    "images": image_variation1_urls,
                    "caption": caption_variation1
                },
                "variation2": {
                    "images": image_variation2_urls,
                    "caption": caption_variation2
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            full_traceback = traceback.format_exc()  # Capture the full traceback
            print(f"Error: {error_message}\nTraceback: {full_traceback}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class SubmitUpdatedCampaignView(APIView):
    
    def post(self, request):
        # Step 1: Download the image from Azure Blob URL
        azure_image_url = request.data.get('imageUrl')  # URL provided in the request data
        try:
            response = requests.get(azure_image_url)
            response.raise_for_status()  # Raise exception if there's an issue
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to download image from Azure: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Process the image with PIL and save it locally as 'AImarket.jpeg'
        local_file_name = 'AImarket.jpeg'
        try:
            image = Image.open(BytesIO(response.content))

            # Convert image to RGB (JPEG doesn't support transparency)
            image.convert('RGB').save(local_file_name, 'JPEG')
        except Exception as e:
            return Response({"error": f"Failed to process image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Upload the local JPEG image to S3
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_REGION)

        s3_bucket_name = 'marketwala2'
        s3_file_name = 'AImarket.jpeg'  # Fixed file name for S3
        
        
        try:
            # Upload the locally saved file to S3
            with open(local_file_name, 'rb') as f:
                s3.upload_fileobj(f, s3_bucket_name, s3_file_name, ExtraArgs={'ACL': 'public-read'})

            # Generate public URL for the S3 image
            s3_image_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_file_name}"
        except Exception as e:
            return Response({"error": f"Failed to upload image to S3: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            # Clean up by deleting the local file
            if os.path.exists(local_file_name):
                os.remove(local_file_name)

        url = "https://graph.facebook.com/v21.0/434878196379802/photos"
        # Parameters for the POST request
        params = {
            "url": f"https://marketwala2.s3.ap-south-1.amazonaws.com/{s3_file_name}",  # URL of the image to be posted
            "caption": f"{request.data.get('caption')}",
            "access_token": "EAAIGTr46jE8BO7PyhuPKlriiZCfZCjYbf8s79678E5YpwZCIIdP8Uh1oc6PNhdB4ZBZCZB3jqtr6tEebk3bWcPMZBymA7wDg3876Q9hX7tx7vn3ZCbDLEzFVu5T3vsn7YBY0K8UMQNVJEV5ZBU3MfqIrCBLNrOzc8VuZBSe4sceiDgEHXZCZALcSDiXRwcTDzracXA40b8UGeVsr"
        }

        # Make the POST request
        response = requests.post(url, params=params)
        # Step 5: Save campaign data to the database
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save S3 URL with the campaign data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FetchCampaignDataView(APIView):
    def get(self, request):
        try:
            # Get all the scheduleData from the database
            schedule_data = scheduleData.objects.all()
            serializer = ScheduleDataSerializer(schedule_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.contrib import admin
from django.urls import path,include
from .views import CampaignContentGeneratorView
from .views import SubmitUpdatedCampaignView
from .views import FetchCampaignDataView





urlpatterns = [
    path('generate-campaign-post/',CampaignContentGeneratorView.as_view(), name='generate-campaign-post'),
    path('submit-updated-campaign/', SubmitUpdatedCampaignView.as_view(), name='submit-updated-campaign'),
    path('get-image/', FetchCampaignDataView.as_view(), name='fetch-campaign-data'),

]
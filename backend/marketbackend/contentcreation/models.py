from django.db import models

# Create your models here.

# Create your models here.
class scheduleData(models.Model):
    imageUrl = models.URLField(max_length=2083)
    caption=models.TextField()
    campaignScheduling=models.JSONField()
    
    
    def __str__(self):
        return self.caption

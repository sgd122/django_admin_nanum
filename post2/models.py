from django.db import models

# Create your models here.
class Post2(models.Model):
    post_heading = models.CharField(max_length=200)
    post_text = models.TextField()

    def __str__(self):
        return self.post_heading    

class Like(models.Model):
    post2 = models.ForeignKey(Post2,on_delete=models.CASCADE)        
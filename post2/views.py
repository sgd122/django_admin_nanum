from django.shortcuts import render
from .models import Post2, Like
from django.http import HttpResponse

def index(request):
        posts = Post2.objects.all()  # Getting all the posts from database
        return render(request, 'post2/index.html', { 'posts': posts })

def likePost(request):
    if request.method == 'GET':
           post_id = request.GET['post_id']
           likedpost = Post2.obejcts.get(pk=post_id) #getting the liked posts
           m = Like(post=likedpost) # Creating Like Object
           m.save()  # saving it to store in database
           return HttpResponse("Success!") # Sending an success response
    else:
           return HttpResponse("Request method is not a GET")
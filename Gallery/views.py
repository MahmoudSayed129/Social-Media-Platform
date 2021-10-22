import json
from typing import Text
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Comments, Posts, Likes, Follwers

@login_required(login_url='login')
def index(request):
    posts = Posts.objects.all().order_by('id').reverse()
    p = []
    for post in posts:
        a = {}
        a["post"] = post
        a["num_likes"] = Likes.objects.filter(post_id = post.id).count()
        a["liked"]= Likes.objects.filter(user = request.user, post_id=post.id).count() > 0
        a["num_comments"] = Comments.objects.filter(post_id=post.id).count()
        p.append(a)
    paginator = Paginator(p, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "Gallery/index.html",{"page_obj":page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Gallery/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Gallery/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if not (username and password and email):
            return render(request, "Gallery/register.html", {
                "message": "You must Enter the (Username, Email Adress and Password)."
            })
        if password != confirmation:
            return render(request, "Gallery/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if len(request.FILES) != 0:
                user = User.objects.create_user(username, email, password, profile_img=request.FILES["profile_img"])
            else:
                user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Gallery/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Gallery/register.html")
@login_required(login_url='login')
def add_post(request):
    if len(request.FILES) == 0 and not request.POST.get('post'):
        posts = Posts.objects.all().order_by('id').reverse()
        p = []
        for post in posts:
            a = {}
            a["post"] = post
            a["num_likes"] = Likes.objects.filter(post_id = post.id).count()
            a["liked"]= Likes.objects.filter(user = request.user, post_id=post.id).count() > 0
            a["num_comments"] = Comments.objects.filter(post_id=post.id).count()
            p.append(a)
        paginator = Paginator(p, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "Gallery/index.html",{"page_obj":page_obj, "error":True})
    post = Posts()
    post.text = request.POST.get('post')
    post.user = request.user
    post.username = request.user.username
    if len(request.FILES) != 0:
        post.post = request.FILES['img']
    post.save()
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def profile(request, person):
    you = False
    if request.user.username == person:
        you = True
    is_following = False
    following = 0
    followers = 0
    follows = Follwers.objects.all()
    for follow in follows:
        if follow.follower == request.user.username and follow.follwing == person:
            is_following = True
        if follow.follower == person:
            following += 1
        if follow.follwing == person:
            followers += 1
    posts = Posts.objects.filter(username=person).order_by('id').reverse()
    p = []
    for post in posts:
        a = {}
        a["post"] = post
        a["num_likes"] = Likes.objects.filter(post_id = post.id).count()
        a["liked"]= Likes.objects.filter(user = request.user, post_id=post.id).count() > 0
        a["num_comments"] = Comments.objects.filter(post_id=post.id).count()
        p.append(a)
    paginator = Paginator(p, 10)
    # paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    img_url = ""
    if User.objects.get(username = person).profile_img:
        img_url = User.objects.get(username = person).profile_img.url
    return render(request, "Gallery/profile.html", {"img_url":img_url, "person":person, "page_obj":page_obj, "is_following":is_following, "you":you, "followers":followers, "following":following})
@login_required(login_url='login')
def following(request):
    followings = Follwers.objects.filter(follower=request.user.username)
    ps = Posts.objects.all()
    posts = []
    for p in ps:
        for following in followings:
            if p.username == following.follwing:
                posts.append(p)
    p = []
    for post in posts:
        a = {}
        a["post"] = post
        a["num_likes"] = Likes.objects.filter(post_id = post.id).count()
        a["liked"]= Likes.objects.filter(user = request.user, post_id=post.id).count() > 0
        a["num_comments"] = Comments.objects.filter(post_id=post.id).count()
        p.append(a)
    paginator = Paginator(p, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "Gallery/index.html",{"page_obj":page_obj, "following_page":True})
@login_required(login_url='login')
def follow(request, person):

    new_following = Follwers.objects.create(
        follwing = person,
        follower = request.user.username
    )
    return HttpResponseRedirect(reverse("profile", args=(person,)))
@login_required(login_url='login')
def unfollow(request, person):
    following = Follwers.objects.get(follwing = person, follower = request.user.username)
    following.delete()
    return HttpResponseRedirect(reverse("profile", args=(person,)))

@login_required(login_url='login')
@csrf_exempt
def edit_post(request, post_id):
    post = Posts.objects.get(id=post_id)
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    else:
        data = json.loads(request.body)
        if data.get("post") is not None:
            post.text = data["post"]
        post.save()
        return HttpResponse(status=200)

@login_required(login_url='login')
def delete_post(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def view_post(request, post_id):
    post = Posts.objects.get(pk = post_id)
    num_likes = Likes.objects.filter(post_id = post_id).count()
    liked = False
    if Likes.objects.filter(user = request.user, post_id=post_id).count() > 0:
        liked = True
    comments = Comments.objects.filter(post_id=post_id).order_by('id').reverse()
    num_comments = comments.count()
    return render(request, "Gallery/view_post.html", { "num_comments":num_comments, "comments":comments, "post":post, "num_likes":num_likes, "liked":liked})

@login_required(login_url='login')
@csrf_exempt
def like_post(request, post_id):
    new_like = Likes(
        post_id = post_id,
        user = request.user
    )
    new_like.save()
    return HttpResponse(status=200)

@login_required(login_url='login')
@csrf_exempt
def unlike_post(request, post_id):
    like = Likes.objects.get(post_id = post_id,user = request.user)
    like.delete()
    return HttpResponse(status=200)

def add_comment(request):
    post_id = int(request.POST.get("post_id"))
    comment_content = request.POST.get("comment")
    if  comment_content :
       new_comment = Comments.objects.create(
        comment = comment_content,
        user = request.user,
        post_id = post_id
       ) 
       return HttpResponseRedirect(reverse("view_post", args=(post_id,)))
    else:
        post = Posts.objects.get(pk = post_id)
        num_likes = Likes.objects.filter(post_id = post_id).count()
        liked = False
        if Likes.objects.filter(user = request.user, post_id=post_id).count() > 0:
            liked = True
        comments = Comments.objects.filter(post_id=post_id).order_by('id').reverse()
        num_comments = comments.count()
        return render(request, "Gallery/view_post.html", {"error":True, "num_comments":num_comments, "comments":comments, "post":post, "num_likes":num_likes, "liked":liked})

@login_required(login_url='login')
def edit_image(request):
    person = request.POST["person"]
    if len(request.FILES) != 0:
        new_img = request.FILES['img']
        user = User.objects.get(username = person)
        user.profile_img = new_img
        user.save()
        text = f"{person} changed his profile picture"
        new_post = Posts.objects.create(post=new_img, text=text, user=request.user, username=person)
    return HttpResponseRedirect(reverse("profile", args=(person,)))

@login_required(login_url='login')
def edit_post_photo(request):
    post_id = request.POST["post_id"]
    if len(request.FILES) != 0:
        new_img = request.FILES['img']
        post = Posts.objects.get(id = post_id)
        post.post = new_img
        post.save()
    return HttpResponseRedirect(reverse("view_post", args=(post_id,)))

def delete_profile_img(request):
    person = request.POST["person"]
    user = User.objects.get(username = person)
    user.profile_img = None
    user.save()
    return HttpResponseRedirect(reverse("profile", args=(person,)))

def delete_post_img(request):
    post_id = request.POST["post_id"]
    post = Posts.objects.get(id = post_id)
    post.post = None
    post.save()
    return HttpResponseRedirect(reverse("view_post", args=(post_id,)))
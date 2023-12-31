from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator


from .models import User, Post, Like, Subscription
from .forms import PostForm


def index(request):

    if request.method == "POST":
        posttext = request.POST["text"]
        author = User(request.user.id)
        Post(text=posttext, author=author).save()
        
    elif request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=data["post"])

        if data["likeButton"]:
            try:
                like = post.plikes.get(author=request.user.id)
            except ObjectDoesNotExist:
                Like(post=Post(data["post"]),
                    author=User(request.user.id)).save()
                likes = post.plikes.count()
                return JsonResponse({"likes": likes}, status=201)
            else:
                like.delete()
                likes = post.plikes.count()
                return JsonResponse({"likes": likes, "deleted": True},
                                    status=202)
        if data["saveChangesButton"]:
            post.text = data["text"]
            post.save()
            return JsonResponse({"text": data["text"]}, status=203)
        
    p = Paginator(Post.objects.order_by("-date").all(), 3, 2)
    page = request.GET.get("page")
    page_view = p.get_page(page)

    return render(request, "network/index.html",
                    {"post_form": PostForm(), "page_view": page_view})


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def load_profile(request, user_id, user_name):
    user_object = User.objects.get(pk=user_id)

    if request.method == "PUT":
        try:
            my_subscription = Subscription.objects.get(
                follower=User(pk=request.user.id))
            try:
                my_subscription.subscribers.get(pk=user_id)
                my_subscription.subscribers.remove(user_object)
                subscription = 1
            except ObjectDoesNotExist:
                my_subscription.subscribers.add(user_object)
                subscription = 0
        except ObjectDoesNotExist:
            my_subscription = Subscription(follower=User(pk=request.user.id))
            my_subscription.save()
            my_subscription.subscribers.add(user_object)
            subscription = 0

        user_object_followers = user_object.followers.count()
        return JsonResponse({"subscription": subscription,
                             "user_object_followers": user_object_followers}, status=201)

    my_subscriptions_list = Subscription.objects.filter(
        follower=request.user.id)
    
    p = Paginator(user_object.myposts.all().order_by("-date"), 3, 2)
    page = request.GET.get("page")
    page_view = p.get_page(page)
    
    return render(request, "network/profile.html",
                  {"user_object": user_object,
                   "my_subscriptions_list": my_subscriptions_list,
                   "page_view": page_view})


def load_following(request):
    allposts = []
    try:
        my_subscription = Subscription.objects.get(
            follower=User(pk=request.user.id))
        my_subscribers = my_subscription.subscribers.all()

        for subscriber in my_subscribers:
            subscriber_posts = subscriber.myposts.all()
            for post in subscriber_posts:
                allposts.append(post)

    except ObjectDoesNotExist:
        return render(request, "network/following.html",
                      {"message": "You don't have following!"})

    def myFunc(post):
        return post.date
    allposts.sort(reverse=True, key=myFunc)
    
    p = Paginator(allposts, 3, 2)
    page = request.GET.get("page")
    page_view = p.get_page(page)

    return render(request, "network/following.html",
                  {"page_view": page_view})

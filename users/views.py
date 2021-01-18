from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.models import CustomUser, Follow
from tweets.models import Tweet
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse


def home(request):

    search_query = request.GET.get('search', '')
    if search_query:
        tweets = Tweet.objects.filter(text__icontains=search_query)
    else:
        tweets = Tweet.objects.all()

    return render(request, 'home.html', {'tweets': tweets})


def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get data from the form and authenticate, then login
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def profileupdate(request, username):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.cleaned_data.get('bio')
            form.cleaned_data.get('location')
            form.cleaned_data.get('website')
            form.cleaned_data.get('profilepicture')
            form.cleaned_data.get('background_img')
            form.save()
            return redirect('useroverview', username=request.user.username)

    else:
        form = CustomUserChangeForm()
    return render(request, 'userupdate.html', {'form': form})


def useroverview(request, username):
    userprofile = get_object_or_404(CustomUser, username=username)
    followers = Follow.objects.filter(following=userprofile).count()
    following = Follow.objects.filter(follower=userprofile).count()

    tweets = userprofile.tweets.all()
    return render(
        request,
        'useroverview.html',
        {
            'userprofile': userprofile,
            'tweets': tweets,
            'followers': followers,
            'following': following
        }
    )


def userfollowers(request, username):
    user = get_object_or_404(CustomUser, username=username)
    followers = Follow.objects.filter(following=user).all()

    return render(request, 'userfollowers.html', {'followers': followers, 'user': user})


def userfollowing(request, username):
    user = get_object_or_404(CustomUser, username=username)
    following = Follow.objects.filter(follower = user).all()

    return render(request, 'userfollowing.html', {'following': following, 'user': user})


@login_required
def follow(request):
    res = {}
    if request.method == 'GET':
        userid = request.GET['userid']
        following = get_object_or_404(CustomUser, pk=userid)
        follower = request.user

        if Follow.objects.filter(following=following, follower=follower).exists():
            Follow.objects.filter(following=following, follower=follower).delete()
            res['delete'] = True

        else:
            Follow.objects.create(
                following=following,
                follower=follower
            )
            res['delete'] = False

        res['newFollowerCount'] = Follow.objects.filter(following=following).count()

        return JsonResponse(res, content_type='application/json')

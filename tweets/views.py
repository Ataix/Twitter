from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet, Comment, Likes
from django.http import HttpResponse, JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime


@login_required
def newtweet(request):
    res = {}
    if request.method =='POST':
        text = request.POST.get('text')
        user = request.user

        res['text'] = text
        res['username'] = user.username

        tweet = Tweet.objects.create(
            user = request.user,
            text = text,

        )

        res['tweetdate'] = naturaltime(tweet.created_date)
        res['tweetuser'] = tweet.user.username
        res['tweetpk'] = tweet.pk
        res['tweetlikecount'] = tweet.liked_tweet.count()

        res['tweeturl'] = tweet.get_absolute_url()
        res['userurl'] = user.get_absolute_url()

        return JsonResponse(res, content_type='application/json')

    return render(request, 'newtweet.html')


def tweetoverview(request, tweet_id, username):
    tweet = Tweet.objects.get(pk=tweet_id)
    request.session['tweetid'] = tweet.pk
    return render(request, 'tweetoverview.html', {'tweet': tweet})


@login_required
def newcomment(request):
    res = {}
    if request.method =='POST':
        text = request.POST.get('text')
        user = request.user

        res['text'] = text
        res['username'] = user.username

        comment = Comment.objects.create(
            user = user,
            text = text,
            tweet = Tweet.objects.get(pk=request.POST.get('tweetid'))
        )

        res['createddate'] = naturaltime(comment.created_date)
        res['userurl'] = user.get_absolute_url()

        return JsonResponse(res, content_type='application/json')

    return render(request, 'newtweet.html')


@login_required
def liketweet(request):
    res = {}
    if request.method == 'GET':
        tweetid = request.GET['tweet_id']
        tweet = get_object_or_404(Tweet, pk = tweetid)
        user = request.user

        if Likes.objects.filter(tweet=tweet, user=user).exists():
            Likes.objects.filter(tweet=tweet, user=user).delete()
            res['delete'] = True

        else:
            Likes.objects.create(
                user = user,
                tweet = tweet,
            )

        res['likecount'] = tweet.get_likes()

        return JsonResponse(res, content_type='application/json')

    return render(request, 'newtweet.html')

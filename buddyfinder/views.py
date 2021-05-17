from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import User
from django.shortcuts import render, redirect
from .forms import PreferencesForm
from .forms import MessageForm
from django.urls import reverse
from .models import Message
import os

import spotipy
import spotipy.util as util
from spotipy import oauth2

scope = 'user-top-read'
SPOTIPY_CLIENT_ID = '9a6d36bcbce0438f82823009c1b28b05'
SPOTIPY_CLIENT_SECRET = 'ed7d6bb39ad14ce082bbc740d2742384'
SPOTIPY_REDIRECT_URI = 'http://hoosrooming.herokuapp.com/spotify2'


def index(request):
    return render(request, 'buddyfinder/index.html')


class PreferencesCreate(CreateView):
    model = User
    form_class = PreferencesForm
    template_name = 'buddyfinder/user_form2.html'


def get_preferences(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    if request.method == 'POST':
        user.phone_number = request.POST.get('phone_number')
        user.bio = request.POST.get('bio')
        user.cleanliness_level = request.POST.get('cleanliness_level')
        user.lease = request.POST.get('lease')
        user.budget = int(request.POST.get('budget'))
        # Casting to int because data is being passed as a str
        user.noise_level = request.POST.get('noise_level')
        user.morning_preference = request.POST.get('morning_preference')
        if request.FILES.get('image'):
            user.image = request.FILES.get('image')
        user.save()
        user.score_all()
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    form = PreferencesCreate()
    return render(request, 'buddyfinder/user_form.html', {'form': form})


def get_matches(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    match_list = user.get_scores()
    fav_list = user.get_favorites()
    pend_list = user.get_pending()
    if request.method == 'POST':
        user2 = request.POST.get('user')
        user.manage(user2[1:], user2[0])
        return HttpResponseRedirect(reverse('buddyfinder:matching'))
    return render(request, 'buddyfinder/matches.html', {'dict': match_list, 'fav': fav_list, 'pend': pend_list})


def next_offset(n):
    try:
        return int(n['next'].split('?')[1].split('&')[0].split('=')[1])
    except ValueError:
        return None
    except AttributeError:
        return None
    except TypeError:
        return None


def spotify(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    # token = util.prompt_for_user_token(username, scope)
    # print(token)
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope)
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    total = []
    results = sp.current_user_top_tracks(limit=5)
    next = next_offset(results)

    albums = []
    for r in results['items']:
        albums.append(r)

    if len(albums) != 0:
        spName = albums[0]['name']
        spArtist = albums[0]['artists'][0]['name']
        spLink = albums[0]['external_urls']['spotify']

        # save info to model
        user = request.user
        user.spotify_song = spName
        user.spotify_artist = spArtist
        user.spotify_link = spLink
        user.save()
        # delete cached file as info is saved in database
        os.remove(".cache")
    else:
        return render(request, 'buddyfinder/index.html', {'message': "Error"})

    return render(request, 'buddyfinder/index.html')


def spotify2(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    token = 'http://localhost:8000/buddyfinder/spotify2/?{}'.format(
        request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope)
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
    return render(request, 'buddyfinder/spotify.html')


class MessageCreate(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'buddyfinder/message.html'


def get_messages(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    if request.method == 'POST':
        user.sender = request.POST.get('sender')
        user.receiver = request.POST.get('receiver')
        user.msg_content = request.POST.get('ms')
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    form = MessageCreate()
    return render(request, 'buddyfinder/message.html', {'form': form})


# ************************************************************************
#   Title: Instagram clone in Django
#   Author: Bryon Lara
#   Date: April 18, 2021
#   URL: https://github.com/byronlara5/django_instagram_clone_youtube
#   Tutorial URL: https://www.youtube.com/watch?v=j1voZAmVw9I&t=1276s
# ************************************************************************
def get_inbox(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    messages = Message.get_messages(user=request.user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(
            user=request.user, receiver=message['user'])

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct
    }

    template = loader.get_template('buddyfinder/message.html')

    return HttpResponse(template.render(context, request))


# ************************************************************************
#   Title: Instagram clone in Django
#   Author: Bryon Lara
#   Date: April 18, 2021
#   URL: https://github.com/byronlara5/django_instagram_clone_youtube
#   Tutorial URL: https://www.youtube.com/watch?v=j1voZAmVw9I&t=1276s
# ************************************************************************
def get_directs(request, username):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, receiver__username=username)

    print(directs)
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    template = loader.get_template('buddyfinder/message.html')

    return HttpResponse(template.render(context, request))


# ************************************************************************
#   Title: Instagram clone in Django
#   Author: Bryon Lara
#   Date: April 18, 2021
#   URL: https://github.com/byronlara5/django_instagram_clone_youtube
#   Tutorial URL: https://www.youtube.com/watch?v=j1voZAmVw9I&t=1276s
# ************************************************************************
def send_direct(request):
    from_user = request.user
    if not from_user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    to_user_username = request.POST.get('to_user')
    content = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, content)
        return HttpResponseRedirect(reverse('buddyfinder:inbox', ))

    else:
        HttpResponseBadRequest()


# ************************************************************************
#   Title: Instagram clone in Django
#   Author: Bryon Lara
#   Date: April 18, 2021
#   URL: https://github.com/byronlara5/django_instagram_clone_youtube
#   Tutorial URL: https://www.youtube.com/watch?v=j1voZAmVw9I&t=1276s
# ************************************************************************
def start_conversation(request, username):
    from_user = request.user
    if not from_user.is_authenticated:
        return HttpResponseRedirect(reverse('buddyfinder:index'))
    content = request.user.username + ' ' + \
        'started a new conversation with' + ' ' + username
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('buddyfinder:index')
    if from_user != to_user:
        Message.send_message(from_user, to_user, content)
    return redirect('buddyfinder:inbox')

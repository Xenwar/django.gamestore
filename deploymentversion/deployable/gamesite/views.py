from django.shortcuts import render
from django.http import Http404, HttpResponse,HttpResponseRedirect,JsonResponse, HttpResponseNotFound
from members.models import Member
from gamecenter.models import Game,State,Transaction

import logging
logger = logging.getLogger(__name__)
#@user_passes_test(user_is_player,login_url="loggin_in")
def index(request):
    """
    Get total number of developers, players and games.
    Place holder until what to display is determined.
    """
    n_developers        =   Member.objects.all().count()
    n_players           =   State.objects.all().count()
    n_games             =   Game.objects.all().count()
    context ={
        'developer_counter'   :n_developers,
        'player_counter'      : n_players,
        'game_counter'        : n_games,
    }
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context['num_visits'] = num_visits
    context['messages'] = ['one','two']

    return render(
        request,
        'index.html',
        context,
    )


    '''
        transaction = Transaction.objects.filter(player=player).first()#
        transaction.is_success = True
        transaction.save()
                transaction = Transaction.objects.create(player=player, game=game,checksum=checksum[:24],is_success=False)

    '''
    
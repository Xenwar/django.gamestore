from django.shortcuts import render
from django.views import generic
from django.db import IntegrityError
import datetime
from members.models import Member, ActivationData
from .models import Game, State,Transaction
from .forms import GameAddForm,GameUpdateForm
from members.views import user_is_developer, user_is_player, register, logging_in, logging_out,activation
import uuid
from hashlib import md5
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger(__name__)
@login_required
@user_passes_test(user_is_developer,login_url="/")
def developer_games(request):
    developer = request.user
    game_list = []
    if developer.game_reverse_lookup.all() is not None:
        all_games = developer.game_reverse_lookup.all()
        for game in all_games:
            game_list.append(game)
        return render(request, 'gamecenter/game_list_developer.html', {'game_list': game_list})
    else:
        context = {}
        messages = []
        messages.append("No games found for current developer")
        context['messages'] = messages
        return render(
            request,
            'gamecenter/error.html',
            context,
        )

@login_required
@user_passes_test(user_is_player,login_url="/")
def player_games(request):
    game_list = []
    player = request.user
    if State.objects.filter(player=player).first() is not None:
        all_states = State.objects.filter(player=player) #entries for this player
        try:
            for state in all_states:
                game_list.append(state.game)
        except: #what to check ? game developer does not exist ?
            pass
        return render(request, 'gamecenter/game_list_player.html', {'purchased':state.purchase_date,'game_list': game_list})
    else:
        context = {}
        messages = []
        messages.append("No games found for current player")
        context['messages'] = messages
        return render(
            request,
            'gamecenter/error.html',
            context,
        )

def player_owns_game(pk, game_name):
    #get player, get game for comparison with what is in the state
    game   = Game.objects.get(game_name=game_name)
    player = Member.objects.get(pk=pk)    
    if State.objects.filter(player=player,game=game).first() is None:
        return False
    else:
        return True

def developer_owns_game(pk, game_name):
    #get player, get game
    #game      = Game.objects.get(game_name=game_name)
    developer = Member.objects.get(pk=pk)    
    for g in developer.game_reverse_lookup.all():
        if g.game_name == game_name:
            return True
    return False

@login_required
@user_passes_test(user_is_developer,login_url="/")
def addgame(request):
    logger.error('called method addgame!')
    form = GameAddForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("games")) #how about moving to his/her game list
    else:
        form = GameAddForm()
        return render(request,"gamecenter/gameadd.html",{'form':form})
@login_required
@user_passes_test(user_is_developer,login_url="/")
def updategame(request,game_name):
    if not developer_owns_game(request.user.pk,game_name):
        context = {}
        messages = []
        messages.append("Ownly owner is allowed to updated the game")
        context['messages'] = messages
        return render(
            request,
            'gamecenter/error.html',
            context,
        )
    instance = Game.objects.get(game_name=game_name)
    form = GameUpdateForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("games"))#
    else:
        form = GameUpdateForm(instance=instance)
        return render(request,"gamecenter/gamemodify.html",{'form':form})

        #same form for modifying
@login_required
@user_passes_test(user_is_developer,login_url="/")
def deletegame(request,game_name):
    if not developer_owns_game(request.user.pk,game_name):
        context = {}
        messages = []
        messages.append("Ownly owner is allowed to delete the game")
        context['messages'] = messages
        return render(
            request,
            'gamecenter/error.html',
            context,
        )
    instance = Game.objects.get(game_name=game_name)
    form = GameUpdateForm(request.POST, instance=instance)
    if form.is_valid():
        instance.delete()
        #form.save()
        return HttpResponseRedirect(reverse("developergames"))#
    else:
        form = GameUpdateForm(instance=instance)
        return render(request,"gamecenter/deletegame.html",{'form':form})
        #same form for modifying


@login_required
@user_passes_test(user_is_player,login_url="/")
@csrf_exempt
def play_game_view(request, game_name):
        #Access control
        if not player_owns_game(request.user.pk,game_name):
            context = {}
            messages = []
            messages.append("You need to purchase the game")
            context['messages'] = messages
            return render(
                request,
                'gamecenter/error.html',
                context,
            )
        #get player id and game name someway, from the session ?
        player_id = request.user.pk;
        logger.debug(player_id, '=================================')
        player =    Member.objects.get(pk=player_id) #an overkill to get the object, id is enough.
        game   =    Game.objects.get(game_name=game_name)

        game_url  = game.game_url

        context ={
            'player_id':player_id,
            'game_url' : game_url,
            'game_name': game_name,
            'player_id': player_id,
        }
        return render( 
            request,
            'gamecenter/playgame.html',
            context,
        )
def Calculating_the_checksum(request,pid,sid,secret_key,amount): #step 2 in the instruction, http://payments.webcourse.niksula.hut.fi/
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    logger.debug(checksum)
    return checksum


def verify_checksum(request,pid,ref,result,secret_key): #for comparison with what is returned from a succcessful transaction
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    logger.debug(checksum)
    return checksum

@login_required
@user_passes_test(user_is_player,login_url="/")
def purchase_game(request, game_name):
    pid = str(uuid.uuid4())[0:32] #random payment identifieer as in Transaction id.
    sid = "xenwar"  #fixed
    secret_key  = "3a93fa3784fb085d7debbcee8b25b4ff"#fixed
    game   = Game.objects.get(game_name=game_name)
    player = Member.objects.get(pk=request.user.pk)
    price  = game.price
    checksum = Calculating_the_checksum(request,pid,sid,secret_key,price)
    context ={
        'pid'       : pid,
        'sid'       : sid,
        'secret_key': secret_key,
        'checksum'  : checksum,
        'game_name' : game_name,
        'amount'    :price,
    }
    #We do not know the player yet since he/she has not paid yet.
    try:
        transaction = None
        #There is an upper limit on pid length
        #before success. 
        if Transaction.objects.filter(player=player,game=game).first() is None:
            #No transaction started in the past
            #then create it for the first time. 
            transaction = Transaction.objects.create(player=player, game=game,pid=pid[:24],is_success=False)

        #check if there exists half baked transaction, if found, re-use it. 
        elif Transaction.objects.filter(player=player,game=game).first().is_success == False:
             transaction = Transaction.objects.filter(player=player,game=game).first()
             transaction.pid = pid[:24]
             transaction.save() #not successful yet, just replace old pid with new one, prevents half transactions
        
        elif Transaction.objects.filter(player=player,game=game).first().is_success == True:
            context = {}
            context['messages'] =['You have already bought the game']
            return render( 
                request,
                'gamecenter/error.html',
                context,
            )
    except Exception as e:
        logger.error("game already bought or in process")
        return HttpResponseRedirect(reverse("games"))

    return render(
        request,
        'gamecenter/payment_request.html',
        context,
    )
@login_required
@user_passes_test(user_is_player,login_url="/")
def payment_success(request):
    player = Member.objects.get(pk=request.user.pk)
    context = {
        'pid'       : request.GET['pid'],
        'ref'       : request.GET['ref'],
        'result'    : request.GET['result'],
        'checksum'  : request.GET['checksum'],
    }
    pid                   = request.GET['pid']
    service_checksum      = request.GET['checksum']
    logger.debug(request.GET['pid'])
    #We now know the player has succeeded in purchasing the game.
    try:
        #verify check sum to prevent malacious purchase. 
        local_checksum  = verify_checksum(request,request.GET['pid'],request.GET['ref'],request.GET['result'],"3a93fa3784fb085d7debbcee8b25b4ff")
        #for comparison with what is returned from a succcessful transaction
        if local_checksum == service_checksum:
            logger.debug(local_checksum)
        else:
            raise Exception #somebody trying to by pass the payment service.

        #get transaction, should exist, unless some unlikely deletion of it occurs.  
        #PID IS NEEDED here
        #since there is no refernce to game. 
        if Transaction.objects.filter(player=player,pid=pid[:24]).first() is None:#get transaction
            logger.debug("could not find transaction")
            raise Exception #very very very unlikely
        #check if there exists half baked transaction, if found, re-use it. 
        elif Transaction.objects.filter(player=player,pid=pid[:24]).first().is_success == False:
            transaction = Transaction.objects.filter(player=player,pid=pid[:24]).first()
            transaction.is_success = True
            transaction.save() #successful yet.
            logger.debug("found transaction")
            #############Add the game to the player's property#############
            game   =    transaction.game
            print(game)
            print(player)
            if State.objects.filter(player=player,game=game).first() is None:
                print("state not found which is ok")
                #make entry does not exist, already taken care of in the transaction. But, just in case.
                state = State.objects.create(player=player, game=game,score=0,items="")
                if State.objects.filter(player=player,game=game).first() is None:
                    logger.debug("object Not created.")
                else:
                    game.sales_counter +=1 #keeps increasing forever.
                    game.save()

    except Exception as e:
        logger.error("A problem was encountered while adding a purchased game, contact the system admin",e)
        return HttpResponseRedirect(reverse("games"))

    return render(request,"gamecenter/payment_success.html", context)
#repeated three times, how to combine them ?
#get it once, and based on the 'result', render differetnt templates.
def payment_error(request):
    context = {
        'pid'       : request.GET['pid'],
        'ref'       : request.GET['ref'],
        'result'    : request.GET['result'],
        'checksum'  : request.GET['checksum'],
    }
    return render(request,"gamecenter/payment_error.html", context)

def payment_cancel(request):
    context = {
        'pid'       : request.GET['pid'],
        'ref'       : request.GET['ref'],
        'result'    : request.GET['result'],
        'checksum'  : request.GET['checksum'],
    }
    return render(request,"gamesite/payment_cancel.html", context)
class GameListView(generic.ListView):
    model = Game
    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        return context

class GameDetailView(generic.DetailView):
    model = Game

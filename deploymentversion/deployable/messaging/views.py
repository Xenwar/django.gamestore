from django.http import Http404, HttpResponse,HttpResponseRedirect,JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_protect #adding it everywhere.
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth.decorators import user_passes_test, login_required
from members.views import user_is_developer, user_is_player, register, logging_in, logging_out,activation

from members.models import Member
from gamecenter.models import Game, State
import json

from django.shortcuts import redirect
from django.shortcuts import render
from django.core.urlresolvers import reverse


from django.shortcuts import render_to_response
from django.contrib.auth.models import User


import logging
logger = logging.getLogger(__name__)
# Messaging related views
# would it be clearn to move them to a new app ? [callled: messaging]
@csrf_exempt
def error_to_game(request, game_name  ): #How to call this view from others, for usability.
    print("=========")
    cb = False
    try:
        callback = request.GET['callback']
        cb = True
    except:
        pass
    context = {}
    context['messageType']  = "ERROR"
    context['info']         ="Gamestate could not be loaded"
    logger.error('Gamestate could not be loaded!')
    if cb:
        result = '{0}({1})'.format(callback, context)
        return JsonResponse(json.dumps(result), safe=False)
    else:
        return JsonResponse(context, safe=False)
@csrf_exempt
def loadrequest_from_game(request, gamename): #game name is unique.
    player_id     = request.POST['player_id']
    cb = False
    try:
        callback = request.GET['callback']
        cb = True
    except:
        pass

    try:#Try to get current state of the game.
        game        =  Game.objects.get(game_name=gamename)     #get an actual game object and update it.
        user        =  Member.objects.get(pk=player_id)         #get the user from Members.
        state       =  State.objects.filter(player=user, game=game).first()  #filter further by game
        if state is not None:
            context = state.get_game_state() #game found but problem -> no worries context taken care of in the model
            context["messageType"] = "Success"
            context["info"] = "Game state sent to game"
        else:
            print("state not found")
            raise ValueError('Either game or player were not found. ')

    except Game.DoesNotExist: #What good is 'error_to_game'
        context =  {
            "messageType": "ERROR",
            "info": "Game does not exist on our system"
        }
        logger.error("Game does not exist")

    if cb:
        result = '{0}({1})'.format(callback, context)
        response = JsonResponse(json.dumps(result), safe=False) 
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = JsonResponse(context, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
    logger.debug("Sending state of game: ", game, "State: ", context)
    return response

#requires re-work
#issue: parsing json data, and request.is_ajax() returning false/none.
#solution , flatten structure before sending
#/////////////////////#/////////////////////#/////////////////////#////////REQUIRES CHANGE#/////////////////////#/////////////////////
@csrf_exempt
def score_from_game(request, gamename ): #game name is unique.
    #prone to attack, just change the id to your own,
    #a different kind of access control is neeeded.
    #how to validate the user input ?
    #check if messgeType is Score and validate value to be an integer.
    player_id     = request.POST['player_id']
    score           = request.POST['score']
    cb = False
    try:
        callback = request.GET['callback']
        cb = True
    except:
        pass

    try:#Try to get current state of the game.
        game        =  Game.objects.get(game_name=gamename)     #get an actual game object and update it.
        user        =  Member.objects.get(pk=player_id)         #get the user from Members.
        state       =  State.objects.filter(player=user, game=game).first()  #filter further by game
        if state is not None:
            state.setScore(score)
            state.save()
            context =  {
                "messageType": "Success",
                "info": "Game score saved"
            };
        else:
            raise Exception('Either game or player were not found when saving game state')
    except:
            context =  {
                "messageType": "ERROR",
                "info": "Unable to save score, Game does not exist or ownership problem"
            }
            logger.error("Game does not exist or ownership problem")

    if cb:
        result = '{0}({1})'.format(callback, context)
        response = JsonResponse(json.dumps(result), safe=False) #{"Access-Control-Allow-Origin", "*" })
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = JsonResponse(context, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
    logger.debug("sending score saving result: ", game, "State: ", context)
    return response

@csrf_exempt
def save_from_game(request, gamename ): #game name is unique.
    cb = False
    try:
        callback = request.GET['callback']
        cb = True
    except:
        pass

    score         = request.POST['score']
    player_id     = request.POST['player_id']
    playerItems   = request.POST['playerItems'] #items separated with @, them as they are.
    try:
        game        =  Game.objects.get(game_name=gamename)     #get an actual game object and update it.
        user        =  Member.objects.get(pk=player_id)         #get the user from Members.
        state       =  State.objects.filter(player=user, game=game).first()  #filter further by game
        #game found, check for player's identity, authorization is outsourced.
        if state is not None:
            state.setScore(score)
            state.setItems(playerItems)
            state.save()
            context =  {
                "messageType": "Success",
                "info": "Game state saved"
            };
        else:
            raise ValueError('Saving game state on the service encountered a problem')
    except Game.DoesNotExist:
            context =  {
                "messageType": "ERROR",
                "info": "Unable to save game state, Game does not exist or ownership problem"
            }
            logger.error("Game does not exist or ownership problem")

    if cb:
        result = '{0}({1})'.format(callback, context)
        response = JsonResponse(json.dumps(result), safe=False) 
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = JsonResponse(context, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
    logger.debug("Sending state of game: ", game, "State: ", context)
    return response
#flatten the request
#The only restriction we are imposing is upper and lower limit. 
#it could also be possible to use pre-defined resolution alternatives
#And, accepting only those, replying the default otherwise. 
@csrf_exempt
def setting_from_game(request, gamename): #game name is unique.
    logger.debug("setting ....")
    cb = False
    try:
        callback = request.GET['callback']
        cb = True
    except:
        pass

    try:
        width = int(request.POST['width' ])
        height= int(request.POST['height'])

        # provide the default resolution, if invalid request is made
        # If resolution within limit, accept request, reflected in iframe size change.
        if width < 300 or height < 300 or width  > 700 or height > 700:
            context = {
                    "messageType": "SETTING",
                    "options": {
                        "width" : 400,
                        "height": 400,
                    }
                };
        #accept what is request, if valid request is made
        else:
            context =  {
                "messageType": "SETTING",
                "options": {
                    "width" : width, #found in request and less than the minimum, default it.
                    "height": height,
                }
            };
    except:
        context = {
                "messageType": "Error",
                "info": "Incorrect value of width or height",
        };
    if cb:
        result = '{0}({1})'.format(callback, context)
        response = JsonResponse(json.dumps(result), safe=False) #{"Access-Control-Allow-Origin", "*" })
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = JsonResponse(context, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
    logger.debug("Sending resolution: ", gamename, "State: ", context)
    return response

from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.urlresolvers import reverse
from gamecenter.models import Game
# Create your views here.
#available games, 
#high scores, 
#showing sales for game developers (remember authentication)
def games(request):
	all_games             =   Game.objects.all()
	data = {}
	data["type"] = "games"
	games = [] #a set of games in objects in json format 
	game  = {} #a single game in json format. 
	for g in all_games:
		game["game name"]      		= g.game_name 
		game["maximum score"]       = g.max_score
		game["downloads"]       	= g.sales_counter
		game["price"]               = g.price
		game["upload date"]         = g.upload_date
		game["description"]    		= g.game_description  
		games.append(game)
	data["games"] = games
	return JsonResponse(data)

def highscores(request):
	all_games             =   Game.objects.all()
	data = {}
	data["type"] = "highscores"
	games = [] #a set of games in objects in json format 
	game  = {} #a single game in json format. 
	for g in all_games:
		game["game name"]      		= g.game_name 
		game["maximum score"]       = g.max_score
		games.append(game)
	data["highscores"] = games
	return JsonResponse(data)

def stats(request):
	#check if user is developer
	user = request.user
	data = {}
	if user.is_authenticated() and user.groups.filter(name='developers').exists():
		developer 	  = request.user
		all_games     =   developer.game_reverse_lookup.all()
		#all_games             =   Game.objects.all()
		data = {}
		data["type"] = "sales"
		games = [] #a set of games in objects in json format 
		game  = {} #a single game in json format. 
		for g in all_games:
			game["game name"]      		= g.game_name 
			game["downloads"]       	= g.sales_counter
			game["income"]       		= g.getSales()
			game["price"]               = g.price
			game["upload date"]         = g.upload_date
			games.append(game)
		data["sales"] = games
		return JsonResponse(data)
	else:
		response = JsonResponse({'status':'Error','message':"unauthorized use"})
		response.status_code = 401
		return response



def api(request):
	data = {}
	endpoints = []
	endpoints.append("games")
	endpoints.append("highscores")
	endpoints.append("stats")
	data["api version"] = "1.0"
	data["endpoints"] = endpoints
	return JsonResponse(data)


'''
    game["game_name"]        
    game["max_score"]       
    game["sales_counter"]    
    game["price"]           
    game["upload_date"]      
    game["game_description"]         
    game["developer"]        

    game_name        
    max_score       
    sales_counter    
    price           
    upload_date      
    game_description 
    game_url         
    developer        






	pass
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
    return render(
        request,
        'index.html',
        context,
    )
'''
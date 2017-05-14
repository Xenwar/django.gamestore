from django.db import models
from django.urls import reverse
from django.utils import timezone
from members.models import Member
# A game knows its developer [a single developer]
# Games are stored elsewhere, indicated by game_url. 
# The default game is the one given by course staff. 
# The game is shown in an iframe in the play page. 
import logging
logger = logging.getLogger(__name__)

class Game(models.Model):
    game_name        = models.CharField(max_length=25, blank=False, unique=True, verbose_name="Name")
    max_score        = models.FloatField(verbose_name="Maximum score", default=0.0)  
    sales_counter    = models.PositiveIntegerField(verbose_name="purchase count", default=0)   
    price            = models.FloatField(verbose_name="Price")   
    upload_date      = models.DateField(auto_now=False, auto_now_add=False,verbose_name="Upload date", default=timezone.now)   
    game_description = models.CharField(max_length=25, verbose_name="Game description")
    game_url         = models.URLField(max_length=255, verbose_name="Game url", default="https://git.niksula.hut.fi/oseppala/wsd2016/blob/master/examples/example_game.html")
    developer        = models.ForeignKey(Member, related_name="game_reverse_lookup", on_delete=models.CASCADE, verbose_name="Developer")

    class Meta:
        verbose_name        = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.game_name

    def getMaxScore(self):
        return  self.max_score

    def getSales(self):
        return  self.sales_counter * self.price

    def setMaxScore(self,score):#comes from the state
        logger.debug("Inside setter of game")
        self.max_score = score
        self.save()

    def get_absolute_url(self):
        return reverse('game-detail', args=[str(self.id)])

    def high_scores(self):
        highscores = {}
        highscore  = {}
        game_list = []
        if  State.objects.filter(game=self).first() is not None:#this game is purchased at least once. 
            all_states = State.objects.filter(game=self).order_by('-score')[:10] #get it out
            for state in all_states:
                highscore["name"]   = state.player.first_name
                highscore["score"]  = state.score
                game_list.append(highscore)
                highscore = {}
            highscores["allscores"] = game_list
            return highscores
        return None
#   The state of a gave with respect to a given player is shown below. 
#   (plaer, game) is unique and serves as a key.
#   Entry is created once for player's who purchsed the game.
#   Access control is not done here.
class State(models.Model):
    player    = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Player",related_name="state_reverse_lookup")
    game      = models.ForeignKey(Game,on_delete=models.CASCADE, verbose_name="Game")
    score     = models.FloatField(verbose_name="score")   #different from the maximum score which is one per game
    items     = models.TextField(blank=True)          #itesm separated by @ symbol
    purchase_date      = models.DateField(auto_now=False, auto_now_add=False,verbose_name="purchase date", default=timezone.now)   

    class Meta:
        verbose_name        = 'State'
        verbose_name_plural = 'States'
        unique_together     = ("player", "game")

    def __str__(self):
        return self.player.email + ' ,' + self.game.game_name # used for comparison')''
    #Getter and setter for items of a player's game
    def setItems(self, items):
        self.items = items

    def getItems(self):
        return self.items
    #Getter and setter for score of a player's game
    def setScore(self,score):
        self.score = score
        #make sure it set, then compare with 'global' score, update if needed.
        game = self.game#Game.objects.get(gname=self.game_name)    #get an actual game object and update it.
        if float(self.score) > float(game.getMaxScore()):
            game.setMaxScore(self.score)    #for consistency

        #logger.debug("======================", game.getMaxScore())
        #logger.debug("======================", self.score)

    def getScore(self):
            return  self.score

    def get_absolute_url(self): # a player is not a member here.
        return reverse('state-detail', args=[str(self.pk)])

    def get_game_state(self):    #a game should know its state with respect to a given player.
        try:
            oneString   = self.getItems()
            playerItems = oneString.split("@") #Save as a single string separated by @
            score       = self.getScore()
            currentSate = {}
            gameState   = {}
            logger.debug("processing collected items for: ",self.game)
            gameState['playerItems'] = playerItems
            gameState['score']       = score
            #raise ValueError('k') Testing error message
            currentSate['messageType']  = "LOAD"
            currentSate['gameState']    = gameState
        except: #whatever the reason.BUT, game is found, only loading sate has failed.
            currentSate =  {
                "messageType": "ERROR",
                "info": "Gamestate could not be loaded"
            };
        return currentSate


# Track confirmed payments. Half processed payments are ignored.     
#A player shall not buy the same game twice, protected by the 'unique_together'
#pid may result in many half prococessed transactions, could be analyzed to see how many has failed 
class Transaction(models.Model):
    player        = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="player")
    game          = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="game")
    pid           = models.CharField(max_length=25, blank=True, unique=False, verbose_name="pid")
    is_success    = models.BooleanField(default=False, verbose_name="Transaction complete",blank=True)

    class Meta:
        verbose_name        = 'Transaction'
        verbose_name_plural = 'Transactions'
        unique_together = ('player', 'game',)#For preventing re-purchasing the same game.

    def __str__(self):
        return '( '+self.player.email + ' , ' + self.game.game_name +')'





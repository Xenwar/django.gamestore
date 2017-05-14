from django.contrib import admin
from .models import Game,State, Transaction
from django.contrib import admin
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    #list_display = ('game_name','max_score','sales_counter','price','developer')
    #list_filter = ('developer', 'max_score')
    #fields = ['game_name','developer',('max_score', 'sales_counter','price'),'upload_date','game_description','game_url']
    pass

@admin.register(State)
class PlayerAdmin(admin.ModelAdmin):
    pass#fields = ('first_name','last_name','email', 'player_games')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass#fields = ('first_name','last_name','email', 'player_games')
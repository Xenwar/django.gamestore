from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
#from gamecenter.models import Game

#from gamecenter.models import Games
#A member is A player, a developer or an admin.
#import logging
#logger = logging.getLogger(__name__)
class Member(AbstractUser):
    first_name    = models.CharField(max_length=25, blank=False, verbose_name="first name")
    last_name     = models.CharField(max_length=25, blank=False, verbose_name="last name")
    email         = models.EmailField(max_length=25, verbose_name="Email", unique=True)

    class Meta:
        verbose_name        = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return self.email

    def developers_game(self):
        return ', '.join([game.pk for game in self.game_reverse_lookup.all()])
        developers_game.short_description = 'Games'

    def get_absolute_url(self):
        return reverse('member-detail', args=[str(self.id)])


# When a user registers, an activation email is sent. 
# The email and activation code are also stored for reference in this table.
class ActivationData(models.Model):
    member              = models.OneToOneField(Member,blank=True,null=True,on_delete=models.CASCADE, verbose_name="member")
    email               = models.EmailField(verbose_name='email address',max_length=25,unique=True,db_index=True,blank=False)
    activation_code     = models.CharField(max_length=25,default="Nothing")
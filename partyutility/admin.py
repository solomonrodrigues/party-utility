from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    pass

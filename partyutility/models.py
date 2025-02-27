# partyutility/models.py
import hashlib

from django.db import models
from django.utils import timezone
import uuid


class Party(models.Model):
    """Party room where players join and games are played"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="Party Room")
    code = models.CharField(max_length=4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Parties"

    def __str__(self):
        return f"{self.name} ({self.code})"

    def player_count(self):
        return self.players.count()


class Team(models.Model):
    """Teams for organizing players in a party"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="blue")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.party.code}"

    def player_count(self):
        return self.players.count()


class Player(models.Model):
    """Player in a party, can be associated with a user account or be a guest"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    is_host = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.party.code})"

    @property
    def unique_identifier(self):
        """Combines username and party code for unique identification"""
        return hashlib.sha256(f"{self.username}{self.party.code}".encode()).hexdigest()


class Game(models.Model):
    """Game that can be played at parties"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    min_players = models.PositiveSmallIntegerField(default=2)
    max_players = models.PositiveSmallIntegerField(default=20, null=True, blank=True)
    team_based = models.BooleanField(default=False)
    duration_minutes = models.PositiveSmallIntegerField(default=15)
    materials_needed = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GameSession(models.Model):
    """Record of a game played in a party"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="game_sessions")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="sessions")
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    winner_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_games")
    winner_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name="won_games")

    def __str__(self):
        return f"{self.game.name} at {self.party.name} ({self.started_at.strftime('%Y-%m-%d %H:%M')})"
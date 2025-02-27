# partyutility/views.py
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import render, redirect, get_object_or_404
import random
import string
from .models import Party, Player, Team, Game, GameSession
from django import forms
from django.urls import reverse


# Forms
class CreatePartyForm(forms.Form):
    party_name = forms.CharField(max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'My Party'}))
    player_name = forms.CharField(max_length=50, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Your name'}))


class JoinPartyForm(forms.Form):
    party_code = forms.CharField(max_length=4, min_length=4, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter 4-digit code'}))
    player_name = forms.CharField(max_length=50, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Your name'}))


class AddPlayerForm(forms.Form):
    player_name = forms.CharField(max_length=50, required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Player name'}))


class GenerateTeamsForm(forms.Form):
    num_teams = forms.IntegerField(min_value=2, max_value=10, initial=2,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))


class IndexView(TemplateView):
    template_name = 'partyutility/index.html'


# Create party views
class CreatePartyView(FormView):
    template_name = 'partyutility/partials/create_party_form.html'
    form_class = CreatePartyForm

    def get(self, request, *args, **kwargs):
        # For HTMX requests, we just return the form partial
        if request.headers.get('HX-Request'):
            return render(request, self.template_name, {
                'form': self.form_class()
            })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        party_name = form.cleaned_data.get('party_name', 'Party Room')
        player_name = form.cleaned_data['player_name']

        # Generate a unique party code
        code = self._generate_party_code()

        # Create the party
        party = Party.objects.create(
            name=party_name,
            code=code,
        )

        # Create the first player for this party
        Player.objects.create(
            party=party,
            name=player_name
        )

        # Set the redirect URL
        redirect_url = reverse('party_room', kwargs={'party_code': code})

        # Return a response with the HX-Redirect header
        response = HttpResponse()
        response['HX-Redirect'] = redirect_url
        return response

    def form_invalid(self, form):
        return render(self.request, 'partyutility/partials/create_party_form.html', {
            'form': form
        })

    @staticmethod
    def _generate_party_code(length=4):
        """Generate a unique party code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase, k=length))
            if not Party.objects.filter(code=code).exists():
                return code


# Join party views
class JoinPartyView(FormView):
    template_name = 'partyutility/partials/join_party_form.html'
    form_class = JoinPartyForm

    def get_success_url(self):
        return reverse('party_room', kwargs={'party_code': self.code})

    def get(self, request, *args, **kwargs):
        # For HTMX requests, we just return the form partial
        if request.headers.get('HX-Request'):
            return render(request, self.template_name, {
                'form': self.form_class()
            })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        party_code = form.cleaned_data['party_code'].upper()
        player_name = form.cleaned_data.get('player_name', '')

        try:
            party = Party.objects.get(code=party_code)

            # Generate a guest player name if no name is provided
            player_name = player_name or f"Guest-{random.randint(1000, 9999)}"

            # Create new player for the party
            Player.objects.get_or_create(
                party=party,
                name=player_name
            )

            # Set the redirect URL
            redirect_url = reverse('party_room', kwargs={'party_code': party_code})

            # Return a response with the HX-Redirect header
            response = HttpResponse()
            response['HX-Redirect'] = redirect_url
            return response

        except Party.DoesNotExist:
            form.add_error('party_code', 'Invalid party code. Please check and try again.')
            return self.form_invalid(form)

        except Party.DoesNotExist:
            form.add_error('party_code', 'Invalid party code. Please check and try again.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return render(self.request, 'partyutility/partials/join_party_form.html', {
            'form': form
        })


# Party room view
class PartyRoomView(DetailView):
    model = Party
    template_name = 'partyutility/party_room.html'
    context_object_name = 'party'

    def dispatch(self, request, *args, **kwargs):
        # Get and create current player if needed
        current_player = self.get_current_player()

        if not current_player and not self.request.GET.get('spectate'):
            # If we got here through a direct URL and user isn't a player, redirect to join form
            # Unless they're just spectating
            return redirect('join_party_form')

        return super().dispatch(request, *args, **kwargs)

    def get_current_player(self):
        current_player = None
        current_player = Player.objects.filter(party=self.get_object()).first()
        return current_player

    def get_object(self):
        return get_object_or_404(Party, code=self.kwargs['party_code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_code'] = self.kwargs['party_code']
        current_player = self.get_current_player()
        context['current_player'] = current_player
        context['add_player_form'] = AddPlayerForm()
        context['generate_teams_form'] = GenerateTeamsForm()

        return context


# Player list view for HTMX refreshing
class PlayerListView(ListView):
    model = Player
    template_name = 'partyutility/partials/player_list.html'
    context_object_name = 'players'

    def get_queryset(self):
        self.party = get_object_or_404(Party, code=self.kwargs['party_code'])
        return Player.objects.filter(party=self.party)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party'] = self.party
        return context


# Add player view
class AddPlayerView(View):
    def post(self, request, party_code):
        party = get_object_or_404(Party, code=party_code)
        form = AddPlayerForm(request.POST)

        if form.is_valid():
            player_name = form.cleaned_data['player_name']

            Player.objects.create(
                party=party,
                name=player_name,
                user=None  # These are manually added players, not tied to users
            )

        # Return updated player list
        players = Player.objects.filter(party=party)
        return render(request, 'partyutility/partials/player_list.html', {
            'party': party,
            'players': players,
        })


# Remove player view
class RemovePlayerView(View):
    def delete(self, request, party_code, player_id):
        player = get_object_or_404(Player, id=player_id, party__code=party_code)
        party = player.party

        player.delete()

        players = Player.objects.filter(party=party)
        return render(request, 'partyutility/partials/player_list.html', {
            'party': party,
            'players': players,
        })


# Generate teams view
class GenerateTeamsView(View):
    def post(self, request, party_code):
        party = get_object_or_404(Party, code=party_code)
        form = GenerateTeamsForm(request.POST)

        if form.is_valid():
            num_teams = form.cleaned_data['num_teams']

            players = list(Player.objects.filter(party=party))
            random.shuffle(players)

            # Clear existing teams
            Team.objects.filter(party=party).delete()

            # Create new teams
            teams = []
            team_colors = ['blue', 'red', 'green', 'purple', 'orange', 'teal', 'pink', 'yellow', 'indigo', 'gray']

            for i in range(num_teams):
                team = Team.objects.create(
                    party=party,
                    name=f"Team {i + 1}",
                    color=team_colors[i % len(team_colors)]
                )
                teams.append(team)

            # Assign players to teams
            for idx, player in enumerate(players):
                team_idx = idx % num_teams
                player.team = teams[team_idx]
                player.save()

        # Return updated teams view
        teams = Team.objects.filter(party=party)
        return render(request, 'partyutility/partials/teams.html', {
            'party': party,
            'teams': teams,
        })


# Random game selection view
class RandomGameView(View):
    def get(self, request, party_code):
        party = get_object_or_404(Party, code=party_code)

        # Get list of games
        games = Game.objects.all()

        if games.exists():
            selected_game = random.choice(games)
            context = {
                'game': selected_game,
            }
        else:
            # Fallback games if database is empty
            fallback_games = [
                {'name': 'Charades', 'description': 'Act out a word or phrase without speaking'},
                {'name': 'Pictionary', 'description': 'Draw a word or phrase for others to guess'},
                {'name': 'Trivia', 'description': 'Test your knowledge with random questions'},
                {'name': 'Word Association', 'description': 'Say a word related to the previous word'},
                {'name': 'Two Truths and a Lie', 'description': 'Tell two truths and one lie about yourself'},
            ]
            selected_game = random.choice(fallback_games)
            context = {
                'game': selected_game,
            }

        # Create a game session record
        if isinstance(selected_game, Game):
            GameSession.objects.create(
                party=party,
                game=selected_game
            )

        return render(request, 'partyutility/partials/random_game.html', context)

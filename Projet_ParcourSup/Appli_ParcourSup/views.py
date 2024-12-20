from .models import Bonjour
from django.shortcuts import render, redirect, get_object_or_404
from .models import Formation
from .forms import FormationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CandidatureForm
from .models import Candidature

def Bonjour_view(request):
    tasks = Bonjour.objects.all()
    return render(request, 'Appli_ParcourSup/index.html', {'tasks': tasks})

def formations_view(request):
    formations = Formation.objects.all()
    return render(request, 'Appli_ParcourSup/Formations.html', {'formations': formations})

@login_required
def ajouter_formation(request):
    if request.user.profile.status == 'ecole':
        if request.method == 'POST':
            form = FormationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('liste_formations')
        else:
            form = FormationForm()
        return render(request, 'Appli_ParcourSup/ajouter_formation.html', {'form': form})
    else:
        messages.error(request, 'Vous n\'avez pas la permission d\'ajouter une formation.')
        return redirect('liste_formations')

@login_required
def modifier_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.user.profile.status == 'ecole':
        if request.method == 'POST':
            form = FormationForm(request.POST, request.FILES, instance=formation)
            if form.is_valid():
                form.save()
                return redirect('liste_formations')
        else:
            form = FormationForm(instance=formation)
        return render(request, 'Appli_ParcourSup/modifier_formation.html', {'form': form})
    else:
        messages.error(request, 'Vous n\'avez pas la permission de modifier cette formation.')
        return redirect('liste_formations')

@login_required
def supprimer_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.user.profile.status == 'ecole':
        if request.method == 'POST':
            formation.delete()
            return redirect('liste_formations')
        return render(request, 'Appli_ParcourSup/supprimer_formation.html', {'formation': formation})
    else:
        messages.error(request, 'Vous n\'avez pas la permission de supprimer cette formation.')
        return redirect('liste_formations')

@login_required(login_url='pas_connecte')
def profil_view(request):
    utilisateur = request.user
    profile, created = Profile.objects.get_or_create(user=utilisateur)
    candidatures = Candidature.objects.filter(utilisateur=utilisateur)
    return render(request, 'Appli_ParcourSup/profil.html', {'utilisateur': utilisateur, 'profile': profile, 'candidatures': candidatures})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, status=form.cleaned_data['status'])
            login(request, user)
            return redirect('Page Accueil')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Appli_ParcourSup/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Page Accueil')
    else:
        form = AuthenticationForm()
    return render(request, 'Appli_ParcourSup/login.html', {'form': form})

def pas_connecte_view(request):
    return render(request, 'Appli_ParcourSup/pas_connecte.html')

@login_required(login_url='pas_connecte')
def postuler_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)

    if request.method == 'POST':
        form = CandidatureForm(request.POST)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.utilisateur = request.user
            candidature.formation = formation
            candidature.save()
            messages.success(request, 'Votre candidature a été soumise avec succès!')
            return redirect('liste_formations')
    else:
        form = CandidatureForm()

    return render(request, 'Appli_ParcourSup/postuler_formation.html', {'formation': formation, 'form': form})

@login_required
def accepter_candidature(request, formation_pk, candidat_pk):
    formation = get_object_or_404(Formation, pk=formation_pk)
    candidature = get_object_or_404(Candidature, utilisateur__pk=candidat_pk, formation=formation)

    if request.user.profile.status == 'ecole':
        candidature.statut = 'acceptee'
        candidature.save()
        messages.success(request, f'La candidature de {candidature.utilisateur.username} a été acceptée.')
    else:
        messages.error(request, 'Vous n\'avez pas la permission de réaliser cette action.')

    return redirect('liste_formations')

@login_required
def refuser_candidature(request, formation_pk, candidat_pk):
    formation = get_object_or_404(Formation, pk=formation_pk)
    candidature = get_object_or_404(Candidature, utilisateur__pk=candidat_pk, formation=formation)

    if request.user.profile.status == 'ecole':
        candidature.statut = 'refusee'
        candidature.save()
        messages.success(request, f'La candidature de {candidature.utilisateur.username} a été refusée.')
    else:
        messages.error(request, 'Vous n\'avez pas la permission de réaliser cette action.')

    return redirect('liste_formations')

@login_required
def details_candidature(request, pk):
    candidature = get_object_or_404(Candidature, pk=pk)

    if request.user.profile.status == 'ecole':
        return render(request, 'Appli_ParcourSup/details_candidature.html', {'candidature': candidature})
    else:
        messages.error(request, 'Vous n\'avez pas la permission de consulter cette candidature.')
        return redirect('liste_formations')
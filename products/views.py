from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import recipes, Favorite
from django.contrib.auth.decorators import login_required,user_passes_test
import re


def is_staff_user(user):
    return user.is_staff


@login_required(login_url='login')
def recipe_list(request):
    recipes_list = recipes.objects.all()
    return render(request, 'pages/recipe_list.html', {
        'key': recipes_list,
        'user': request.user
    })


@login_required(login_url='login')
def RecipePage(request, recipe_id):
    favs = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)

    recipe = get_object_or_404(recipes, id=recipe_id)
    description_sentences = re.split(r'[.,]', recipe.descripition)
    ingredients_list = re.split(r'[.,]', recipe.Ingredients)
    return render(request, 'pages/RecipePage.html', {
        'recipe': recipe,
        'description_sentences': description_sentences,
        'ingredients_list': ingredients_list,
        'favs': favs
    })

@user_passes_test(is_staff_user, login_url='login')
def Addrecipe(request):
    
    recipename = request.POST.get('name')
    coursename = request.POST.get('course')
    ingredients = request.POST.get('ingredients')
    description = request.POST.get('description')
    alldata = recipes(name = recipename , course = coursename , descripition = description , Ingredients = ingredients )
    if(recipename and coursename and ingredients and description):
            alldata.save()
            return redirect('recipe_list')
    return render(request,'pages/AddRecipe.html')


@login_required(login_url='login')
def search_recipes(request):
    favs = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)

    query = request.GET.get('q', '')
    ingredients = request.GET.get('ingredients', '')
    
    recipes_filtered = recipes.objects.all()
    
    if query:
        recipes_filtered = recipes_filtered.filter(
            Q(name__icontains=query) | Q(descripition__icontains=query)
        )
    
    if ingredients:
        ingredient_list = [i.strip() for i in ingredients.split(',')]
        for ing in ingredient_list:
            recipes_filtered = recipes_filtered.filter(ingredients__icontains=ing)

    return render(request, 'pages/Search.html', {
        'recipes': recipes_filtered,
        'query': query,
        'ingredients': ingredients,
        'favs': favs
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm-password')
        email = request.POST.get('email')
        isadmin_input = request.POST.get('is-admin')

        if password != confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'pages/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'pages/signup.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        if isadmin_input == 'on':
            user.is_staff = True  
        user.save()

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')

    return render(request, 'pages/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('recipe_list')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'pages/login.html')

    return render(request, 'pages/login.html')


def logout_view(request):
    auth_logout(request) 
    return redirect('login')  

@login_required(login_url='login')
def add_to_favorites(request, recipe_id):
    recipe = recipes.objects.get(id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    messages.success(request, f'{recipe.name} added to your favorites.')
    return redirect(request.META.get('HTTP_REFERER', 'recipe_list'))


@login_required(login_url='login')
def remove_from_favorites(request, recipe_id):
    recipe = recipes.objects.get(id=recipe_id)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    messages.success(request, f'{recipe.name} removed from your favorites.')
    return redirect(request.META.get('HTTP_REFERER', 'recipe_list'))


@login_required(login_url='login')
def favorites(request):
    favs = Favorite.objects.filter(user=request.user)
    return render(request, 'pages/favorites.html', {'favorites': favs})

@user_passes_test(is_staff_user, login_url='login')
def EditRecipe(request, recipe_id):
    recipe = get_object_or_404(recipes, id=recipe_id)
    if request.method == 'POST':
        recipe.name = request.POST.get('name')
        recipe.course = request.POST.get('course')
        recipe.descripition = request.POST.get('description')
        recipe.Ingredients = request.POST.get('ingredient')
        recipe.save()
        return redirect('recipe_list')
    return render(request, 'pages/editPage.html', {'recipe': recipe})


@user_passes_test(is_staff_user, login_url='login')
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(recipes, id=recipe_id)
    recipe.delete()
    messages.success(request, "Recipe deleted successfully.")
    return redirect('recipe_list')
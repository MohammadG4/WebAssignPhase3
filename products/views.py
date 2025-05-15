from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import recipes
from .models import user
from django.db.models import Q
from django.contrib.auth import authenticate, login


def recipe_list(request):
    return render(request,'pages/recipe_list.html',{'key':recipes.objects.all()})
def RecipePage(request):
    return render(request,'pages/RecipePage.html')
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



def search_recipes(request):
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
    })
def signup(request):
     username = request.POST.get('username')
     password = request.POST.get('password')
     confirm = request.POST.get('confirm-password')
     email = request.POST.get('email')
     isadmin_input = request.POST.get('is-admin')
     if isadmin_input == 'on':
        isadmin = True
     else :
        isadmin = False       
     userdata = user(username = username , password = password , Email = email , isadmin = isadmin)
     if (password != confirm):
         messages.error(request,'Error in confirming password')
         return render(request, 'pages/signup.html')
     if(username and (password == confirm) and email):
          userdata.save()
          return redirect('login')
     return render(request , 'pages/signup.html')

def login(request):
     username = request.POST.get('username')
     password = request.POST.get('password')
     if not user.objects.filter(username=username).exists():
         messages.error(request,'username doesnot exist!')
         return render(request , 'pages/login.html')
     check = authenticate(request, username=username, password=password)
     if(check is None):
         messages.error(request,'username and password do not match !')
         return render(request,'pages/login.html')
     else:
         messages.success(request,'successful process')
         return redirect('recipe_list')
                 
     return render(request , 'pages/login.html')
# Create your views here.

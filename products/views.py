from django.shortcuts import render
from .models import recipes
from django.db.models import Q

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

# Create your views here.

from django.shortcuts import render
from .models import recipes

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
# Create your views here.

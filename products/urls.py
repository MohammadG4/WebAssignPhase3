from django.urls import path
from . import views 

urlpatterns = [
    path('recipe_list/',views.recipe_list,name = 'recipe_list'),
    path('RecipePage/',views.RecipePage,name = 'RecipePage'),
    path('AddRecipe/',views.Addrecipe,name = 'AddRecipe'),
    path('search/', views.search_recipes, name='search'),
    path('signup/' , views.signup , name = 'signup'),
    path('login/' , views.login , name = 'login'),
]
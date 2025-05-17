from django.urls import path
from . import views 

urlpatterns = [
    path('',views.recipe_list,name = 'recipe_list'),
    path('RecipePage/<int:recipe_id>/', views.RecipePage, name='RecipePage'),
    path('AddRecipe/',views.Addrecipe,name = 'AddRecipe'),
    path('EditRecipe/<int:recipe_id>/',views.EditRecipe,name = 'EditRecipe'),
    path('DeleteRecipe/<int:recipe_id>/',views.delete_recipe,name = 'delete_recipe'),
    path('favorites/',views.favorites,name = 'favorites'),
    path('add_to_favorites/<int:recipe_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('search/', views.search_recipes, name='search'),
    path('signup/' , views.signup , name = 'signup'),
    path('login/' , views.login , name = 'login'),
    path('logout/', views.logout_view, name='logout'),

]
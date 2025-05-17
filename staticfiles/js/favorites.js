// favorites.js - Script for the favorites page

document.addEventListener('DOMContentLoaded', function() {
  const loadFavoriteRecipes = () => {
    const savedRecipes = JSON.parse(localStorage.getItem("saved_data")) || [];
    const favoriteRecipes = savedRecipes.filter(recipe => recipe.isFav === true);
    
    const recipesContainer = document.querySelector('.recipes-container');
    const emptyState = document.querySelector('.empty-state');
    
    recipesContainer.innerHTML = '';
    
    if (favoriteRecipes.length === 0) {
      recipesContainer.style.display = 'none';
      emptyState.style.display = 'block';
    } else {
      recipesContainer.style.display = 'grid';
      emptyState.style.display = 'none';
      
      favoriteRecipes.forEach((recipe, index) => {
        const recipeCard = createRecipeCard(recipe, index);
        recipesContainer.appendChild(recipeCard);
      });
    }
  };
  
  const createRecipeCard = (recipe, index) => {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.dataset.index = index;
    
    card.innerHTML = `
      <h2>${recipe.name}</h2>
      <p><strong>Course:</strong> ${recipe.crsname}</p>
      <p><strong>Ingredients:</strong> ${recipe.ingred}</p>
      <p class="description">${recipe.decrib}</p>
      <div class="card-actions">
        <a href="RecipePage.html?recipe=${encodeURIComponent(recipe.name)}" class="details-btn">View Details</a>
        <div class="action-buttons">
          <a href="editPage.html?recipe=${encodeURIComponent(recipe.name)}" class="edit-btn">Edit</a>
          <button class="remove-favorite" data-name="${recipe.name}">Remove from Favorites</button>
        </div>
      </div>
    `;
    
    return card;
  };
  
  const handleRemoveFromFavorites = (e) => {
    if (e.target.classList.contains('remove-favorite')) {
      const recipeName = e.target.dataset.name;
      
      const savedRecipes = JSON.parse(localStorage.getItem("saved_data")) || [];
      
      const updatedRecipes = savedRecipes.map(recipe => {
        if (recipe.name === recipeName) {
          recipe.isFav = false;
        }
        return recipe;
      });
      
      localStorage.setItem("saved_data", JSON.stringify(updatedRecipes));
      
      loadFavoriteRecipes();
    }
  };
  
  document.querySelector('.recipes-container').addEventListener('click', handleRemoveFromFavorites);
  
  loadFavoriteRecipes();
});
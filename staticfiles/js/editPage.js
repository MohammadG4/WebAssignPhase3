// editPage.js - Script for the edit recipe page

document.addEventListener('DOMContentLoaded', function() {
  const getUrlParameter = (name) => {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
  };

  const recipeName = getUrlParameter('recipe');
  let currentRecipe = null;
  let allRecipes = [];
  
  const loadRecipeData = () => {
    allRecipes = JSON.parse(localStorage.getItem("saved_data")) || [];
    currentRecipe = allRecipes.find(r => r.name === recipeName);
    
    if (!currentRecipe) {
      alert("Recipe not found!");
      window.location.href = "recipes_list.html";
      return;
    }
    
    document.getElementById("name").value = currentRecipe.name;
    
    const courseSelect = document.getElementById("course");
    const courseValue = currentRecipe.crsname.toLowerCase().replace(" ", "_");
    for (let i = 0; i < courseSelect.options.length; i++) {
      if (courseSelect.options[i].value === courseValue) {
        courseSelect.selectedIndex = i;
        break;
      }
    }
    
    const ingredientsList = document.getElementById("ingredients-list");
    ingredientsList.innerHTML = ""; 
    
    const ingredients = currentRecipe.ingred.split(", ");
    ingredients.forEach(ingredient => {
      const parts = ingredient.split(" - ");
      const ingredientName = parts[0];
      const quantity = parts.length > 1 ? parts[1] : "1";
      
      addIngredientToList(ingredientName, quantity);
    });
    
    document.getElementById("description").value = currentRecipe.decrib;
  };
  
  window.addIngredientToList = (ingredient, quantity) => {
    const list = document.getElementById("ingredients-list");
    const li = document.createElement("li");
    li.textContent = `${ingredient} - ${quantity}`;
    
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "X";
    deleteBtn.style.marginLeft = "10px";
    deleteBtn.style.background = "red";
    deleteBtn.style.color = "white";
    deleteBtn.style.border = "none";
    deleteBtn.style.cursor = "pointer";
    deleteBtn.onclick = function () {
      list.removeChild(li);
    };
    
    li.appendChild(deleteBtn);
    list.appendChild(li);
  };
  
  window.addIngredient = () => {
    const ingredient = document.getElementById("ingredient").value;
    const quantity = document.getElementById("quantity").value;
    
    if (ingredient && quantity) {
      addIngredientToList(ingredient, quantity);
      
      document.getElementById("ingredient").value = "";
      document.getElementById("quantity").value = "";
    }
  };
  
  const collectIngredients = () => {
    const items = document.getElementById("ingredients-list").getElementsByTagName("li");
    const ingredients = [];
    
    for (let i = 0; i < items.length; i++) {
      const text = items[i].textContent.replace("X", "").trim();
      ingredients.push(text);
    }
    
    return ingredients.join(", ");
  };
  
  document.getElementById("recipe-form").addEventListener("submit", function(event) {
    
    const name = document.getElementById("name").value;
    const courseSelect = document.getElementById("course");
    const courseValue = courseSelect.options[courseSelect.selectedIndex].value;
    const courseName = courseSelect.options[courseSelect.selectedIndex].text;
    const ingredients = collectIngredients();
    const description = document.getElementById("description").value;
    
    const updatedRecipe = {
      name: name,
      crsname: courseName,
      ingred: ingredients,
      decrib: description,
      isFav: currentRecipe.isFav 
    };
    
    const updatedRecipes = allRecipes.map(r => {
      if (r.name === recipeName) {
        return updatedRecipe;
      }
      return r;
    });
    
    localStorage.setItem("saved_data", JSON.stringify(updatedRecipes));
    
    window.location.href = `RecipePage.html?recipe=${encodeURIComponent(name)}`;
  });
  
  document.getElementById("delete-recipe").addEventListener("click", function() {
    if (confirm(`Are you sure you want to delete "${currentRecipe.name}"?`)) {
      const updatedRecipes = allRecipes.filter(r => r.name !== recipeName);
      
      localStorage.setItem("saved_data", JSON.stringify(updatedRecipes));
      
      window.location.href = "recipes_list.html";
    }
  });
  
  loadRecipeData();
});
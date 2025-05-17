function addIngredient() {
  const ingredient = document.getElementById("ingredient").value;
  const quantity = document.getElementById("quantity").value;
  if (ingredient && quantity) {
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

    document.getElementById("ingredient").value = "";
    document.getElementById("quantity").value = "";
  }
}

function addrecipe(event) {
  event.preventDefault(); 

  const name = document.getElementById("name").value;
  const crsname = document.getElementById("course").value;
  const description = document.getElementById("description").value;
  
  const ingredientsList = document.getElementById("ingredients-list").children;
  const ingredients = [];

  for (let i = 0; i < ingredientsList.length; i++) {
    ingredients.push(ingredientsList[i].textContent.replace("X", "").trim());
  }

  const recipe = {
    name: name,
    crsname: crsname.charAt(0).toUpperCase() + crsname.slice(1).replace("_", " "), 
    ingred: ingredients.join(", "),
    decrib: description,
    isFav: false
  };

  const existingData = JSON.parse(localStorage.getItem("saved_data")) || [];
  existingData.push(recipe);
  localStorage.setItem("saved_data", JSON.stringify(existingData));

  window.location.href = "recipes_list.html";
}

document.getElementById("recipe-form").addEventListener("submit", addrecipe);
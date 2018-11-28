var editRecipeId = null;

var newForm = document.querySelector("#create-form");
var editForm = document.querySelector("#edit-form");
var loginForm = document.querySelector("#login-form");
var createUserForm = document.querySelector("#createUser-form");

//EVERY SINGLE FETCH REQUEST AND MAKE CHANGE

var addButton = document.querySelector("#add-button");
addButton.onclick = function() {
  console.log("Button was clicked");
  var nameField = document.querySelector("#name-field");
  var ingredientsField = document.querySelector("#ingredients-field");
  var instructionsField = document.querySelector("#instructions-field");
  var cooktimeField = document.querySelector("#cooktime-field");
  var preptimeField = document.querySelector("#preptime-field");
  //button works when page refreshes appear, make button
  createRecipe(nameField.value, ingredientsField.value, instructionsField.value, cooktimeField.value, preptimeField.value);
  window.alert("Your recipe was created");
  nameField.value = '';
  ingredientsField.value = '';
  instructionsField.value = '';
  cooktimeField.value = '';
  preptimeField.value = '';
};

// this is the SAVE button inside the edit form
var editButton = document.querySelector("#edit-button");
editButton.onclick = function() {
  // TOOD: send the updated item to the server
  console.log("Button was clicked");
  //createPanda(.....);
  var nameField = document.querySelector("#edit-name-field");
  var ingredientsField = document.querySelector("#edit-ingredients-field");
  var instructionsField = document.querySelector("#edit-instructions-field");
  var cooktimeField = document.querySelector("#edit-cooktime-field");
  var preptimeField = document.querySelector("#edit-preptime-field");
  //button works when page refreshes appear, make button

  replaceRecipe(nameField.value, ingredientsField.value, instructionsField.value, cooktimeField.value, preptimeField.value, editRecipeId);
  nameField.value = ''
  ingredientsField.value = ''
  instructionsField.value = ''
  cooktimeField.value = ''
  preptimeField.value = ''
};

var accButton = document.querySelector("#create-account-button");
accButton.onclick = function(){
  console.log("new user button was clicked");
  newForm.style.display = "none";
  editForm.style.display = "none";
  createUserForm.style.display = "block";
  loginForm.style.display = "none";
};

var addCreatedAccount = document.querySelector("#add-created-account")
addCreatedAccount.onclick = function(){
  var emailField = document.querySelector("#new-email-field");
  var passwordField = document.querySelector("#new-password-field");
  var fnameField = document.querySelector("#new-fname-field");
  var lnameField = document.querySelector("#new-lname-field");

  //TODO: prevent user from creating user with same email
  createUser(fnameField.value, lnameField.value, emailField.value, passwordField.value);
  console.log("successfully created user");

  emailField.value = ''
  passwordField.value = ''
  fnameField.value = ''
  lnameField.value = ''
};

var loginButton = document.querySelector("#login-button");
loginButton.onclick = function(){
  //code here to verify user
  console.log("login button was clicked");
  var emailField = document.querySelector("#existing-email-field");
  var pwField = document.querySelector("#existing-password-field");
  authenticateUser(emailField.value, pwField.value);
};

var logoutButton = document.querySelector("#logout-button");
logoutButton.onclick = function(){
  newForm.style.display = "none";
  editForm.style.display = "none";
  createUserForm.style.display = "none";
  loginForm.style.display = "block";
}

function createUser(fname, lname, email, password){
  var someData = `fname=${encodeURIComponent(fname)}`;
  someData += `&lname=${encodeURIComponent(lname)}`;
  someData += `&email=${encodeURIComponent(email)}`;
  someData += `&password=${encodeURIComponent(password)}`;
  console.log("this is the data", someData)
  fetch("http://localhost:8080/users", {
  method: "POST",
  body: someData,
  credentials: 'include',
  headers: {
    "Content-type": "application/x-www-form-urlencoded"
  }
  }).then(function(response){
    console.log("Response Status when user was trying to be created:", response.status);
    if(response.status == 201){
      window.alert("successfully created user")
      console.log("yay! we can now switch forms")
      newForm.style.display = "none";
      editForm.style.display = "none";
      createUserForm.style.display = "none";
      loginForm.style.display = "block";
    } else if(response.status == 422){
      window.alert("You are already registered. Try logging in.")
      newForm.style.display = "none";
      editForm.style.display = "none";
      createUserForm.style.display = "none";
      loginForm.style.display = "block";
    } else{
      console.log("you have an error when you tried to switch forms")
      window.alert("oops")
    }
  });
};

function authenticateUser(email, pw){
  var someData = `email=${encodeURIComponent(email)}`;
  someData += `&password=${encodeURIComponent(pw)}`;
  fetch("http://localhost:8080/sessions", {
  method: "POST",
  body: someData,
  credentials: 'include',
  headers: {
    "Content-type": "application/x-www-form-urlencoded"
  }
  }).then(function(response){
    console.log("cool, that user was verified", response.status);
    if(response.status == 201) {
      showTheRecipes();
      console.log("switch to add recipes form")
      newForm.style.display = "block";
      editForm.style.display = "none";
      createUserForm.style.display = "none";
      loginForm.style.display = "none";
      window.alert("Welcome!")
    } else {
      window.alert("Invalid username or password, please verify your credentials")
    }
  });
};


function createRecipe(name,ingredients,instructions,cooktime,preptime){
  var someData = `name=${encodeURIComponent(name)}`;
  someData += `&ingredients=${encodeURIComponent(ingredients)}`;
  someData += `&instructions=${encodeURIComponent(instructions)}`;
  someData += `&cooktime=${encodeURIComponent(cooktime)}`;
  someData += `&preptime=${encodeURIComponent(preptime)}`;
  fetch("http://localhost:8080/recipes", {
  method: "POST",
  body: someData,
  credentials: 'include',
  headers: {
    "Content-type": "application/x-www-form-urlencoded"
  }
  }).then(function(response){
    console.log("cool, that message was created", response.status);
    if(response.status == 201) {
      console.log("run the code below")
      showTheRecipes();
    } else {
      console.log("got an error")
    }
  });
};

function showTheRecipes () {
  fetch("http://localhost:8080/recipes", {
    credentials: 'include'
  }).then(function(response){
    if (response.status == 401) {
      // DONE: show login form, hide recipes list
      newForm.style.display = "none";
      editForm.style.display = "none";
      createUserForm.style.display = "none";
      loginForm.style.display = "block";
    } else if (response.status == 200) {
      // DONE: hide login form, show recipes list
      newForm.style.display = "block";
      editForm.style.display = "none";
      createUserForm.style.display = "none";
      loginForm.style.display = "none";
      // add recipes to list:
      response.json().then(function(theRecipes){
        console.log(theRecipes)
        
        var myList = document.querySelector("#my-list");
        myList.innerHTML = "";
        theRecipes.forEach(function(theRecipe){
          var listItem = document.createElement("li");
          listItem.innerHTML = theRecipe.name + "<br />" + " Ingredients: " + theRecipe.ingredients + "<br />" +  " Instructions: " + theRecipe.instructions + "<br />" + " Cooktime: " + theRecipe.cooktime + " minute(s) " + "<br />" + " Preptime: " + theRecipe.preptime + " minute(s) " + "<br />"
          //listItem.innerHTML = "<span class=innerhtmlstyle>" + "<br />" + theRecipe.name + "<br />"+ theRecipe.name + " requires " + theRecipe.ingredients + "<br />" + ". The instructions are: " + theRecipe.instructions + "<br />" + ". It takes " + theRecipe.cooktime + " minutes to cook and " + theRecipe.preptime + " minutes to prep." + "</span>"


          var deleteButton = document.createElement("button");
          deleteButton.innerHTML = "Delete";
          deleteButton.className = "delete-button";
          listItem.appendChild(deleteButton);

          myList.appendChild(listItem);

          deleteButton.onclick= function(){
            deleteRecipe(theRecipe);
            console.log("delete", theRecipe.id)
          };

          var updateButton = document.createElement("button");
          updateButton.innerHTML = "Edit";
          updateButton.className = "update-button";

          listItem.appendChild(updateButton);

          updateButton.onclick = function(){

            console.log("replaced", theRecipe.id)

            newForm.style.display = "none";
            editForm.style.display = "block";

            // save the recipe so we can get its ID later
            editRecipeId = theRecipe.id;

            // populate edit form fields with current data
            var nameField = document.querySelector("#edit-name-field");
            nameField.value = theRecipe.name;
            var ingredientsField = document.querySelector("#edit-ingredients-field");
            ingredientsField.value = theRecipe.ingredients;
            var instructionsField = document.querySelector("#edit-instructions-field");
            instructionsField.value = theRecipe.instructions;
            var cooktimeField = document.querySelector("#edit-cooktime-field");
            cooktimeField.value = theRecipe.cooktime;
            var preptimeField = document.querySelector("#edit-preptime-field");
            preptimeField.value = theRecipe.preptime;
          };
        });
      });
    }
  });
};

function deleteRecipe(recipe) {
  if(confirm("You want to delete?")){
    console.log("Deleting recipe with ID", recipe.id);
    fetch(`http://localhost:8080/recipes/${recipe.id}` , {
      method: "DELETE",
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
      console.log("Delete recipe successful");
      loadRecipes();
  };
};


function replaceRecipe(name, ingredients, instructions, cooktime, preptime, recipe_id) {
    var someData = `name=${encodeURIComponent(name)}`;
    someData += `&ingredients=${encodeURIComponent(ingredients)}`;
    someData += `&instructions=${encodeURIComponent(instructions)}`;
    someData += `&cooktime=${encodeURIComponent(cooktime)}`;
    someData += `&preptime=${encodeURIComponent(preptime)}`;

    console.log("Replacing recipe with ID", recipe_id);
    fetch(`http://localhost:8080/recipes/${recipe_id}` , {
      method: "PUT",
      body: someData,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(function () {
      console.log("Replace recipe successful");
      // show the create form again
      newForm.style.display = "block";
      editForm.style.display = "none";
      loadRecipes();
    });

};

var loadRecipes = function () {
  fetch("http://localhost:8080/recipes", {
    credentials: 'include'
  }).then(function (response) {
    console.log(response.status);
    if (response.status == 401){
      //not logged in, show login form
      newForm.style.display = "none";
      editForm.style.display = "none";
      createUserForm.style.display = "none";
      loginForm.style.display = "block";
    } else if (response.status == 200){
    response.json().then(function (theRecipes) {
      console.log("Recipes:", theRecipes);
      showTheRecipes(theRecipes);
      });
    }
  });
};

loadRecipes();

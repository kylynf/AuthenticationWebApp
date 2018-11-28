# Resource: recipes and users
## Recipes Attributes:
* name
* ingredients
* instructions
* cooktime
* preptime

## Users Attributes:
* first name
* last name
* email
* encrypted password

# Recipes Schema
```
CREATE TABLE recipes (
id INTEGER PRIMARY KEY,
name varchar(255),
ingredients varchar(255),
instructions varchar (255),
cooktime integer,
preptime integer);
```

# Users Schema
```
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name varchar(255),
    last_name varchar(255),
    email varchar(255),
    encrypted_password varchar(255));
```


# REST endpoints
Name | HTTP Method | Recipes Path | Sessions Path | Users Path
-----|-------------|--------------| ------------- | -------
Create | POST      |  /recipes    | /sessions | /users
Delete | DELETE | http://localhost:8080/recipes/${recipe.id} | NONE | NONE
Replace | PUT | http://localhost:8080/recipes/${recipe_id} | NONE | NONE
Retrieve | GET | http://localhost:8080/recipes/${recipe.id} | http://localhost:8080/sessions | NONE
List | GET | http://localhost:8080/recipes | NONE | NONE


# Password Encryption Method
Bcrypt

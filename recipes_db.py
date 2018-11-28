import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class RecipesDB:
    def __init__(self):
        #"open the file"
        #connecting
        print("Connecting to DB.")
        self.connection = sqlite3.connect("recipes_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def __del__(self):
        print("Disconecting from DB.")
        self.connection.close()

    def getRecipe(self,recipe_id):
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?" , [recipe_id])
        return self.cursor.fetchone()

    def getRecipes(self):
        #selecting and reading
        self.cursor.execute("SELECT * FROM recipes")
        #grabbing data here
        return self.cursor.fetchall()

    def createRecipe(self,name,ingredients,instructions,cooktime,preptime):
        #run a query
        #semicolon is not needed in python file
        #inserting
        self.cursor.execute("INSERT INTO recipes (name, ingredients, instructions, cooktime, preptime) VALUES (?,?,?,?,?)" , [name, ingredients, instructions, cooktime, preptime])
        self.connection.commit()

    def deleteRecipe(self, recipe_id):
        self.cursor.execute("DELETE FROM recipes WHERE id=?" , [recipe_id])
        self.connection.commit()

    def replaceRecipe(self, name, ingredients, instructions, cooktime, preptime, recipe_id):
        self.cursor.execute("UPDATE recipes SET name= ?, ingredients = ?, instructions = ?, cooktime = ?, preptime = ? WHERE id = ?", [name, ingredients, instructions, cooktime, preptime, recipe_id])
        self.connection.commit()

# class UsersDB:
#     def __init__(self):
#         #"open the file"
#         #connecting
#         print("Connecting to DB.")
#         self.connection = sqlite3.connect("recipes_db.db")
#         self.connection.row_factory = dict_factory
#         self.cursor = self.connection.cursor()

#     def __del__(self):
#         print("Disconecting from DB.")
#         self.connection.close()

    def getUserByEmail(self,email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", [email])
        return self.cursor.fetchone()
    
    def getUser(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?" , [id])
        return self.cursor.fetchone()

    def createUser(self,first_name, last_name, email, encrypted_password):
        self.cursor.execute("INSERT INTO users (first_name, last_name, email, encrypted_password) VALUES (?,?,?,?)" , [first_name, last_name, email, encrypted_password])
        self.connection.commit()


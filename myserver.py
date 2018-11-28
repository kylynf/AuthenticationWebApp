from http.server import BaseHTTPRequestHandler , HTTPServer
from urllib.parse import parse_qs
import json
from recipes_db import RecipesDB
# from recipes_db import UsersDB
from passlib.hash import bcrypt
from http import cookies
from session_store import SessionStore

gSessionStore = SessionStore()

class MyAwesomeHandler(BaseHTTPRequestHandler):

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session(self):
        #goal: assign self.session according to sessionid
        self.load_cookie()
        if "sessionID" in self.cookie:
            sessionID = self.cookie["sessionID"].value
            self.session = gSessionStore.getSession(sessionID)
            if self.session == None:
                #session data does not exist for this ID
                sessionID = gSessionStore.createSession()
                self.session = gSessionStore.getSession(sessionID)
                self.cookie["sessionID"] = sessionID
        else:
            #client has no session id yet
            sessionID = gSessionStore.createSession()
            self.session = gSessionStore.getSession(sessionID)
            self.cookie["sessionID"] = sessionID
        print("CURRENT SESSION: ", self.session)

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()
        return

    def do_GET(self):
        self.load_session()
        if self.path == "/recipes":
            self.handleRecipeList()
        elif self.path.startswith("/recipes/"):
            parts = self.path.split("/")
            recipe_id = parts[2]
            self.handleRecipeRetrieve(recipe_id)
        elif self.path == "/sessions":
            self.handleSessionRetrieve()
        else:
            self.handleNotFound()

    def do_POST(self):
        #put users path here
        #data goes here
        #write to file in create
        self.load_session()
        if self.path == "/recipes":
            self.handleRecipeCreate()
        elif self.path == "/users": # sign up
            self.handleUserCreate()
        elif self.path == "/sessions": # sign in
            self.handleSessionCreate()
        else:
            #not found response
            self.handleNotFound()
        
    def do_DELETE(self):
        #read in list
        self.load_session()
        if self.path.startswith("/recipes/"):
            parts = self.path.split("/")
            recipe_id = parts[2]
            self.handleRecipeDelete(recipe_id)
        else:
            self.handleNotFound()

    def do_PUT(self):
        #read in list
        self.load_session()
        if self.path.startswith("/recipes/"):
            parts = self.path.split("/")
            recipe_id = parts[2]
            self.handleRecipeReplace(recipe_id)
        else:
            self.handleNotFound()

    def handleRecipeList(self):
        # todo: copy this to all receipe methods
        if "userID" not in self.session:
            self.handle401()
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        #receive message here
        db = RecipesDB()
        recipes = db.getRecipes()

        self.wfile.write(bytes(json.dumps(recipes), "utf-8"))

    # retrieve info for signed-in user
    def handleSessionRetrieve(self):
        if "userID" in self.session:
            # db = UsersDB()
            db = RecipesDB()
            user = db.getUser(self.session["userID"])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(user), "utf-8"))
        else:
            self.handle401()
            #alert("Please register")
            
    def handleRecipeCreate(self):
        length = self.headers["Content-length"]
        #ready body data from client
        body = self.rfile.read(int(length)).decode("utf-8")
        #parse the body into a dictionary with values of arrays
        data = parse_qs(body)

        name = data['name'][0]
        ingredients = data['ingredients'][0]
        instructions = data['instructions'][0]
        cooktime = data['cooktime'][0]
        preptime = data['preptime'][0]

        #send to the database
        db = RecipesDB()
        db.createRecipe(name,ingredients,instructions,cooktime,preptime)

        self.send_response(201)
        self.end_headers()

    # user sign up
    def handleUserCreate(self):
        length = self.headers["Content-length"]
        #ready body data from client
        body = self.rfile.read(int(length)).decode("utf-8")
        #parse the body into a dictionary with values of arrays
        data = parse_qs(body)

        fname = data['fname'][0]
        lname = data['lname'][0]
        email = data['email'][0]
        password = data['password'][0]

        encrypted_password = bcrypt.hash(password)

        #send to the database
        # db = UsersDB()
        db = RecipesDB()
        if db.getUserByEmail(email) == None:
            db.createUser(fname, lname, email, encrypted_password)
            self.send_response(201)
            self.end_headers()
            #alert("You have successfully signed up")
        else:
            self.handle422()
            #alert("Sorry there was an error")

    # user sign in
    def handleSessionCreate(self):
        length = self.headers["Content-length"]
        #ready body data from client
        body = self.rfile.read(int(length)).decode("utf-8")
        #parse the body into a dictionary with values of arrays
        data = parse_qs(body)

        email = data['email'][0]
        pw = data['password'][0]

        #send to the database
        db = RecipesDB()

        user = db.getUserByEmail(email)
        if user == None:
            #failure
            self.handle401()
        else:
            if bcrypt.verify(pw, user['encrypted_password']):
                #YAY
                self.session["userID"] = user["id"]
                self.send_response(201)
                self.end_headers()
            else:
                #failure
                self.handle401()

    def handleRecipeRetrieve(self, recipe_id):
        db = RecipesDB()
        recipe = db.getRecipe(recipe_id)
        print("testing", recipe)
        if recipe == None:
            self.handleNotFound()
        else:
            myjson = json.dumps(recipe)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes (myjson, "utf-8"))

    def handleRecipeDelete(self, recipe_id):
        db = RecipesDB()
        recipe = db.getRecipe(recipe_id)
        print("testing delete", recipe_id)
        if recipe == None:
            self.handleNotFound()
        else:
            db.deleteRecipe(recipe_id)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("<h1> Recipe Deleted</h1>", "utf-8"))

    def handleRecipeReplace(self, recipe_id):
        db = RecipesDB()
        recipe = db.getRecipe(recipe_id)
        print("testing replace", recipe_id)
        if recipe == None:
            self.handleNotFound()
        else:
            length = self.headers["Content-length"]
            #ready body data from client
            body = self.rfile.read(int(length)).decode("utf-8")
            #parse the body into a dictionary with values of arrays
            data = parse_qs(body)

            name = data['name'][0]
            ingredients = data['ingredients'][0]
            instructions = data['instructions'][0]
            cooktime = data['cooktime'][0]
            preptime = data['preptime'][0]
            db.replaceRecipe(name, ingredients, instructions, cooktime, preptime, recipe_id)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("<h1> Recipe Deleted</h1>", "utf-8"))

    def handleNotFound(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("Sorry, not found", "utf-8"))


    def handle401(self):
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes("You are not authorized", "utf-8"))

    def handle422(self):
        self.send_response(422)
        self.end_headers()
        self.wfile.write(bytes("Unprocessable", "utf-8"))


def run():
    listen = ("0.0.0.0", 8080)
    server = HTTPServer(listen, MyAwesomeHandler)

    #know that server is listening otherwise empty screen
    print("Listening...")
    server.serve_forever()

run()


from flask_restful import Resource
from flask import request
from models import User, Recipe
from sqlalchemy.exc import IntegrityError

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url')
        bio = data.get('bio')

        # Create new User object
        user = User(username=username, password=password, image_url=image_url, bio=bio)

        try:
            # Save user to database
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Username already exists"}, 400

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            return {"message": "User is logged in", "user_id": session['user_id']}
        return {"message": "No user logged in"}

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return {"message": "Logged in successfully"}
        return {"message": "Invalid credentials"}, 401

class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        return {"message": "Logged out successfully"}

class RecipeIndex(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return [recipe.to_dict() for recipe in recipes], 200













# # resources.py


# from flask_restful import Resource


# class Signup(Resource):
#     def post(self):
#         return {'message': 'Signup endpoint'}
# class CheckSession(Resource):
#     def get(self):
#         return {"message": "Check session endpoint"}

# class Login(Resource):
#     def post(self):
#         return {"message": "Login endpoint"}

# class Logout(Resource):
#     def post(self):
#         return {"message": "Logout endpoint"}

# class RecipeIndex(Resource):
#     def get(self):
#         return {"message": "Recipes endpoint"}

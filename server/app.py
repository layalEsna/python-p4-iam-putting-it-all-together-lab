# #!/usr/bin/env python3

# from flask import request, session, jsonify, make_response
# from flask_restful import Resource
# from sqlalchemy.exc import IntegrityError

# from config import app, db, api
# from models import User, Recipe






from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Import app, database, and API correctly
from config import app, db, api
from models import User, Recipe

# from werkzeug.security import generate_password_hash, check_password_hash

# class Signup(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data['username']
#         password = data['password']
#         bio = data['bio']
#         image_url = data['image_url']

#         # Validate and create the user record
#         if not username or not password:
#             return {"message": "Username and password are required"}, 400

#         user = User(username=username, bio=bio, image_url=image_url)
#         user.password = password  # Hash the password
#         db.session.add(user)
#         db.session.commit()

#         return {"message": "User created successfully", "user": user.username}, 201

class Signup(Resource):
   
    def post(self):
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        image_url = data.get('image_url')
        # image_url = data.get('image_url', 'https://example.com/default.jpg')
        bio = data.get('bio', '')
        
        if not username or not username.strip():
            return jsonify({"error": "Username is required."}), 400
        if not password or not password.strip():
            return jsonify({"error": "Password is required."}), 400

        existing_user = User.query.filter(User.username == username.strip()).first()
        if existing_user:
            return jsonify({'error': 'Username already exists.'}), 422
        
        try:
            new_user = User(
                username=username.strip(),
                image_url=image_url,
                bio=bio
            )
            new_user.password = password.strip()  # Ensure password is hashed
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            # Return the response correctly as a JSON object
            return jsonify(new_user.to_dict()), 201  # HTTP 201 status for successful creation

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Database error occurred."}), 422
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500















class CheckSession(Resource):
    def get(self):

        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Not logged in.'}, 401)
        
        user = User.query.get(user_id)

        if not user:
            return make_response({'error': 'Invalid username.'}, 401)
        return make_response(user.to_dict(), 200)


# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data.get('username', '').strip()
#         password = data.get('password', '').strip()

#         if not username or not password:
#             return make_response({'error': 'Username and password are required.'}, 400)

#         user = User.query.filter_by(username=username).first()
#         if not user or not user.check_password(password):
#             return make_response({'error': 'Invalid credentials.'}, 401)

#         session['user_id'] = user.id
#         return make_response(user.to_dict(), 200)

class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response({'error': 'Username and password are required.'}, 400)
        
        user = User.query.filter(User.username==username).first()

        if not user or not user.check_password(password):
            return make_response({'error': 'Invalid username or password.'}, 401)
        session['user_id'] = user.id
        return make_response(user.to_dict(), 200)

class Logout(Resource):
    def delete(self):
        user_id = session.pop('user_id', None)
        if not user_id:
            return make_response({'error': 'Not logged in.'}, 401)

        return make_response({}, 204)
    

# class RecipeIndex(Resource):
#     def get(self):
#         user_id = session.get['user_id']
#         if not user_id:
#             return make_response({'error':
#                                   'Not logged in'}, 401)
#         recipes = Recipe.query.all()
        
#         recipe_list = []
#         for reci in recipes:
#           if reci.user:
#             recipe_list.append({
#                 'title': reci.title,
#                 'instruction': reci.instructions,
#                 'minutes': reci.minutes_to_complete,
#                 'user': {
#                     'username': reci.user.username,
#                     'image_url': reci.user.image_url,  
#                     'bio': reci.user.bio  


#                 }
#             })
#           else:
#               recipe_list.append({
#                         'title': reci.title,
#                         'instructions': reci.instructions,
#                         'minutes': reci.minutes_to_complete,
#                         'user': None  # If no user is associated with the recipe
#                     })
              
#         return make_response({'recipes': recipe_list}, 200)
        
class RecipeIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401  # Return a dictionary directly

        recipes = Recipe.query.all()
        recipe_list = [
            {
                "title": recipe.title,
                "instructions": recipe.instructions,
                "minutes_to_complete": recipe.minutes_to_complete,
                "user": {
                    "id": recipe.user.id,
                    "username": recipe.user.username
                } if recipe.user else None
            }
            for recipe in recipes
        ]
        return recipe_list, 200  # No need to use jsonify

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        title = data.get('title')
        instructions = data.get('instructions')
        minutes_to_complete = data.get('minutes_to_complete')

        errors = {}
        if not title:
            errors['title'] = 'Title is required.'
        if not instructions:
            errors['instructions'] = 'Instructions are required.'
        if not minutes_to_complete or not isinstance(minutes_to_complete, int):
            errors['minutes_to_complete'] = 'Minutes to complete must be an integer.'

        if errors:
            return errors, 422

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        new_recipe = Recipe(
            title=title,
            instructions=instructions,
            minutes_to_complete=minutes_to_complete,
            user=user
        )
        db.session.add(new_recipe)
        db.session.commit()

        recipe_data = {
            "title": new_recipe.title,
            "instructions": new_recipe.instructions,
            "minutes_to_complete": new_recipe.minutes_to_complete,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }

        return recipe_data, 201 




api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5000, debug=True)




















# #!/usr/bin/env python3

# from flask import request, session
# from flask_restful import Resource
# from sqlalchemy.exc import IntegrityError

# from config import app, db, api
# from models import User, Recipe

# class Signup(Resource):
#     pass

# class CheckSession(Resource):
#     pass

# class Login(Resource):
#     pass

# class Logout(Resource):
#     pass

# class RecipeIndex(Resource):
#     pass

# api.add_resource(Signup, '/signup', endpoint='signup')
# api.add_resource(CheckSession, '/check_session', endpoint='check_session')
# api.add_resource(Login, '/login', endpoint='login')
# api.add_resource(Logout, '/logout', endpoint='logout')
# api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)
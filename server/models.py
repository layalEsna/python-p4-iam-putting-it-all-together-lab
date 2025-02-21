# from sqlalchemy.orm import validates, relationship
# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_serializer import SerializerMixin
# from config import db, bcrypt
# # check_password



# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship, validates
# from config import db, bcrypt

# # from flask_bcrypt import Bcrypt
# db = SQLAlchemy()
# # bcrypt = Bcrypt()


from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    # User attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
 
    # One-to-many relationship with Recipe
    recipes = relationship('Recipe', back_populates='user')

    # Password property to ensure it's write-only
    @property
    def password(self):
        raise AttributeError('Password is write-only')

    @password.setter
    def password(self, password):
        # Hash the password before saving
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the hashed password
        return bcrypt.check_password_hash(self._password_hash, password)

    def set_password(self, password):
        self.password = password  # This will use the setter to hash the password

    # Validate username to ensure it is not empty
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username cannot be empty.')
        if User.query.filter(User.username == username).first():
            raise ValueError('Username already exists.')
        return username

    # Validate image_url to ensure it is a valid URL or use default
    # @validates('image_url')
    # def validate_image_url(self, key, image_url):
    #     if not image_url or not image_url.strip():
    #         return 'https://example.com/default.jpg'  # Default if not provided
    #     return image_url.strip()
    @validates('image_url')
    def validate_image_url(self, key, image_url):
        if not image_url or not image_url.strip():
            return 'https://example.com/default.jpg'  # Default value
        return image_url.strip()


    # Validate password_hash to ensure it's not empty
    @validates('_password_hash')
    def validate_password_hash(self, key, _password_hash):
        if not _password_hash:
            raise ValueError('Password hash cannot be empty.')
        return _password_hash

    def to_dict(self):
        # Method to return the user as a dictionary
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "image_url": self.image_url,
        }






# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False, unique=True)
#     # _password_hash = db.Column(db.String, nullable=False, default=bcrypt.generate_password_hash('default').decode('utf_8'))
#     _password_hash = db.Column(db.String, nullable=False)

#     image_url = db.Column(db.String, nullable=False, default='https://example.com/default.jpg')
#     bio = db.Column(db.String, nullable=False, default='')


#     def to_dict(self):
#         return {
#             "id": self.id,
#             "username": self.username,
#             "bio": self.bio,
#             "image_url": self.image_url,
#         }

#     # One to many relationship with recipes
#     recipes = relationship('Recipe', back_populates='user')

#     # @hybrid_property
#     @property
#     def password(self):
#         raise AttributeError('Password is write-only')
    
#     @password.setter
#     def password(self, password):
#         self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self._password_hash, password)
    
#     # def set_password(self, password):
#     #     self.password = password


#     @validates('_password_hash')
#     def validate_password_hash(self, key, _password_hash):
#         if not _password_hash:
#             raise ValueError('Password hash cannot be empty.')
#         return _password_hash


    
#     @validates('username')
#     def username_validation(self, key, username):
#         if not username or not username.strip():
#             raise ValueError('Username cannot be empty.')
#         return username.strip()
    
#     @validates('image_url')
#     def image_url_validation(self, key, image_url):
#         if not image_url or not image_url.strip():
#             return 'https://example.com/default.jpg' 
#         return image_url.strip()

    
    

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = relationship('User', back_populates='recipes')

    @validates('title')
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError('Title cannot be empty')
        return title
    
    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or not instructions.strip():
            raise ValueError('Instructions cannot be empty')
        elif len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters')
        return instructions







# from sqlalchemy.orm import validates
# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_serializer import SerializerMixin

# from config import db, bcrypt

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     pass

# class Recipe(db.Model, SerializerMixin):
#     __tablename__ = 'recipes'
    
#     pass
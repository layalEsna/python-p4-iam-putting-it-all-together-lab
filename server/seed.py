# #!/usr/bin/env python3

# from random import randint, choice as rc

# from faker import Faker

# from app import app
# from models import db, Recipe, User

# fake = Faker()

# with app.app_context():

#     print("Deleting all records...")
#     Recipe.query.delete()
#     User.query.delete()

#     fake = Faker()

#     print("Creating users...")

#     # make sure users have unique usernames
#     users = []
#     usernames = []

#     for i in range(20):
        
#         username = fake.first_name()
#         while username in usernames:
#             username = fake.first_name()
#         usernames.append(username)

#         user = User(
#             username=username,
#             bio=fake.paragraph(nb_sentences=3),
#             image_url=fake.url(),
#         )

#         user.password_hash = user.username + 'password'

#         users.append(user)

#     db.session.add_all(users)

#     print("Creating recipes...")
#     recipes = []
#     for i in range(100):
#         instructions = fake.paragraph(nb_sentences=8)
        
#         recipe = Recipe(
#             title=fake.sentence(),
#             instructions=instructions,
#             minutes_to_complete=randint(15,90),
#         )

#         recipe.user = rc(users)

#         recipes.append(recipe)

#     db.session.add_all(recipes)
    
#     db.session.commit()
#     print("Complete.")
#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    db.session.query(Recipe).delete()
    db.session.query(User).delete()

    print("Creating users...")

    users = []
    usernames = set()

    for _ in range(20):
        username = fake.unique.first_name()
        usernames.add(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.image_url(),
        )

        user.set_password(username + "password")  # Correct password hashing
        users.append(user)

    db.session.add_all(users)
    db.session.commit()  # Commit users before assigning to recipes

    print("Creating recipes...")
    recipes = []

    for _ in range(100):
        instructions = fake.paragraph(nb_sentences=8)

        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15, 90),
            user=rc(users)  # Associate with a random user
        )

        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()

    print("Seeding complete.")

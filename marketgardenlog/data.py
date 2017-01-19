from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Garden, Base, Plant, User


# garden_names = ['Renoir', 'Zaratrusta', 'Vivien', 'Sena', 'Cran',
#                 'Siracusa', 'Falela', 'Carton', 'Finch', 'Fern']
# garden_locations = ['Madrid', 'Rubi', 'Milan', 'Irun', 'Endaia', 'Vic',
#                     'Medina', 'Panes', 'Segovia', 'Lleida']
# garden_type = ['Herb Garden', 'Flower Garden', 'Edible Landscaping',
#                'Rain Garden', 'Vegetable Garden', 'Others']

engine = create_engine('sqlite:///marketgardenlog.db')

# Bind the engine to the metadata of the Base class
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# DBSession() instance establishes all conversations with the database
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')  # NOQA
session.add(User1)
session.commit()


# Tony's Garden
garden1 = Garden(user_id=1, name="Tony's Garden", garden_type="Herbs Garden")

session.add(garden1)
session.commit()

plant2 = Plant(user_id=1, name="Parsley", comments="Juicy grilled veggie patty with tomato mayo and lettuce",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant2)
session.commit()


plant1 = Plant(user_id=1, name="French Fries", comments="with garlic and parmesan",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant1)
session.commit()

plant2 = Plant(user_id=1, name="Chicken Burger", comments="Juicy grilled chicken patty with tomato mayo and lettuce",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant2)
session.commit()

plant3 = Plant(user_id=1, name="Chocolate Cake", comments="fresh baked and served with ice cream",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant3)
session.commit()

plant4 = Plant(user_id=1, name="Sirloin Burger", comments="Made with grade A beef",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant4)
session.commit()

plant5 = Plant(user_id=1, name="Root Beer", comments="16oz of refreshing goodness",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant5)
session.commit()

plant6 = Plant(user_id=1, name="Iced Tea", comments="with Lemon",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant6)
session.commit()

plant7 = Plant(user_id=1, name="Grilled Cheese Sandwich",
                     comments="On texas toast with American Cheese", plant_type="Aromatic Herbs", garden=garden1)

session.add(plant7)
session.commit()

plant8 = Plant(user_id=1, name="Veggie Burger", comments="Made with freshest of ingredients and home grown spices",
                     plant_type="Aromatic Herbs", garden=garden1)

session.add(plant8)
session.commit()


# Felix's Garden
garden2 = Garden(user_id=1, name="Felix's Garden", garden_type="Floral Garden")

session.add(garden2)
session.commit()

plant1 = Plant(user_id=1, name="Rosal", plant_type="Floral Plant",
               garden=garden2)

session.add(plant1)
session.commit()

plant2 = Plant(user_id=1, name="Orquidea", plant_type="Floral Plant",
               garden=garden2)

session.add(plant2)
session.commit()

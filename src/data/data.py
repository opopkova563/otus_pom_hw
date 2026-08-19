import random
from faker import Faker

fake = Faker('en_US')


def generate_user():
    return {
        "gender": random.choice(["male", "female"]),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
        "birthdate": fake.date_of_birth().strftime("%m/%d/%Y")
    }

def generate_product():
    return {
        "product_name": fake.catch_phrase(),
        "summary": fake.text(max_nb_chars=100),
        "description": fake.text(max_nb_chars=100),
        "ISBN": fake.isbn13(),
        "min_value": fake.random_int(min=1, max=10),
        "retail_price": fake.random_int(min=6, max=10),
        "cost_price": fake.random_int(min=1, max=5)
    }

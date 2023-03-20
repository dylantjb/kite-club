from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import internet, person
from blogs.models import User, Club, Post, books
from blogs.helpers import get_genres, get_themes
import random
import logging
""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

"""setup"""
fake = Faker()
fake.add_provider(internet)
fake.add_provider(person)
user_list= []
themes = get_themes()

class Command(BaseCommand):
    help = "seed database for testing and development."

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')

def clear_data():
    """Deletes all the table data"""
    logging.info("Delete Address instances")
    User.objects.all().delete()


def create_user():
    """Creates an user object using faker"""
    logging.info("Creating user")
    fname = fake.unique.first_name()
    lname = fake.unique.last_name()
    user = User(
        username = "@" + fname + str(random.randint(0, 12)) + str(random.randint(1,9)),
        first_name = fname,
        last_name = lname,
        email = fname + "." + lname + "@" + fake.free_email_domain(),
        bio = fake.paragraph(nb_sentences=5)
    )
    user.save()
    logging.info("{} user created.".format(user))
    return user

def create_club():
    """Creates an user object using faker"""
    logging.info("Creating a club with exactly two admins and 10 members")
    club_owner = create_user()
    club = Club(
        owner = club_owner  ,
        name = fake.text(max_nb_chars=20),
        bio = fake.paragraph(nb_sentences=2),
        rules = fake.paragraph(nb_sentences=4),
        theme = (random.choice(themes))[1]
        
    )
    club.save()
    club.admins.add(create_user())
    club.admins.add(create_user())
    for i in range(10):
        current_user= create_user()
        club.members.add(current_user)
    logging.info("{} user created.".format(club))
    return club
def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        Club.objects.all().delete()
        Post.objects.all().delete()
        books.objects.all().delete()
        return

    # Creating 25 clubs
    for i in range(25):
        create_club()


import os
import sys
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE','robotic_club.settings')

import django
django.setup()

from core.models import BlogAndArticle


BlogAndArticle.objects.all().delete()
fake = Faker()

print(fake.sentence())
for _ in range(100):
    obj=BlogAndArticle(
        title=fake.sentence(),
        shortDescription=fake.sentence(nb_words=4),
        content=fake.sentence(nb_words=100),

    )
    obj.picture='../static/img/Rectangle 220.png'
    obj.save()


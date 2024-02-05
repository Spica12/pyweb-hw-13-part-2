import configparser
import pathlib
from datetime import datetime

from bson import json_util
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from mongoengine import (CASCADE, BooleanField, Document, ListField,
                         ReferenceField, StringField, connect)

from .models import Author, Quote, Tag

file_config = (
    pathlib.Path(__file__).parent.parent.parent.joinpath("configs").joinpath("config.ini")
)
print(file_config)
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("DEV_MONGO_DB", option="USER")
password = config.get("DEV_MONGO_DB", option="PASSWORD")
db = config.get("DEV_MONGO_DB", option="DB_NAME")

uri = f"mongodb+srv://{user}:{password}@cluster0.ae7t2cd.mongodb.net/?retryWrites=true&w=majority"
print(uri)

connect(db=db, host=uri)
print("Connected")


class AuthorMongo(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=120)
    description = StringField()

    meta = {"collection": "authors"}


class QuoteMongo(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(AuthorMongo, reverse_delete_rule=CASCADE)
    quote = StringField()

    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)


def seed_authors(request):

    authors = AuthorMongo.objects().all()

    for author_mongo in authors:
        try:
            born_date = datetime.strptime(author_mongo.born_date, '%B %d, %Y')
            author = Author(
                fullname=author_mongo.fullname,
                born_date=born_date,
                born_location=author_mongo.born_location,
                description=author_mongo.description,
            )

            author.save()

        except IntegrityError:
            print(f"Author {author_mongo.fullname} exists.")

    return redirect(to='quoteapp:main')


def seed_quotes(request):

    quotes = QuoteMongo.objects().all()

    for quote_mongo in quotes:

        author = Author.objects.filter(fullname=quote_mongo.author.fullname).first()

        quote = Quote(
            quote=quote_mongo.quote,
            author=author,
        )
        quote.save()

        tags_name = quote_mongo.tags
        for tag_name in tags_name:
            tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
            quote.tags.add(tag)


    return redirect(to='quoteapp:main')



# path_data = Path(__file__).parent.parent.parent.joinpath('data')


# def seed_authors(request):
#     file_name = "authors.json"
#     file_path = path_data.joinpath(file_name)
#     print(file_path)

#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         for el in data:
#             try:
#                 born_date = datetime.strptime(el.get("born_date"), '%B %d, %Y')
#                 author = Author(
#                     fullname=el.get("fullname"),
#                     born_date=born_date,
#                     born_location=el.get("born_location"),
#                     description=el.get("description"),
#                 )

#                 if author.fullname == "Alexandre Dumas-fils":
#                     author.fullname = "Alexandre Dumas fils"

#                 author.save()

#             except IntegrityError:
#                 print(f"Author {el.get('fullname')} exists.")

#     return redirect(to='quoteapp:main')


# def seed_quotes(request):
#     file_name = "quotes.json"
#     file_path = path_data.joinpath(file_name)
#     print(file_path)

#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         for el in data:
#             author = Author.objects.filter(fullname=el.get("author")).first()

#             if author is None:
#                 author = Author(fullname=el.get("author"))
#                 author.save()


#             quote = Quote(
#                 quote=el.get("quote"),
#                 author=author,
#             )
#             quote.save()

#             tags_name = el.get("tags")
#             for tag_name in tags_name:
#                 tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
#                 quote.tags.add(tag)


#     return redirect(to='quoteapp:main')

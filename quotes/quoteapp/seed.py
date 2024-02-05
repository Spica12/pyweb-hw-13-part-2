import json
from datetime import datetime
from pathlib import Path

from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, Quote, Tag
from .models import Author, Quote, Tag

path_data = Path(__file__).parent.parent.parent.joinpath('data')


def seed_authors(request):
    file_name = "authors.json"
    file_path = path_data.joinpath(file_name)
    print(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            try:
                born_date = datetime.strptime(el.get("born_date"), '%B %d, %Y')
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=born_date,
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )

                if author.fullname == "Alexandre Dumas-fils":
                    author.fullname = "Alexandre Dumas fils"

                author.save()

            except IntegrityError:
                print(f"Author {el.get('fullname')} exists.")

    return redirect(to='quoteapp:main')


def seed_quotes(request):
    file_name = "quotes.json"
    file_path = path_data.joinpath(file_name)
    print(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            author = Author.objects.filter(fullname=el.get("author")).first()

            if author is None:
                author = Author(fullname=el.get("author"))
                author.save()


            quote = Quote(
                quote=el.get("quote"),
                author=author,
            )
            quote.save()

            tags_name = el.get("tags")
            for tag_name in tags_name:
                tag, created = Tag.objects.get_or_create(name=tag_name, user=request.user)
                quote.tags.add(tag)


    return redirect(to='quoteapp:main')

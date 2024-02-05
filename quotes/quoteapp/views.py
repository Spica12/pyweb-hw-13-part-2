import collections

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Quote, Tag


# Create your views here.
def top_ten_tags():
    tags = Tag.objects.all()

    counter_tags = collections.Counter()

    for tag in tags.iterator():
        coutes_with_tag = Quote.objects.filter(tags=tag.id).all()
        counter_tags[tag] = len(coutes_with_tag)

    # print(counter_tags.most_common(10))
    most_common_tags = [tag for tag in dict(counter_tags.most_common(10))]

    return most_common_tags


def main(request):
    all_quotes = Quote.objects.all()
    items_per_page = 10
    paginator = Paginator(all_quotes, items_per_page)
    page = request.GET.get('page')

    try:
        quotes = paginator.page(page)

    except PageNotAnInteger:
        quotes = paginator.page(1)

    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)

    most_common_tags = top_ten_tags()

    return render(
        request,
        "quoteapp/index.html",
        {"quotes": quotes, "most_common_tags": most_common_tags},
    )


def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:main")
        else:
            return render(request, "quoteapp/tag.html", {"form": form})

    return render(request, "quoteapp/tag.html", {"form": TagForm()})


def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            author = Author.objects.filter(id=request.POST["author"]).first()
            new_quote.author = author

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quoteapp:main")
        else:
            return render(
                request,
                "quoteapp/quote.html",
                {"authors": authors, "tags": tags, "form": form},
            )

    return render(
        request,
        "quoteapp/quote.html",
        {"authors": authors, "tags": tags, "form": QuoteForm()},
    )


def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:main")
        else:
            return render(request, "quoteapp/author.html", {"form": form})

    return render(request, "quoteapp/author.html", {"form": AuthorForm()})


def detail(request, author_fullanme):
    author = get_object_or_404(Author, fullname=author_fullanme)

    return render(request, "quoteapp/detail.html", {"author": author})


def delete_all_quotes(request):
    quotes = Quote.objects.all()
    for quote in quotes:
        quote.delete()

    return redirect(to="quoteapp:main")


def delete_all_authors(request):
    authors = Author.objects.all()
    for author in authors:
        author.delete()

    return redirect(to="quoteapp:main")


def delete_all_tags(request):
    tags = Tag.objects.all()
    for tag in tags:
        tag.delete()

    return redirect(to="quoteapp:main")


def find_quotes_by_tag(request, tag):
    tag = Tag.objects.filter(name=tag).first()
    # quotes = []
    # all_quotes = Quote.objects.all()

    # for quote in all_quotes.iterator():
    #     tags = [str(tag) for tag in quote.tags.iterator()]
    #     if tag.name in tags:
    #         quotes.append(quote)

    quotes = Quote.objects.filter(tags=tag.id).all()

    return render(request, "quoteapp/quotes.html", {"quotes": quotes, 'viewing_tag': tag})

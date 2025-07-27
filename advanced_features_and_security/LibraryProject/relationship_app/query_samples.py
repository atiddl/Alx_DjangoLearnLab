import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    author_name = "Jane Austen"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = Book.objects.filter(author=author)
        print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")

    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in_library]}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")

    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
    except Librarian.DoesNotExist:
        print(f"No librarian found for library '{library_name}'")


    try:
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"Librarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for library '{library_name}'")

if __name__ == "__main__":
    run_queries()

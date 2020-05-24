from django.shortcuts import render
from catalog.models import Book, BookInstance, Author, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import Author

# Create your views here.
def index(request):

    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_genre = Genre.objects.all().count()
    num_books_count = Book.objects.filter(title__contains='The').count()

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    # wild_books = Book.objects.filter(title__contains='wild')

    context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_books_count': num_books_count,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model=Book
    paginate_by = 3

# The view passes the context (list of books) by default as object_list and book_list aliases; either will work.


    # context_object_name = 'my_book_list' #your own name for the list as a template
    # queryset = Book.objects.filter(title__icontains='The')[:5]
    # template_name = 'books/book_list.html' # Specify your own template name/location

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='the')[:5]

    # def get_context_data(self, **kwargs):
    #     # call the base implementation first to get the context
    #     context = super(BookListView,self).get_context_data(**kwargs)
    #     # create any data and add it to the context
    #     context["some_data"] = 'This is just some data'
    #     return context

class BookDetailView(generic.DetailView):
    model = Book

# All you need to do now is create a template called /locallibrary/catalog/templates/catalog/book_detail.html, and the view will pass it the database information for the specific Book record extracted by the URL mapper. Within the template you can access the list of books with the template variable named object OR book (i.e. generically "the_model_name").

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3

class AuthorDetailView(generic.DetailView):
    model = Author

    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/all_books_borrowed.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian"""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method =='POST':
        # Create a form instance and populate it with data from the request (binding)
        form = RenewBookForm(request.POST)

        # CHeck if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL
            return HttpResponseRedirect(reverse('all-borrowed'))
        # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_data = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_data})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2019'}

# By default, these views will redirect on success to a page displaying the newly created/edited model item, which in our case will be the author detail view we created in a previous tutorial.

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors') 
    # reverse("author-detail", args=[str(self.id)])

"""The "create" and "update" views use the same template by default, which will be named after your model: model_name_form.html (you can change the suffix to something other than _form using the template_name_suffix field in your view, for example template_name_suffix = '_other_suffix')"""

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
# By default, these views will redirect on success to a page displaying the newly created/edited model item, which in our case will be the book detail view we created in a previous tutorial.

class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
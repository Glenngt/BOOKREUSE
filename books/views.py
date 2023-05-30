from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order,Contact
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import JsonResponse
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView



def delete_book(request,pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return redirect('http://127.0.0.1:8000/manage/')


def update_book(request, pk):
    book = Book.objects.get(id=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        book_available = request.POST.get('book_available')
        if book_available=="on":
            f=True
        else:
            f=False

        if "image" in request.FILES:
            image = request.FILES["image"]
            book.image = image

        book.title = title
        book.author = author
        book.description = description
        book.price = price
        book.book_available=f

        book.save()

        return redirect('http://127.0.0.1:8000/manage/')

    context = {'book': book}
    return render(request, 'update_book.html', context)


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'add_book.html'
    fields = ['title', 'author', 'description', 'price', 'image','book_available']
    login_url = 'login'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BooksListView(ListView):
    model = Book
    template_name = 'list.html'


class LatestBooksListView(BooksListView):
    template_name = 'home.html'

    def get_queryset(self):
        return Book.objects.order_by('-id')[:4]


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'


class SearchResultsListView(ListView):
	model = Book
	template_name = 'search_results.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		return Book.objects.filter(
		Q(title__icontains=query) | Q(author__icontains=query)
	)


class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url     = 'login'


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	product = Book.objects.get(id=body['productId'])
	Order.objects.create(
		product=product
	)
	return JsonResponse('Payment completed!', safe=False)


class AboutUsView(TemplateView):
    template_name = 'aboutus.html'

class ContactUsView(TemplateView):
    template_name = 'contactus.html'
    fields=['name','email','request']

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        reuest = request.POST.get('request')  # Add this line


        return render(request, 'contactus.html')


class ManageListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'manage.html'
    login_url = 'login'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter the books by the logged-in user
        queryset = queryset.filter(user=self.request.user)
        return queryset




from django.shortcuts import render 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import JsonResponse
import json
from django.views.generic import TemplateView




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
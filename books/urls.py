
from django.urls import path
from .views import *
from .views import AddBookView, AboutUsView



urlpatterns = [
    path('', LatestBooksListView.as_view(), name='home'),
    path('list/', BooksListView.as_view(), name='list'),
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('contactus/',ContactUsView.as_view(),name="contactus"),
    path('manage/',ManageListView.as_view(),name="manage"),
    path('update/<int:pk>',update_book),
    path('delete/<int:pk>',delete_book)

]
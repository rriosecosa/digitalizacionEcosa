from django.urls import path
from .views import HomeView, NosotrosView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('nosotros/', NosotrosView.as_view(), name='nosotros'),
]
from django.urls import path

from . import views
from .tasks import update_prices_task

app_name = 'assets'
urlpatterns = [
    path('tasks/update-prices/', update_prices_task),
    path('manual-stimulation/', views.manual_price_stimulation, name="manual_stimulation"),
]
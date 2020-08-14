from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from main_app import views
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('events/', views.events_list, name='events'),
    path('create_event/', views.create_event, name='create_event'),
    path('event/<int:uni_id>/', views.view_event, name='event'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.signin, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('delete/<int:uni_id>', views.delete_event, name='delete_event'),
    path('event/<int:pk>/create_payment/', views.create_payment, name='create_payment'),
    path('delete_payment/<int:pk>', views.delete_payment, name='delete_payment'),
    path('ev_sort_date', views.event_date_sort, name='ev_sort_by_date'),
    path('pay_sort_date/<int:uni_id>', views.pay_date_sort, name='pay_date_sort'),
    path('pay_sort_sum/<int:uni_id>', views.pay_sum_sort, name='pay_sum_sort'),
    path('docs/', views.docs, name='docs')
] + static('docs/_static/', document_root=os.path.join(settings.BASE_DIR, 'Docs/build/html/_static'))



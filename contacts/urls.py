from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from contacts import views

app_name = 'contacts'
urlpatterns = [
    path('', views.contact_form, name='contact_insert'),
    path('<int:id>/', views.contact_form, name='contact_update'),
    path('delete/<int:id>/', views.contact_delete, name='contact_delete'),
    path('list/', views.contacts_list, name='contacts_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from editor import views


urlpatterns = [
    path('edit/', views.editor_window, name='editor_window'),

    path('save/', views.save_content, name='save'),
    path('new/', views.new_file_name, name='new_file'),
    path('delete/', views.delete_file, name='delete_file'),
    path('compile/', views.compile, name='compile'),

    path('sharing/<int:pk>/', views.sharing, name='sharing'),

    path('detail/<int:pk>/', views.detail_view, name='detail'),


]

from django.contrib import admin
from django.urls import path
from .views import get_message, upload_pdf, view_pdf, delete_pdf, index, upload_video, list_videos, get_video, upload_avatar, get_avatar, get_audio
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('view-pdf/<str:file_id>/', view_pdf, name='view_pdf'),
    path('delete-pdf/<int:pdf_id>/', delete_pdf, name='delete_pdf'),

    path('message/', views.get_message, name='get_message'),

    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path('', index, name='index'),

    path("api/upload/", views.upload_video, name="upload_video"),
    path("api/video/<str:file_id>/", views.get_video, name="get_video"),
    path("api/videos/", views.list_videos, name="list_videos"),
    path("api/delete-video/<str:file_id>/", views.delete_video, name="delete_video"),
    # path('api/generate-text/', views.generate_text, name='generate_text'),


    path("api/upload-avatar/", views.upload_avatar, name="upload_avatar"),
    path("api/avatar/<str:file_id>/", views.get_avatar, name="get_avatar"),

    path('webhook/', views.webhook_handler, name='webhook'),

    # path("text-to-speech/", views.text_to_speech, name="text_to_speech"),
    path("list-video/", views.list_videos, name="list_videos"),

    path("get-audio/", get_audio, name='get_audio'),
    
]

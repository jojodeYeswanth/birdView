from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from app import views
from django.conf.urls import url
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index.as_view(), name='home'),
    path('user-profile/', views.profile, name="profile"),
    url(r'^add/cage/$', views.AddCage, name='add-cage'),
    url(r'^add/bird/$', views.AddBird, name='add-bird'),
    path('select-option/', views.cageoption.as_view(), name='cageoption'),
    url(r'^bird-profile/$', views.BirdProfileView.as_view(), name='birds'),
    url(r'^image-list/$', views.BirdImageView.as_view(), name='images'),
    url(r'^video-list/$', views.BirdVideoView.as_view(), name='videos'),

    url(r'^/(?P<stream_path>(.*?))/$', views.dynamic_stream, name="videostream"),
    url(r'^detect-video/$', views.index_screen, name='detect_video'),
    url(r'^image-capture/$', views.image_capture, name='image-capture'),
    url(r'^video-capture/$', views.video_capture, name='video-capture'),
    path('make-image-public/<int:pk>/', views.make_image_public.as_view(), name='make-image-public'),
    path('make-video-public/<int:pk>/', views.make_video_public.as_view(), name='make-video-public'),

    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

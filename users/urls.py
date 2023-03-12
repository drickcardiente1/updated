from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', include('social_django.urls', namespace='social')),
    # socials close form
    path("close/", views.close, name="close"),
    # home
    path('', views.home, name='home'),
    # manual login
    path('login/', views.log_in_view, name='login'),
    # Profile View
    path('profile/', views.profile_view, name='profile'),
    # Profile Update Proccess
    path('update_profile/', views.update_profile, name='update_profile'),
    # Profile Update Picture Proccess
    path('update_profile_pic/', views.update_profile_pic, name='update_profile_pic'),
    # Profile Update Picture from saved
    path('update_profile_pic_from_saved/', views.update_profile_pic_from_saved, name='update_profile_pic_from_saved'),
    # Profile Picture save from take a photo
    path('save_profile_pic_from_take_picture/', views.save_profile_pic_from_take_picture, name='save_profile_pic_from_take_picture'),
    # manual login submit proccess
    # log-in proccess
    path('login_proccess/', views.log_in_proccess, name='login_proccess'),
    # forgot-password proccess
    path('forgot_password/', views.forgot_password_proccess, name='forgot_password'),
    # forgot-password proccess
    path('newpwd_confirmation/', views.forgot_password_confirm_proccess, name='newpwd_confirmation'),
    # logout
    path("logout/", views.signout, name='logout'),
    # signup manual
    path('signup/', views.sign_up_view, name='signup'),
    path('submit_register/', views.submit_register, name='submit_register'),
    path('send_otpregistration/', views.action_otpsendregistration, name='send_otpregistration'),
    # check users status
    path('user_stats/', views.user_stats, name='user_stats'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
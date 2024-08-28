from django.urls import path, include, re_path
from .views import AuthView

urlpatterns = [


    path('auth/',include('djoser.urls'),name='createuser'),
    re_path(r'^auth/', include('djoser.urls.authtoken'),name='token'),
    path('reg/',AuthView.reg,name='reg'),
    path('login/',AuthView.login,name='signin'),
    path('logout/',AuthView.logout,name='logOut')

]
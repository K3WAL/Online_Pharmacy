from re import template
from sre_constants import SUCCESS
from store import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, PasswordResetForm, MySetPasswordForm



urlpatterns = [
    path('', views.ProductView.as_view(), name="index"),
    path('home/', views.index, name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('collections/covid_essential', views.covid, name="covid"),
    path('collections/family_care', views.family, name="family"),
    path('collections/personal_care', views.personal, name="personal"),
    path('collections/ayurvedic', views.ayurvedic, name="ayurvedic"),
    path('collections/surgical', views.surgical, name="surgical"),
    path('collections/devices', views.devices, name="devices"),
    path('collections/immunity_booster', views.immunity, name="immunity"),
    path('collections/sexual_wellness', views.wellness, name="wellness"),
    path('collections/medicine', views.medicine, name="medicine"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', 
    authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', 
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), 
    name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', 
    form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',
     form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
     name='password_reset_complete'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart,),
    path('minuscart/', views.minus_cart,),
    path('removecart/', views.remove_cart,),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('buynow/', views.buynow, name='buynow'),
    path('prescription/', views.prescription, name="prescription"),
    path('newsletter/', views.newsletter, name="newsletter"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

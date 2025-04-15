# from django.contrib import admin
# from django.urls import path

# from . import views


from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

urlpatterns = [
        #Leave as empty string for base url
    path('admin-panel/', admin.site.urls),
    path('', views.store, name='store'),  # Root URL for the store view
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
        path('register/', views.register, name='register'),  # User registration
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(next_page='store'), name='logout'),
     path('add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Add to Cart URL
    path('product/<int:id>/', views.product_view, name='product_view'),  # Product View URL
     path('logout/', auth_views.LogoutView.as_view(next_page='store'), name='logout'),
     path('delete_item/', views.delete_item, name='delete_item'),  # Delete Item URL
     path('update_item/', views.update_item, name='update_item'),
     path('process_order/', views.processOrder, name="process_order"),



]
 
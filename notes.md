~~~shell
$ pip install -r requirements.txt
~~~

~~~shell
$ pip freeze > requirements.txt
~~~
<a name="top"></a>
### Tutorial

Firstly, create and activate a new virtual environment:
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   pip install django==3.2.12
   ```
   - python -m venv venv
   - venv\Scripts\activate
   - pip install django==3.2.12
___________________________________
--

### 1. Create project 
   ```
   python manage.py startapp products
   ```
---
### 2. app products:

1. Create app products
   ```pycon
   python manage.py startapp products
   ```
   
2. Registration products:
   ```
   settings.py -> 
   
   INSTALLED_APPS = [
      ....
    'products',
      ....
   ]
   ```
3. Create Templates:
   ```
   templates/products ->  ~~~.html
   ```
4. Create Views:
   ```
   products -> views.py 
   
   class IndexView(TemplateView):
   class ...ListView(ListView):
   class ...DetailView(DetailView):
   
   class ...View(View)

   CreateView, UpdateView, DeleteView
   ```

5. Create products/urls:
   ```
   products -> urls.py added urlpatterns
   
   urlpatterns = [
       path('', ProductsListView.as_view(), name='index'),
       path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
       path('product_details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
       path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
   
       path('comment-like/<int:comment_id>', CommentLikeView.as_view(), name='comment_like'),
       path('comment-like/admin/<int:comment_id>', CommentLikeAdminView.as_view(), name='comment_admin'),
       path('comment-delete/admin/<int:comment_id>/', CommentDeleteAdminView.as_view(), name='comment_delete_admin'),
   
       path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
       path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
   ]
   ```
6. Add in store/urls
   ```
   store -> urls.py added urlpatterns
   
   urlpatterns = [
       path('admin/', admin.site.urls),
   
       path('', IndexView.as_view(), name='index'),
       path('products/', include('products.urls', namespace='products')),
      ...
   ]
   ```

7. Create models:
   ```
   products -> models.py
   
   ProductCategory, Product, BasketQuerySet, Basket,
   PublishManager, PostLike, Comment, CommentLike,
   ```
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
8. Create createsuperuser
   ```
   python manage.py createsuperuser
   ```

9. Create forms:
   ```
   products -> forms.py
   
   CommentForm
   ```

10. Registration in admin panel:
   ```
   products -> admin.py
   
   ProductAdmin, BasketAdmin, CommentAdmin, CommentLikeAdmin
   ```


---
### 3. app users:

1. Create app users
   ```
   python manage.py startapp users
   ```
   
2. Registration products:
   ```
   settings.py -> 
   
   INSTALLED_APPS = [
      ....
    'users',
      ....
   ]
   ```
   
3. Create Templates:
   ```
   templates/users ->  ~~~.html
   ```
   
4. Create Views:
   ```
   users -> views.py 
   
   class UserLoginView(LoginView)
   class UserRegistrationView(CreateView)
   class UserProfileView(UpdateView)
   class EmailVerificationView(TemplateView)
   class DataGenerationView(FormView)

   ```

5. Create users/urls:
   ```
   users -> urls.py added urlpatterns
   
   urlpatterns = [
       path('login/', UserLoginView.as_view(), name='login'),  # ../users/login
       path('register/', UserRegistrationView.as_view(), name='register'),  # ../users/register
       path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),  # ../users/profile/1
       path('logout/', LogoutView.as_view(), name='logout'),
       path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
   
       path('service/', DataGenerationView.as_view(), name='service'),  # ../users/service
   ]
   ```
   
6. Add in store/urls
   ```
   store -> urls.py added urlpatterns
   
   urlpatterns = [
      ...
      path('users/', include('users.urls', namespace='users')),
      ...
   ]
   ```

7. Create models:
   ```
   users -> models.py
   
   User, EmailVerification
   ```
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
8. Create createsuperuser
   ```
   python manage.py createsuperuser
   ```

9. Create forms:
   ```
   users -> forms.py
   
   UserLoginForm, UserRegistrationForm, UserProfileForm, GenerateDataForm
   ```

10. Registration in admin panel:
   ```
   users -> admin.py
   
   UserAdmin, EmailVerificationAdmin
   ```


---
### 3. app orders:

1. Create app orders
   ```pycon
   python manage.py startapp orders
   ```
2. Registration orders:
   ```
   settings.py -> 
   
   INSTALLED_APPS = [
      ....
    'orders',
      ....
   ]
   ```
   
3. Create Templates:
   ```
   templates/orders ->  order-create.html
   ```
4. Create Views:
   ```
   orders -> views.py added OrderCreateView
   ```
5. Create orders/urls:
   ```
   orders -> urls.py added urlpatterns
   
   urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
   ]
   ```
6. Add in store/urls
   ```
   store -> urls.py added urlpatterns
   
   urlpatterns = [
    ...
   path('orders/', include('orders.urls', namespace='orders')),
   ]
   ```
7. Create models:
   ```
   orders -> models.py
   
   Order
   ```
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
8. Create forms:
   ```
   orders -> forms.py
   
   OrderForm
   ```

9. Registration in admin panel:
   ```
   orders -> admin.py
   
   OrderAdmin
   ```


___________________________________
---

* QuerySet
   https://docs.djangoproject.com/en/4.1/ref/models/querysets/

   ```pycon
   from products.models import ProductCategory
   category = ProductCategory.objects.get(id=1)
   category
   <ProductCategory: Clothes>
   ```
   
   ```pycon
   ProductCategory.objects.all()
   <QuerySet [<ProductCategory: Clothes>, <ProductCategory: New>, <ProductCategory: Shoes>, <ProductCategory: Accessories>, <ProductCategory: Present>]>
   ```
   
   ```pycon
   ProductCategory.objects.filter(description=None)
   <QuerySet []>
   ```

* Fixture
   ```bash
   python manage.py dumpdata products.ProductCategory > products/fixtures/categories.json
   python manage.py dumpdata products.Product > products/fixtures/goods.json
   ```
   
   ```pycon
   python manage.py loaddata products/fixtures/categories.json
   python manage.py loaddata products/fixtures/goods.json
   ```

* Test environ

   https://django-environ.readthedocs.io/en/latest/quickstart.html

   ```pycon
   from django.conf import settings

   settings.DEBUG
   True

   settings.DOMAIN_NAME
   'http://127.0.0.1:8000'

   ```





<a href="#top">UP</a>



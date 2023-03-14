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
10. stripe.com
    1. https://stripe.com/docs/checkout/quickstart?lang=python
    
    2. STRIPE
    ```pycon
    STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')
      ```
    3. ```pip3 install stripe```
    4. 
    ```
    checkout_session=..... 
    ```
    5. webhook
    
    https://stripe.com/docs/payments/checkout/fulfill-orders

    https://stripe.com/docs/stripe-cli#login-account
    
    ```
    C:\>stripe status
    
    ✔ All services are online.
    As of: March 12, 2023 @ 08:36PM +00:00
    ```
    6. create webhook
    
    ```
    C:\>stripe listen --forward-to 127.0.0.1:8000/webhook/stripe/
    
    Ready! You are using Stripe API Version [2022-11-15]. 
    Your webhook signing secret is whsec_73899a70b0c3418c309e0a8e3512d872366d7c7ceeb52d77f5575c633da6318 (^C to quit)
    ```
    ```
    2023-03-12 22:55:38   --> charge.succeeded [evt_3MkvvZIJNrmkY0J21uUcE2Eu]
    2023-03-12 22:55:38  <--  [200] POST http://127.0.0.1:8000/webhook/stripe/ [evt_3MkvvZIJNrmkY0J21uUcE2Eu]2023-03-12 22:55:38   --> checkout.session.completed [evt_1MkvvaIJNrmkY0J2h73o3k8z]
    2023-03-12 22:55:38   --> payment_intent.succeeded [evt_3MkvvZIJNrmkY0J21aGhZDEK]
    2023-03-12 22:55:38   --> payment_intent.created [evt_3MkvvZIJNrmkY0J21gWLPRYz]
    2023-03-12 22:55:38  <--  [200] POST http://127.0.0.1:8000/webhook/stripe/ [evt_1MkvvaIJNrmkY0J2h73o3k8z]2023-03-12 22:55:38  <--  [200] POST http://127.0.0.1:8000/webhook/stripe/ [evt_3MkvvZIJNrmkY0J21aGhZDEK]2023-03-12 22:55:38  <--  [200] POST http://127.0.0.1:8000/webhook/stripe/ [evt_3MkvvZIJNrmkY0J21gWLPRYz]
    ```
    7. api <a href="#create_stripe_product_price">create_stripe_product_price</a>

    https://stripe.com/docs/api/checkout/sessions/create#create_checkout_session-line_items-price_data
    https://stripe.com/docs/payments/accept-a-payment




11. Create Templates:
    ```
    templates/orders ->  
    
    canceled.html
    success.html
    ```
12. Create Views:
    ```
    orders -> views.py 
    SuccessTemplateView, CanceledTemplateView
    ```

13. Create orders/urls:
    ```pycon
    urlpatterns = [
    ...

    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    ]
    ```
14. Create your event handler
    ```
    orders -> views.py 
    
    def stripe_webhook_view
    ```
    
15. Add in store/urls
    ```
    store -> urls.py added urlpatterns
    
    urlpatterns = [
    ...
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),
    ...
    ]
    ```
    
15. Add in products/models

    ```
    products -> models.py added 
    def save()
    def create_stripe_product_price()

    ```
    
16. Add in products/models
    
    <a href="#de_json">de_json</a>
    ```
    products -> models.py added 
    def de_json(self)

    ```
    
17. Add in orders/models

    <a href="#basket_history">basket_history</a>

    ```
    products -> models.py added 
    def de_json(self)
    
    orders -> models.py added 
    def update_after_payment(self)

    ```

18. Create Templates:
   ```
   templates/orders ->  orders.html
   ```
19. Create Views:
   ```
   orders -> views.py added OrderListView
   ```
20. Create orders/urls:
   ```
   orders -> urls.py added urlpatterns
   
   urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
   ]
   ```

21. Create Templates:
   ```
   templates/orders ->  order.html
   ```
22. Create Views:
   ```
   orders -> views.py added OrderDetailView
   ```
23. Create orders/urls:
   ```
   orders -> urls.py added urlpatterns
   
   urlpatterns = [
    path('', OrderDetailView.as_view(), name='order'),
   ]
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
  
* Test reverse

   ```pycon
    from django.conf import settings
    from django.urls import reverse
  
    success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success'))
    success_url
    'http://127.0.0.1:8000/orders/order-success/'
  
    cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled'))
    cancel_url
    'http://127.0.0.1:8000/orders/order-canceled/'

   ```

* Test create_stripe_product_price()

    <a name="create_stripe_product_price"></a>
   ```pycon
    from products.models import Product
    product = Product.objects.last()
  
    product.create_stripe_product_price()
  
    <Price price id=price_1MkwUFIJNrmkY0J2SnTs4QC7 at 0x230acb52750> JSON: {
      "active": true,
      "billing_scheme": "per_unit",
      "created": 1678656687,
      "currency": "usd",
      "custom_unit_amount": null,
      "id": "price_1MkwUFIJNrmkY0J2SnTs4QC7",
      "livemode": false,
      "lookup_key": null,
      "metadata": {},
      "nickname": null,
      "object": "price",
      "product": "prod_NVyRa1eLdcGyZg",
      "recurring": null,
      "tax_behavior": "unspecified",
      "tiers_mode": null,
      "transform_quantity": null,
      "type": "one_time",
      "unit_amount": 2499,
      "unit_amount_decimal": "2499"
    }

   ```

* Test de_json

    <a name="de_json"></a>
   ```pycon
    from products.models import Basket, Product
    basket = Basket.objects.last()
    basket.de_json()
    {'product_name': 'Short Chiffon Dress', 'quantity': 1, 'price': 49.99, 'sum': 49.99}

   ```
  
* Test basket_history

    <a name="basket_history"></a>
   ```pycon
    from orders.models import Order
    order = Order.objects.get(id=12)
    order
    <Order: Order #12. Petro Sky>
    order.basket_history
    {'purchased_items': [{'product_name': 'Short Dress', 'quantity': 1, 'price': 24.99, 'sum': 24.99},
   {'product_name': 'Short Chiffon Dress', 'quantity': 1, 'price': 49.99, 'sum': 49.99}], 'total_sum': 74.98}
   ```

*  django_extensions
    ```
   python manage.py shell_plus
   ```



<a href="#top">UP</a>



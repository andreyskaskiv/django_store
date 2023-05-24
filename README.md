# **Django Store Project**

### What is implemented in this application:

<a name="top"></a>

1. Class base view &#9989;
2. Database Postgresql &#9989;
3. OAuth &#9989;
4. TestCase &#10060;/&#9989;
5. <a href="#Integration_testing"> Integration testing </a> - &#9989;
6. Caching, Redis &#9989;
7. Generation goods &#9989;
8. django-debug-toolbar &#9989;
9. Celery &#9989;
10. stripe &#9989;


---


<a href="Tutorial.md">Tutorial.md</a>

---

1. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run project dependencies, migrations, fill the database with the fixture data etc.:

   ```bash
   systemctl start postgresql.service 
   systemctl status postgresql.service
   ```
   
   Create a database, section 5 in the <a href="Tutorial.md">Tutorial.md</a>
  
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
   Fixtures:
   ```bash
   python manage.py loaddata <path_to_fixture_files>
   
   python manage.py loaddata products/fixtures/categories.json
   python manage.py loaddata products/fixtures/goods.json
   ```
   Redis:
   ```bash
   sudo systemctl start redis
   sudo systemctl status redis 
   ```
   Celery:   
   ```bash
   celery -A store worker -l INFO
   ```
   Stripe:   
   ```bash
   ./stripe status
   ```
3. Runserver
   ```bash
   python manage.py runserver
   ```



### Selenium test:
<a name="Integration_testing"></a>
![tests_integration_animation.gif](docs%2Ftests_integration_animation.gif)



<a href="#top">UP</a>
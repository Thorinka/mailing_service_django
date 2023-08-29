# Skychimp

Django project, which allows you to create and send messages to your clients. Also there's a blog for promotion.

Requirements:
asgiref==3.7.2
async-timeout==4.0.3
Django==4.2.4
django-crontab==0.7.1
Pillow==10.0.0
psycopg2==2.9.7
python-dotenv==1.0.0
pytils==0.4.1
redis==5.0.0
sqlparse==0.4.4
typing_extensions==4.7.1
tzdata==2023.3

.env
This application needs you to create ".env" file. Then you need to set all constants. For example, there is structure for ".env" file:
CACHE_ENABLED=1
CACHE_LOCATION=redis://127.0.0.1:6379

EMAIL_HOST_USER=email@host.com
EMAIL_HOST_PASSWORD=verysecretpassword
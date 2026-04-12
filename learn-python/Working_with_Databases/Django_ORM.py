# Django ORM: Object-Relational Mapping

# Install Django
print("pip install django")

# Create a Django project and app
print("django-admin startproject myproject")
print("cd myproject")
print("python manage.py startapp myapp")

# Define a model in models.py
print("class User(models.Model):\n    name = models.CharField(max_length=100)\n    age = models.IntegerField()")

# Run migrations
print("python manage.py makemigrations")
print("python manage.py migrate")

# Query the database
print("User.objects.all()")

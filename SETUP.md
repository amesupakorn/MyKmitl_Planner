## Setup

```python
# Create project folder
mkdir my_projects

# Create a virtual environment (Windows)
py -m venv myvenv

# Activate virtual environment (Windows)
myvenv\Scripts\activate.bat

# Create a virtual environment (MacOS)
python3 -m venv myvenv

# Activate virtual environment (MacOS)
source myvenv/bin/activate

pip install django

# Create project "myblogs"
django-admin startproject myblogs

# Create the "blogs" app
python manage.py startapp blogs
```

> ติดตั้ง Potgres Client `psycopg2` ติดตั้ง `django-extensions` และ `jupyter notebook` ด้วยคำสั่ง
> 

```python
pip install psycopg2

pip install psycopg2-binary

pip install django-extensions ipython jupyter notebook

pip install ipython==8.25.0 jupyter_server==2.14.1 jupyterlab==4.2.2 jupyterlab_server==2.27.2

pip install notebook==6.5.6
#หากติดตั้ง หรือ run jupyter ไม่ได้ให้ลองเปลี่ยน notebook version ดังนี้ 6.5.7

```

จากนั้นสร้าง directory ชื่อ `notebooks`

```
mkdir notebooks
```

> **DB ใน postgres แก้ใน setting.py**
> 

```
# Database setting
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "myapp",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Add app blogs to INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Add your apps here
    "django_extensions",
    "blogs",
]
```

> makemigrations เพื่อให้ Django ทำการสร้างไฟล์ migration ขึ้นมา
> 

```python
python manage.py makemigrations
python manage.py migrate
```

ทำการ start Jupyter Notebook server ด้วย command

```
python manage.py shell_plus --notebook
```

ใน Cell แรกของไฟล์ Notebook เพิ่ม code นี้ลงไป

```python
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
```
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
pip install django psycopg2 

# Create project "myblogs"
django-admin startproject myblogs

# Create the "blogs" app
python manage.py startapp blogs
```
> makemigrations เพื่อให้ Django ทำการสร้างไฟล์ migration ขึ้นมา
> 

```python
python manage.py makemigrations
python manage.py migrate
```


ติดตั้งแพ็กเกจ django-tailwind ผ่าน pip:
python -m pip install django-tailwind
​​
หรือคุณสามารถติดตั้งเวอร์ชันล่าสุดที่กำลังพัฒนาได้จาก:

python -m pip install git+https://github.com/timonweb/django-tailwind.git
​

สร้างแอป Django ที่ใช้ร่วมกับ Tailwind CSS โดยใช้คำสั่ง:

python3 manage.py tailwind init

python3 manage.py tailwind install
​
สุดท้าย คุณสามารถใช้คลาส Tailwind CSS ใน HTML ของคุณได้แล้ว เริ่มเซิร์ฟเวอร์พัฒนาโดยรันคำสั่ง:

python3 manage.py tailwind start

```
python manage.py tailwind install

pip install django-allauth

pip install django-widget-tweaks

pip install django-jwt

pip3 install PyJWT

pip install cryptography

pip install fido2

pip install djangorestframework

pip install Pillow



```
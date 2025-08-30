# Terminal Testing

First: run `python manage.py runserver`

Testing (bisa gunakan http://127.0.0.1:8000/admin)

email: user@example.com
password: useruser

## Signup user baru
curl -X POST -H "Content-Type: application/json" -d '{"username":"diana", "email":"diana@mail.com", "password":"123"}' http://127.0.0.1:8000/api/signup/

## Login
curl "http://127.0.0.1:8000/api/login/?username=andi&password=pasien123"

## Get user detail (andi punya id=4 dari seeder)
curl http://127.0.0.1:8000/api/user/4/

## Get semua service
curl http://127.0.0.1:8000/api/services/

## Get semua appointment
curl http://127.0.0.1:8000/api/appointments/

# Dashboard Testing

Step:
1. run `python manage.py runserver`
2. Open another terminal, run `streamlit run dashboard_django.py`
# Terminal Testing

First: run `python app.py`

Testing

## Signup user baru
curl -X POST -H "Content-Type: application/json" -d '{"username":"baru", "email":"baru@mail.com", "password":"123"}' http://127.0.0.1:5000/api/signup/

## Login (sesuai brief, via GET)
curl "http://127.0.0.1:5000/api/login/?username=andi&password=pasien123"

## Get user detail
curl http://127.0.0.1:5000/api/user/4/

## Get semua service
curl http://127.0.0.1:5000/api/services/

## Get semua appointment
curl http://127.0.0.1:5000/api/appointments/

## Batalkan appointment dengan ID 1
curl -X POST http://127.0.0.1:5000/api/appointments/1/cancel/



# Dashboard Testing

Step:
1. Run `python app.py`
2. Open another terminal, run `streamlit run dashboard.py`
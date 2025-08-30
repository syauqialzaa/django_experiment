import os
import django
from datetime import datetime, timedelta

# Ganti 'healthlinkr_project' jika nama folder proyek Anda berbeda
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthlinkr_project.settings')
django.setup()

from api.models import CustomUser, HealthFacility, Service, Appointment

def run_seed():
    print("Deleting old data...")
    Appointment.objects.all().delete()
    Service.objects.all().delete()
    HealthFacility.objects.all().delete()
    CustomUser.objects.all().delete()

    print("Creating new data...")
    
    # Users
    # --- BARIS YANG DIPERBAIKI ---
    admin = CustomUser.objects.create_superuser(username='admin', email='admin@health.com', password='admin123', role=CustomUser.Role.ADMINISTRATOR)
    
    dr_budi = CustomUser.objects.create_user(username='dr.budi', email='budi@health.com', password='dokter123', role=CustomUser.Role.DOCTOR)
    dr_susan = CustomUser.objects.create_user(username='dr.susan', email='susan@health.com', password='dokter123', role=CustomUser.Role.DOCTOR)
    andi = CustomUser.objects.create_user(username='andi', email='andi@mail.com', password='pasien123', role=CustomUser.Role.PATIENT)
    
    print(f"{CustomUser.objects.count()} users created.")

    # Facilities
    rs_sehat = HealthFacility.objects.create(name="RS Sehat Selalu", address="Jl. Kesehatan No. 1, Jakarta")
    klinik_ceria = HealthFacility.objects.create(name="Klinik Ceria", address="Jl. Bahagia No. 2, Jakarta")
    print(f"{HealthFacility.objects.count()} facilities created.")
    
    # Services
    konsul_umum = Service.objects.create(name="Konsultasi Umum", facility=rs_sehat)
    konsul_umum.available_doctors.add(dr_budi)
    konsul_gigi = Service.objects.create(name="Konsultasi Gigi", facility=klinik_ceria)
    konsul_gigi.available_doctors.add(dr_susan)
    print(f"{Service.objects.count()} services created.")

    # Appointment
    Appointment.objects.create(patient=andi, doctor=dr_budi, service=konsul_umum, appointment_time=datetime.now() + timedelta(days=3))
    print(f"{Appointment.objects.count()} appointments created.")

    print("Seeding complete!")

if __name__ == '__main__':
    run_seed()
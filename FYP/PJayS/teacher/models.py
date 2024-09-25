from django.db import models
import random
import string
import uuid
# Create your models here.

def generate_teacher_id():
    prefix = 'PJAYS'
    counter = random.randint(1000, 9999)  # Adjust range as needed
    member_id = f"{prefix}{str(counter).zfill(6)}"
    return member_id

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True, auto_created=True)  # Sesuaikan panjang sesuai kebutuhan
    nama = models.CharField(max_length=100)
    ic_cikgu = models.CharField(max_length=12, unique=True)
    jantina = models.CharField(max_length=10, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])
    kaum = models.CharField(max_length=50, choices=[('IBAN ATAU SEA DAYAK', 'IBAN  ATAU SEA DAYAK'), ('TEMIAR', 'TEMIAR'),('INDO', 'INDO'),('KADAZAN','KADAZAN'),('KAYAN','KAYAN'),('MELAYU','MELAYU'),('ORANG ASLI','ORANG ASLI'),('SEMAI','SEMAI'),('THAI','THAI'),('LAIN-LAIN','LAIN-LAIN')])  # Dropdown
    agama = models.CharField(max_length=50, choices=[('BUDDHA', 'BUDDHA'), ('ISLAM', 'ISLAM'),('KRISTIAN','KRISTIAN'),('TAO','TAO'),('TIADA AGAMA','TIADA AGAMA'),('TERATAI','TERATAI'),('LAIN-LAIN','LAIN-LAIN')] )  # Dropdown
    alamat_rumah = models.CharField(max_length=255)  # Dropdown
    pangkat = models.CharField(max_length=50, choices=[('Pengerusi', 'Pengerusi'), ('Naib Pengerusi', 'Naib Pengerusi'), ('Pegawai Ehwal Ekonomi','Pegawai Ehwal Ekonomi'), ('Penolong Pegawai Ehwal Ekonomi', 'Penolong Pegawai Ehwal Ekonomi'), ('Juruaudit','Juruadit'), ('Penolong Juruaudit', 'Penolong Juruaudit'), ('Guru Biasa','Guru Biasa'), ('Lain-lain','Lain-lain') ])  # Dropdown
    ahli = models.CharField(max_length=11, choices=[('Aktif', 'Aktif'),('Tidak Aktif', 'Tidak Aktif')], default='Aktif')
    modal_syer = models.DecimalField(max_digits=10, decimal_places=2)
    tarikh_daftar = models.DateField()

    def __str__(self):
        return self.nama

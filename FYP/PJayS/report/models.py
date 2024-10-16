from django.db import models
from django.core.validators import RegexValidator
from student.models import Member  # Adjust this import
from teacher.models import Teacher  # Import your Teacher model

class Report(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Member model
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Teacher model

    # Personal details
    nama = models.CharField(max_length=100)
    
    # Add IC for student and teacher
    ic_pelajar = models.CharField(
        max_length=12, 
        unique=True,
        validators=[RegexValidator(r'^\d{12}$', message="IC must be exactly 12 digits")]
    )
    
    ic_cikgu = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(r'^\d{12}$', message="IC must be exactly 12 digits")]
    )
    
    jantina = models.CharField(max_length=10, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])

    kaum = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('IBAN ATAU SEA DAYAK', 'IBAN ATAU SEA DAYAK'),
        ('INDONESIA', 'INDONESIA'),
        ('KADAZAN', 'KADAZAN'),
        ('KAYAN', 'KAYAN'),
        ('MELAYU', 'MELAYU'),
        ('ORANG ASLI', 'ORANG ASLI'),
        ('SEMAI', 'SEMAI'),
        ('THAI', 'THAI'),
        ('LAIN-LAIN', 'LAIN-LAIN')
    ])

    agama = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('BUDDHA', 'BUDDHA'),
        ('ISLAM', 'ISLAM'),
        ('KRISTIAN', 'KRISTIAN'),
        ('TIADA AGAMA', 'TIADA AGAMA'),
        ('LAIN-LAIN', 'LAIN-LAIN')
    ])

    alamat_rumah = models.CharField(max_length=255)

    tingkatan = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ])

    kelas = models.CharField(max_length=50, choices=[
        ('-', '-'),
        ('ANGGERIK', 'ANGGERIK'),
        ('CEMPAKA', 'CEMPAKA'),
        ('DAHLIA', 'DAHLIA'),
        ('MAWAR', 'MAWAR'),
        ('SEROJA', 'SEROJA'),
        ('TERATAI', 'TERATAI'),
        ('UM', 'UM'),
        ('UKM', 'UKM'),
        ('USM', 'USM'),
        ('LILY', 'LILY')
    ])

    pangkat = models.CharField(max_length=50, choices=[
        ('Pengerusi', 'Pengerusi'),
        ('Naib Pengerusi', 'Naib Pengerusi'),
        ('Pegawai Ehwal Ekonomi', 'Pegawai Ehwal Ekonomi'),
        ('Penolong Pegawai Ehwal Ekonomi', 'Penolong Pegawai Ehwal Ekonomi'),
        ('Juruaudit', 'Juruaudit'),
        ('Penolong Juruaudit', 'Penolong Juruaudit'),
        ('Guru Biasa', 'Guru Biasa'),
        ('Lain-lain', 'Lain-lain')
    ])  # Dropdown for rank

    ahli = models.CharField(max_length=11, choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif')
    modal_syer = models.DecimalField(max_digits=10, decimal_places=2)
    tarikh_daftar = models.DateField()

    def __str__(self):
        return self.nama

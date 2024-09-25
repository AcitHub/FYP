from django.db import models

def generate_member_id():
    prefix = "MEM"
    try:
        last_member = Member.objects.filter(member_id__startswith=prefix).order_by('-member_id').first()
        if last_member and last_member.member_id[len(prefix):]:
            last_id_num = int(last_member.member_id[len(prefix):])
        else:
            last_id_num = 0
    except (ValueError, TypeError) as e:
        print(f"Error in generate_member_id: {e}")
        last_id_num = 0

    new_id_num = last_id_num + 1
    new_id = f"{prefix}{new_id_num:04d}"
    print(f"Generated new ID: {new_id}")
    return new_id

class Member(models.Model):
    member_id = models.CharField(max_length=8, primary_key=True, editable=False, default=generate_member_id)
    nama = models.CharField(max_length=100)
    ic_pelajar = models.CharField(max_length=12, unique=True)
    jantina = models.CharField(max_length=10, choices=[('Lelaki', 'Lelaki'), ('Perempuan', 'Perempuan')])
    kaum = models.CharField(max_length=50, choices=[('-', '-'), ('IBAN', 'IBAN'), ('INDO', 'INDO'), ('KADAZAN', 'KADAZAN'), ('KAYAN', 'KAYAN'), ('MELAYU', 'MELAYU'), ('ORANG ASLI', 'ORANG ASLI'), ('SEMAI', 'SEMAI'), ('THAI', 'THAI'), ('LAIN-LAIN', 'LAIN-LAIN')])
    agama = models.CharField(max_length=50, choices=[('-', '-'), ('BUDDHA', 'BUDDHA'), ('ISLAM', 'ISLAM'), ('KRISTIAN', 'KRISTIAN'), ('TIADA AGAMA', 'TIADA AGAMA'), ('LAIN-LAIN', 'LAIN-LAIN')])
    alamat_rumah = models.CharField(max_length=255)
    tingkatan = models.CharField(max_length=50, choices=[('-', '-'),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    kelas = models.CharField(max_length=50, choices=[('-', '-'),('ANGGERIK', 'ANGGERIK'), ('CEMPAKA', 'CEMPAKA'), ('DAHLIA', 'DAHLIA'), ('MAWAR', 'MAWAR'), ('SEROJA', 'SEROJA'), ('TERATAI', 'TERATAI'), ('UM', 'UM'), ('UKM', 'UKM'), ('USM', 'USM'), ('LILY', 'LILY')])
    ahli = models.CharField(max_length=11, choices=[('Aktif', 'Aktif'), ('Tidak Aktif', 'Tidak Aktif')], default='Aktif')
    modal_syer = models.DecimalField(max_digits=10, decimal_places=2)
    tarikh_daftar = models.DateField()

    def __str__(self):
        return self.nama

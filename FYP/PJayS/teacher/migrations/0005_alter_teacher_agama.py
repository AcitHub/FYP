# Generated by Django 5.1.1 on 2024-10-13 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_teacher_kaum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='agama',
            field=models.CharField(choices=[('BUDDHA', 'BUDDHA'), ('ISLAM', 'ISLAM'), ('KRISTIAN', 'KRISTIAN'), ('TAO', 'TAO'), ('TIADA AGAMA', 'TIADA AGAMA'), ('LAIN-LAIN', 'LAIN-LAIN')], max_length=50),
        ),
    ]

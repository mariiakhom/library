# Generated by Django 4.2 on 2023-04-26 15:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_genre_options_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('a', 'Available'), ('o', 'On loan')], default='a', max_length=1)),
                ('due_back', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='library.book')),
            ],
        ),
    ]

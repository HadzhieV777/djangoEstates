# Generated by Django 4.0.3 on 2022-03-22 12:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('One bedroom apartment', 'One bedroom apartment'), ('Two bedrooms apartment', 'Two bedrooms apartment'), ('Three bedrooms apartment', 'Three bedrooms apartment'), ('Maisonette', 'Maisonette'), ('Single family house', 'Single family house'), ('Duplex', 'Duplex'), ('Vacation home', 'Vacation home'), ('Office', 'Office'), ('Hotel', 'Hotel'), ('Special-purpose', 'Special-purpose'), ('Industrial', 'Industrial'), ('Land', 'Land')], max_length=24)),
                ('location', models.CharField(max_length=150)),
                ('floor', models.CharField(choices=[('Ground Floor', 'Ground Floor'), ('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'), ('8th', '8th'), ('9th', '9th'), ('10th', '10th'), ('11th', '11th'), ('12th', '12th'), ('13th', '13th'), ('14th', '14th'), ('15th', '15th'), ('Last Floor', 'Last Floor')], max_length=12)),
                ('heating_type', models.CharField(choices=[('Forced Air System', 'Forced Air System'), ('Steam Radiant Heat Systems', 'Steam Radiant Heat Systems'), ('Electric System', 'Electric System'), ('Geothermal System', 'Geothermal System')], max_length=26)),
                ('area', models.FloatField()),
                ('exposition', models.CharField(choices=[('East', 'East'), ('West', 'West'), ('North', 'North'), ('South', 'South')], max_length=5)),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('type_of_transaction', models.CharField(choices=[('For sale', 'For sale'), ('For rent', 'For rent')], max_length=8)),
                ('description', models.TextField(max_length=500)),
                ('amenities', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator(message="The ingredients should be separated by ', '.", regex='^[a-zA-Z]+(, [a-zA-Z]+)*$')])),
                ('main_image', models.ImageField(upload_to='')),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('publication_date',),
            },
        ),
        migrations.CreateModel(
            name='EstateImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='estates/')),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.estate')),
            ],
        ),
    ]

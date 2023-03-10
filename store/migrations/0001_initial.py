# Generated by Django 4.0.6 on 2022-07-28 16:17

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
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
                ('area', models.CharField(choices=[('kathmandu', 'Thamel'), ('kathmandu', 'Swayambhu'), ('kathmandu', 'Gausal'), ('Lalitpur', 'Lagankhel'), ('Lalitpur', 'Pulchowk'), ('Lalitpur', 'Jawlakhel'), ('kathmandu', 'Kapan'), ('kathmandu', 'Budhanilkantha'), ('kathmandu', 'Asan'), ('kathmandu', 'Kotwshwor'), ('kathmandu', 'Baneshwor'), ('Lalitpur', 'Satdobato'), ('Lalitpur', 'Balkumari'), ('kathmandu', 'Ratopul'), ('kathmandu', 'Kalopul')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('CE', 'Covid Essential'), ('FC', 'Family Care'), ('PC', 'Personal Care'), ('A', 'Ayurvedic'), ('S', 'Surgical'), ('D', 'Devices'), ('IB', 'Immunity Booster'), ('SW', 'Sexual Wellness'), ('M', 'Medicne')], max_length=3, null='True')),
                ('product_image', models.ImageField(null='True', upload_to='store/static/online')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.collection')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='Pending', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='featured_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='store.product'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product, Order, OrderItem
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Superuser "admin" (password: admin123) created.')

        # Create Sample User
        if not User.objects.filter(username='user').exists():
            u = User.objects.create_user('user', 'user@example.com', 'user123')
            u.first_name = 'Nguyễn'
            u.last_name = 'Văn A'
            u.save()
            self.stdout.write('Sample user "user" (password: user123) created.')

        # Create Categories
        categories = ['Hoa Hồng', 'Hoa Lan', 'Hoa Cẩm Tú Cầu', 'Hoa Hướng Dương', 'Hoa Tulip']
        cat_objs = []
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'description': f'Các loại {cat_name} tươi đẹp.'}
            )
            cat_objs.append(cat)

        # Create Products
        products_data = [
            ('Bó Hồng Đỏ Tình Yêu', 500000, 10, 'Hoa Hồng'),
            ('Hồng Trắng Tinh Khôi', 450000, 5, 'Hoa Hồng'),
            ('Lan Hồ Điệp Sang Trọng', 1200000, 3, 'Hoa Lan'),
            ('Cẩm Tú Cầu Xanh Mát', 350000, 8, 'Hoa Cẩm Tú Cầu'),
            ('Hướng Dương Rạng Rỡ', 250000, 15, 'Hoa Hướng Dương'),
            ('Tulip Hà Lan Rực Rỡ', 600000, 7, 'Hoa Tulip'),
            ('Bó Hoa Mix Pastel', 700000, 4, 'Hoa Hồng'),
            ('Giỏ Hoa Chúc Mừng', 900000, 2, 'Hoa Lan'),
        ]

        for name, price, stock, cat_name in products_data:
            category = Category.objects.get(name=cat_name)
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'price': price,
                    'stock': stock,
                    'category': category,
                    'description': f'Đây là mô tả chi tiết cho {name}. Hoa tươi được nhập khẩu và bảo quản kỹ lưỡng.',
                    'available': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))

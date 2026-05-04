from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name="Ảnh đại diện")

    def __str__(self):
        return f"Hồ sơ của {self.user.username}"

    class Meta:
        verbose_name = "Hồ sơ người dùng"
        verbose_name_plural = "Hồ sơ người dùng"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Mô tả")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Danh mục")
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Hình ảnh")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    stock = models.PositiveIntegerField(verbose_name="Số lượng tồn kho")
    available = models.BooleanField(default=True, verbose_name="Sẵn bán")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
        ('shipped', 'Đang giao'),
        ('completed', 'Hoàn thành'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Người đặt")
    first_name = models.CharField(max_length=50, verbose_name="Tên")
    last_name = models.CharField(max_length=50, verbose_name="Họ")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=250, verbose_name="Địa chỉ")
    postal_code = models.CharField(max_length=20, verbose_name="Mã bưu điện")
    city = models.CharField(max_length=100, verbose_name="Thành phố")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'

    def __str__(self):
        return f'Đơn hàng {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Đơn hàng")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Sản phẩm")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

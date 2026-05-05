from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, OrderCreateForm
from .models import Category, Product, Order, OrderItem
from django.db.models import Q, Sum, Count
from django.contrib.admin.views.decorators import staff_member_required
import json
import os
import urllib.error
import urllib.request


def _ollama_chat(system_prompt: str, user_message: str, timeout: int = 120):
    """Gọi Ollama (/api/chat) — mặc định Llama 3.2 cục bộ."""
    base = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434').rstrip('/')
    model = os.getenv('OLLAMA_MODEL', 'llama3.2')
    url = f'{base}/api/chat'
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt.strip()},
            {'role': 'user', 'content': user_message.strip()},
        ],
        'stream': False,
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode())
        msg = (body or {}).get('message') or {}
        text = (msg.get('content') or '').strip()
        return text if text else None
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None

@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(paid=True).aggregate(Sum('items__price'))['items__price__sum'] or 0
    total_users = User.objects.count()
    total_products = Product.objects.count()
    
    # Doanh thu theo tháng (6 tháng gần nhất)
    from django.db.models.functions import TruncMonth
    from django.utils import timezone
    from datetime import timedelta

    six_months_ago = timezone.now() - timedelta(days=180)
    revenue_by_month = Order.objects.filter(paid=True, created__gte=six_months_ago) \
        .annotate(month=TruncMonth('created')) \
        .values('month') \
        .annotate(total=Sum('items__price')) \
        .order_by('month')

    months_labels = [r['month'].strftime('%m/%Y') for r in revenue_by_month]
    revenue_data = [float(r['total']) for r in revenue_by_month]

    # Thống kê trạng thái đơn hàng
    status_stats = Order.objects.values('status').annotate(count=Count('id'))
    status_labels = []
    status_counts = []
    status_dict = dict(Order.STATUS_CHOICES)
    for stat in status_stats:
        status_labels.append(status_dict.get(stat['status'], stat['status']))
        status_counts.append(stat['count'])
    
    # Top 5 sản phẩm bán chạy
    top_products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]
    
    # Đơn hàng gần đây
    recent_orders = Order.objects.order_by('-created')[:10]

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'months_labels': json.dumps(months_labels),
        'revenue_data': json.dumps(revenue_data),
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
        'top_products': top_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'shop/admin/dashboard.html', context)
from .cart import Cart
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Chatbot View
def chatbot_response(request):
    user_message = request.GET.get('message', '').strip()
    if not user_message:
        return JsonResponse({'response': "Chào bạn! Tôi có thể giúp gì cho bạn?"})

    try:
        # Lấy thông tin sản phẩm (chỉ lấy tối đa 15 sản phẩm để tiết kiệm token)
        products = Product.objects.filter(available=True).order_by('-created')[:15]
        categories = Category.objects.all()
        
        product_info = "\n".join([f"- {p.name}: {p.price} VNĐ" for p in products])
        category_info = ", ".join([c.name for c in categories])

        system_prompt = f"""
        Bạn là nhân viên tư vấn tại 'FlowerShop'.
        Sản phẩm nổi bật:
        {product_info}
        Danh mục: {category_info}
        Địa chỉ: 123 Đường Láng, Hà Nội. SĐT: +84 123 456 789.
        Ship: Nội thành HN trong 2h.
        Trả lời lịch sự, ngắn gọn bằng tiếng Việt.
        """

        reply = _ollama_chat(system_prompt, user_message)
        if reply:
            return JsonResponse({'response': reply})
        return JsonResponse({
            'response': (
                'Không kết nối được Ollama (Llama 3.2 cục bộ). '
                'Hãy cài Ollama, chạy `ollama pull llama3.2`, khởi động Ollama và thử lại. '
                'Mặc định API: http://127.0.0.1:11434 — có thể đổi OLLAMA_BASE_URL / OLLAMA_MODEL trong .env.'
            ),
        })

    except Exception:
        return JsonResponse({'response': 'Xin lỗi, chatbot đang gặp lỗi. Bạn có thể thử lại sau giây lát!'})

# Cart Views
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'Đã xóa {product.name} khỏi giỏ hàng.')
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart': cart})

# Order Views
@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Clear the cart
            cart.clear()
            messages.success(request, 'Đơn hàng của bạn đã được tạo thành công!')
            return render(request, 'shop/order/created.html', {'order': order})
    else:
        # Pre-fill form with profile data if available
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': request.user.profile.address,
        }
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'shop/order/create.html', {'cart': cart, 'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order/list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order/detail.html', {'order': order})

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:8] # Hiển thị 8 sản phẩm mới nhất
    return render(request, 'shop/home.html', {
        'categories': categories,
        'products': products
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Tài khoản {user.username} đã được tạo thành công!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Hồ sơ của bạn đã được cập nhật!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'shop/profile.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Sort functionality
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})

def abouuxuut(request):
    return render(request, 'shop/about.html')
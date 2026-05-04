from django import forms
from django.contrib.auth.models import User
from .models import Profile, Order

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Xác nhận mật khẩu")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'first_name': 'Họ',
            'last_name': 'Tên',
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Mật khẩu không khớp.")
        return confirm_password

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Họ',
            'last_name': 'Tên',
            'email': 'Email',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'avatar']
        labels = {
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ',
            'avatar': 'Ảnh đại diện',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024: # 2MB limit
                raise forms.ValidationError("Dung lượng ảnh không được vượt quá 2MB.")
            
            extension = avatar.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Định dạng ảnh không hợp lệ. Chỉ chấp nhận JPG, JPEG, PNG.")
        return avatar

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        labels = {
            'first_name': 'Họ',
            'last_name': 'Tên',
            'email': 'Email',
            'address': 'Địa chỉ',
            'postal_code': 'Mã bưu điện',
            'city': 'Thành phố',
        }

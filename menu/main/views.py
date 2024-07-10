from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template import loader, TemplateDoesNotExist
from .forms import CustomUserCreationForm, ProductForm, CustomUserLoginForm
from .models import Product, Purchase, PurchaseItem
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging


@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_all_purchases')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def add_admin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'add_admin.html', {'form': form})

@login_required
def view_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'view_purchases.html', {'purchases': purchases})

@csrf_exempt
@require_POST
@login_required
def save_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data.get('cart', [])
        user = request.user

        try:
            purchase = Purchase.objects.create(nombre=user.username, email=user.email)

            for item in cart:
                product = Product.objects.get(id=item['id'])
                quantity = item['quantity']
                PurchaseItem.objects.create(purchase=purchase, product=product, quantity=quantity)

            return JsonResponse({'success': True})

        except Exception as e:
            print(f"Error al guardar el carrito: {e}")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
@require_POST
def save_purchase(request):
    print("Vista save_purchase llamada")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            email = data.get('email')
            direccion = data.get('direccion', None)
            items_data = data.get('purchase_data')

            if not (nombre and email and items_data):
                return JsonResponse({'success': False, 'error': 'Datos incompletos'})

            purchase = Purchase(nombre=nombre, email=email, direccion=direccion, purchase_data=json.dumps(items_data))
            purchase.save()

            total_price = 0

            for item_data in items_data:
                product_id = item_data['id']
                quantity = item_data['quantity']
                product = Product.objects.get(id=int(product_id))
                PurchaseItem.objects.create(purchase=purchase, product=product, quantity=quantity)
                total_price += product.price * quantity

            purchase.total_price = total_price
            purchase.save()

            messages.success(request, '¡Compra realizada exitosamente!')
            return JsonResponse({'success': True})

        except ValueError as ve:
            print(f"Error de decodificación JSON: {ve}")
            return JsonResponse({'success': False, 'error': 'Error en los datos JSON'})

        except Product.DoesNotExist as pde:
            return JsonResponse({'success': False, 'error': 'Uno o más productos no existen'})

        except Exception as e:
            print(f"Error al guardar la compra: {e}")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)

@login_required
def view_all_purchases(request):
    purchases = Purchase.objects.all()
    products = Product.objects.all()
    if request.method == "POST":
        if "delete_product" in request.POST:
            product_id = request.POST.get("product_id")
            Product.objects.filter(id=product_id).delete()
            return redirect('view_all_purchases')
        else:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
    else:
        form = ProductForm()
    return render(request, 'view_all_purchases.html', {'purchases': purchases, 'products': products, 'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige al usuario dependiendo de si es staff o no
                if user.is_staff:
                    return redirect('view_all_purchases')
                else:
                    return redirect('home')
            else:
                # Autenticación fallida
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = CustomUserLoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')
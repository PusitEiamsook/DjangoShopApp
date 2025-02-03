from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Inventory, Cart, Address, Transaction, TransactionDetail

# Create your views here.

def indexView(request):
    return render(request, "shopapp/index.html")

def loginView(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('login')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('login')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('index')
    
    # Render the login page template (GET request)
    return render(request, 'shopapp/login.html')

def registerView(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken.")
            return redirect('register')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created successfully.")
        return redirect('register')
    
    # Render the registration page template (GET request)
    return render(request, 'shopapp/register.html')

def logoutView(request):
    logout(request)
    return redirect('index')

def productsView(request):
    products = Inventory.objects.all()
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        item = Inventory.objects.get(id=item_id)
        user_cart = Cart.objects.filter(user=request.user, item=item).first()
        
        if user_cart:
            new_quantity = user_cart.quantity + quantity
        else:
            new_quantity = quantity
        
        if new_quantity <= item.quantity:
            if user_cart:
                user_cart.quantity = new_quantity
                user_cart.save()
            else:
                Cart.objects.create(user=request.user, item=item, quantity=quantity)
            return render(request, 'shopapp/products.html', {'products': products, 'addtocartsuccessful': 'Added to cart successfully.'})
        else:
            return render(request, 'shopapp/products.html', {'products': products, 'error': 'Requested quantity exceeds available stock.'})
    
    return render(request, 'shopapp/products.html', {'products': products})

def productDetailView(request, product_id):
    product = get_object_or_404(Inventory, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        user_cart = Cart.objects.filter(user=request.user, item=product).first()
        
        if user_cart:
            new_quantity = user_cart.quantity + quantity
        else:
            new_quantity = quantity
        
        if new_quantity <= product.quantity:
            if user_cart:
                user_cart.quantity = new_quantity
                user_cart.save()
            else:
                Cart.objects.create(user=request.user, item=product, quantity=quantity)
            return redirect('productDetail', product_id=product.id)
        else:
            return render(request, 'shopapp/productDetail.html', {'product': product, 'error': 'Requested quantity exceeds available stock.'})
    
    return render(request, 'shopapp/productDetail.html', {'product': product})

@login_required(login_url="login")
def accountView(request):
    user = request.user

    if request.method == 'POST':
        if 'update_details' in request.POST:
            new_username = request.POST.get('username', user.username)
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return render(request, 'shopapp/account.html', {'user': user, 'error': 'Username already exists.'})
            else:
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.username = new_username
                user.email = request.POST.get('email', user.email)
                user.save()
                return redirect('account')

        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                return redirect('account')
            else:
                return render(request, 'shopapp/account.html', {'user': user, 'password_form': password_form})
            
        if 'add_address' in request.POST:
            address_text = request.POST.get('address')
            if address_text:
                Address.objects.create(user=user, address=address_text)
                return redirect('account')

        if 'remove_address' in request.POST:
            address_id = request.POST.get('address_id')
            address = get_object_or_404(Address, id=address_id)
            address.delete()
            return redirect('account')

    password_form = PasswordChangeForm(user)
    addresses = Address.objects.filter(user=user)
    return render(request, 'shopapp/account.html', {'user': user, 'password_form': password_form, 'addresses': addresses})

@login_required(login_url="login")
def cartView(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = get_object_or_404(Cart, id=cart_item_id)
        
        if 'update' in request.POST:
            new_quantity = int(request.POST.get('quantity'))
            inventory_item = cart_item.item

            if new_quantity <= inventory_item.quantity:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                return render(request, 'shopapp/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'error': 'Requested quantity exceeds available stock.'})

        if 'remove' in request.POST:
            cart_item.delete()
        
        return redirect('cart')
    
    return render(request, 'shopapp/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkoutView(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    addresses = Address.objects.filter(user=user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        shipping_address_id = request.POST.get('shippingAddress')
        proof_of_payment = request.FILES.get('proofOfPayment')

        if not shipping_address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('checkout')

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('checkout')

        shipping_address = Address.objects.get(id=shipping_address_id)

        # Create a transaction
        transaction = Transaction.objects.create(
            timestamp=timezone.now(),
            user=user,
            shippingAddress=shipping_address,
            proofOfPayment=proof_of_payment
        )

        # Move items from Cart to TransactionDetail
        for cart_item in cart_items:
            if cart_item.item.quantity < cart_item.quantity:
                messages.error(request, f"Not enough stock for {cart_item.item.productName}.")
                return redirect('checkout')

            TransactionDetail.objects.create(
                transaction=transaction,
                item=cart_item.item,
                quantity=cart_item.quantity
            )

            # Reduce inventory quantity
            cart_item.item.quantity -= cart_item.quantity
            cart_item.item.save()

        # Clear the cart
        cart_items.delete()

        return render(request, 'shopapp/cart.html', {'transactionsuccess': 'Transaction successful.'})

    return render(request, 'shopapp/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total_price': total_price})

def transactionHistoryView(request):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    transaction_details = []
    
    for transaction in user_transactions:
        details = TransactionDetail.objects.filter(transaction=transaction)
        total_price = sum(detail.item.price * detail.quantity for detail in details)
        transaction_details.append({
            'transaction': transaction,
            'details': details,
            'total_price': total_price
        })
    
    return render(request, 'shopapp/transactionHistory.html', {'transaction_details': transaction_details})

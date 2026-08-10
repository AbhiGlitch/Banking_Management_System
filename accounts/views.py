from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import BankAccount, Transaction
from .forms import RegisterForm, BankAccountForm, DepositForm, WithdrawForm, TransferForm 


@login_required
def dashboard(request):
    try:
         account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        return render(request, 'dashboard.html',{"error": "no bank account found for this user."})
    return render(request, "dashboard.html", {
        "account": account
    })
@login_required
def profile(request):
    account = BankAccount.objects.filter(user=request.user).first()
    return render(request, 'profile.html',{ 'user': request.user, 'account': account }) 
@login_required
def edit_profile(request):
    user = request.user
    account = BankAccount.objects.get(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        user.email = request.POST.get("email", "").strip()

        account.phone = request.POST.get("phone", "").strip()
        account.address = request.POST.get("address", "").strip()

        user.save()
        account.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "edit_profile.html", {
        "user": user,
        "account": account,
    })

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
        else:
            print(form.errors)   # Add this line
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})   
@login_required   
def create_account(request):
     if BankAccount.objects.filter(user=request.user).exists():
        return redirect('dashboard')
     if request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.account_number = random.randint(1000000000, 9999999999)
            account.save()
            return redirect('dashboard')
     else:
        form = BankAccountForm()
     return render(request, 'create_account.html', {'form': form})
@login_required
def deposit(request):
    account = BankAccount.objects.get(user=request.user)

    if request.method == "POST":
        form = DepositForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            Transaction.objects.create(
                account=account,
                transaction_type='deposit',
                amount=amount
            )

            return redirect('dashboard')
    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})
@login_required
def withdraw(request):
    account = BankAccount.objects.get(user=request.user)

    if request.method == "POST":
        form = WithdrawForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            if account.balance >= amount:
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type="withdraw",
                    amount=amount
                )

                messages.success(
                    request,
                    f"₹{amount} withdrawn successfully."
                )

                return redirect("dashboard")

            else:
                messages.error(request, "Insufficient Balance")
                return redirect("withdraw")

    else:
        form = WithdrawForm()

    return render(request, "withdraw.html", {"form": form})    

@login_required
def transfer(request):

    sender = BankAccount.objects.get(user=request.user)

    if request.method == "POST":

        form = TransferForm(request.POST)

        if form.is_valid():

            receiver_account_number = form.cleaned_data["receiver_account_number"]
            amount = form.cleaned_data["amount"]

            # Check sender and receiver are not the same
            if receiver_account_number == sender.account_number:
                messages.error(
                    request,
                    "You cannot transfer money to your own account."
                )
                return redirect("transfer")

            # Check receiver account exists
            try:
                receiver = BankAccount.objects.get(
                    account_number=receiver_account_number
                )
            except BankAccount.DoesNotExist:
                messages.error(
                    request,
                    "Receiver account does not exist."
                )
                return redirect("transfer")

            # Check sufficient balance
            if sender.balance < amount:
                messages.error(
                    request,
                    "Insufficient balance."
                )
                return redirect("transfer")

            # Transfer money
            with transaction.atomic():

                sender.balance -= amount
                sender.save()

                receiver.balance += amount
                receiver.save()

                # Sender transaction
                Transaction.objects.create(
                    account=sender,
                    transaction_type="transfer",
                    amount=amount
                )

                # Receiver transaction
                Transaction.objects.create(
                    account=receiver,
                    transaction_type="credit",
                    amount=amount
                )

            messages.success(
                request,
                f"₹{amount} transferred successfully."
            )

            return redirect("dashboard")

    else:
        form = TransferForm()

    return render(
        request,
        "transfer.html",
        {"form": form}
    )
@login_required
def transaction_history(request):
    account = BankAccount.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        account=account
    ).order_by('-created_at')

    return render(request, 'transaction_history.html', {
        'transactions': transactions
    })    
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. Please log in."
            )

            return redirect("login")
    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            print("LOGIN FAILED: Invalid username or password.")  # Debugging line 
    return render(request, "login.html")
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_account(request):
    if request.method == "POST":
        form = BankAccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()

            messages.success(
                request,
                "Bank account created successfully."
            )

            return redirect("dashboard")

    else:
        form = BankAccountForm()

    return render(
        request,
        "create_account.html",
        {"form": form}
    )
@login_required
def delete_account(request):
        if request.method == "POST":
            user = request.user
            user.delete()
            messages.success(
                request,
                " Your Bank account Permanently deleted successfully."
            )
            return redirect("home")

        return render(
            request,
            "delete_account.html",
        )
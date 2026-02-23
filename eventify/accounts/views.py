from django.shortcuts import redirect, render
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("dashboard")

            form.add_error(None, "Invalid username or password")

        return render(request, "accounts/login.html", {"form": form})

class RegisterView(View):
    """
        Handles user registration functionality.
        :GET -> Displays the registration form.
        :POST -> Creates a new user account.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "accounts/register.html", {"form": form})

class LogoutView(LoginRequiredMixin, View):
    """
        Handles user logout functionality.
        :GET -> Logs out the user and redirects to login page.
    """
    def get(self, request):
        logout(request)
        return redirect("login")
    
class ChangePasswordView(LoginRequiredMixin, View):
    """
    Handles password change functionality.
    :GET -> Displays the password change form.
    :POST -> Processes the password change request.
    """
    def get(self, request):
        """"
        Displays the password change form.
        """
        form = ChangePasswordForm()
        return render(request, "accounts/change_password.html", {"form": form})
    
    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect("dashboard")
        else:
            return render(request, "accounts/change_password.html", {"form": form})

class PasswordResetView(View):
    """
    Handles password reset functionality.
    :GET -> Displays the password reset form.
    :POST -> Processes the password reset request.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = PasswordResetForm()
        return render(request, "accounts/password_reset.html", {"form": form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            #:TODO
            #MAIL INTEGRATION
            return render(request, "accounts/password_reset_done.html")
        else:
            return render(request, "accounts/password_reset.html", {"form": form})
        
class MyProfileView(LoginRequiredMixin, View):
    """
    Displays the user's profile information.
    """
    def get(self, request):
        return render(request, "accounts/my_profile.html")
    
    # def post(self, request):
    #     action = request.POST.get("action")
    #     if action=="changeAccountType":
    #         request.user.role = "organizer"
    #         request.user.save()
    #         return redirect("my_profile")
    #     if action=="revertAccountType":
    #         request.user.role = "participant"
    #         request.user.save()
    #         return redirect("my_profile")
    #     else:
    #         return redirect("my_profile")
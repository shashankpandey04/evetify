from django.shortcuts import redirect, render
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from events.models import Event
from registrations.models import RegisterEvent

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
    def get(self, request):
        user = request.user
        context = {
            "registered_events": RegisterEvent.objects.filter(user=request.user),
            "organized_events": Event.objects.filter(organizer=user),
            "volunteer_events": Event.objects.filter(volunteers=user),
        }
        return render(request, "accounts/my_profile.html", context)

    def post(self, request):
        action = request.POST.get("action")
        user = request.user

        if action == "changeAccountType":
            new_role = request.POST.get("role")
            if user.role == "organizer" and Event.objects.filter(organizer=user).exists():
                return JsonResponse({
                    "message": "Cannot change account type while you are organizer of any event.",
                    "role": user.role
                }, status=403)
            valid_roles = ["organizer", "volunteer", "participant"]
            if new_role in valid_roles:
                user.role = new_role
                user.save()
                return JsonResponse({
                    "message": f"Account type changed to {new_role}",
                    "role": user.role
                })
            else:
                return JsonResponse({
                    "message": "Invalid action or role",
                    "role": user.role
                }, status=400)

        elif action == "editProfile":
            # Update editable fields
            fields = [
                "full_name", "username", "email", "phone_number",
                "cityName", "countryName", "gender", "organization", "bio"
            ]
            for field in fields:
                value = request.POST.get(field)
                if value is not None:
                    setattr(user, field, value)

            dob = request.POST.get("date_of_birth")
            if dob:
                try:
                    from datetime import datetime
                    user.date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()
                except Exception:
                    pass
            user.save()
            return JsonResponse({
                "message": "Profile updated successfully!"
            })

        else:
            return JsonResponse({
                "message": "Invalid action"
            }, status=400)
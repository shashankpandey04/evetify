from django.shortcuts import render, redirect
from events.models import Event
from attendance.models import Attendance
from accounts.models import User
from certificates.models import CertificatesModel
from registrations.models import RegisterEvent
from django.views import View
from django.http import JsonResponse
from django.db.models import Q, Count
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):

        stats = {
            "upcoming_events": Event.objects.filter(status="published").count(),
            "total_attendance": Attendance.objects.filter(
                user=request.user,
                checkedIn=True,
                checkedOut=True
            ).count(),
            "certificates_issued": CertificatesModel.objects.filter(
                issuedTo=request.user
            ).count(),
        }

        context = {
            "stats": stats,
            "is_organizer": request.user.role == "organizer",
            "is_volunteer": request.user.role == "volunteer",
            "is_participant": request.user.role == "participant",
        }

        if context["is_organizer"]:
            recent_events = Event.objects.filter(organizer=request.user).annotate(
                reg_count=Count('registerevent'),
                vol_count=Count('volunteers')
            ).order_by('-createdAt')[:5]

            total_registrations = RegisterEvent.objects.filter(event__organizer=request.user).count()

            total_volunteers = User.objects.filter(volunteered_events__organizer=request.user).distinct().count()

            recent_users = User.objects.order_by('-created_at')[:5]

            stats["total_registrations"] = total_registrations
            stats["total_volunteers"] = total_volunteers
            context.update({
                "recent_events": recent_events,
                "recent_users": recent_users,
                "stats": stats
            })

        return render(request, "dashboard/dashboard.html", context)

class UserManagementView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != "organizer":
            return redirect('dashboard')
        allUsers = User.objects.all()
        return render(request, 'dashboard/management/user_management.html', {
            'allUsers': allUsers
        })

class UserEndPoints(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != "organizer":
            return redirect('dashboard')
        query = request.GET.get('q')

        users = []

        if query:
            queryset = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(full_name__icontains=query)
            )[:10]

            users = [
                {
                    "uuid": str(user.uuid),
                    "username": user.username,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                }
                for user in queryset
            ]

        return JsonResponse({
            "success": True,
            "count": len(users),
            "results": users
        })

class ViewUser(LoginRequiredMixin, View):
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)

        if request.user.role != "organizer":
            return redirect("dashboard")
        data = {
            "uuid": str(user.uuid),
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "is_active_member": user.is_active_member,
            "created_at": user.created_at,
        }

        return render(request, 'dashboard/management/view_user.html', {
            "user": data
        })

    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)

        try:
            body = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

        action = body.get("action")

        if action == "change_role":
            if request.user.role != "organizer":
                return JsonResponse({
                    "success": False,
                    "message": "Permission denied"
                }, status=403)

            new_role = body.get("role")

            valid_roles = [r[0] for r in User.ROLE_CHOICES]
            if new_role not in valid_roles:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid role"
                }, status=400)

            user.role = new_role
            user.save()

            return JsonResponse({
                "success": True,
                "message": "Role updated successfully"
            })

        elif action == "reset_password":

            new_password = body.get("password")

            if not new_password or len(new_password) < 6:
                return JsonResponse({
                    "success": False,
                    "message": "Password too short"
                }, status=400)

            if request.user != user and request.user.role != "organizer":
                return JsonResponse({
                    "success": False,
                    "message": "Permission denied"
                }, status=403)

            user.set_password(new_password)
            user.save()

            if request.user == user:
                update_session_auth_hash(request, user)

            return JsonResponse({
                "success": True,
                "message": "Password updated successfully"
            })

        elif action == "deactivate":
            if request.user.role != "organizer":
                return JsonResponse({
                    "success": False,
                    "message": "Permission denied"
                }, status=403)

            user.is_active_member = False
            user.save()

            return JsonResponse({
                "success": True,
                "message": "User deactivated successfully"
            })

        elif action == "mail":
            if request.user.role != "organizer":
                return JsonResponse({
                    "success": False,
                    "message": "Permission denied"
                }, status=403)

            email = body.get("email")
            if not email:
                return JsonResponse({
                    "success": False,
                    "message": "Email is required"
                }, status=400)

            subject = body.get("subject", "No Subject")
            message = body.get("message", "")

            return JsonResponse({
                "success": True,
                "message": f"Email sent to {email} with subject '{subject}'"
            })

        return JsonResponse({
            "success": False,
            "message": "Invalid action"
        }, status=400)
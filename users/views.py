from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from users import forms as user_forms


# Create your views here.
class LoginView(View):
    form_class = user_forms.LoginForm
    template_name = "staff/users/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.account_status == "SUSPENDED":
                    errors = "Your account has been suspended."
                elif user.account_status == "DEACTIVATED":
                    errors = "Your account has been deactivated."
                else:
                    login(request, user)
                    return redirect("/web/admin/products")
            else:
                errors = "Invalid email or password"
        else:
            errors = form.errors
        context = {"errors": errors, "form": form}
        return render(request, self.template_name, context)

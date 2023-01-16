from datetime import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import render, redirect

from . import forms
from video import models as video_models


class StaffMixin(UserPassesTestMixin, View):
    def test_func(self):
        if self.request.user.is_anonymous:
            raise PermissionDenied
        return self.request.user.is_staff and self.request.user.account_status == "ACTIVE"


class DashboardView(StaffMixin):
    def get(self, request):
        return render(self.request, 'staff/dashboard.html')


class ListProductView(StaffMixin):
    page = "products"

    def get(self, request):
        return render(self.request, 'staff/products/index.html', {'page': self.page})


class ListSerialKeyView(StaffMixin):
    page = "keys"

    def get(self, request):
        return render(self.request, 'staff/serial_keys/index.html', {'page': self.page})


class RetrieveSerialKeyView(StaffMixin):
    page = "keys"
    form_class = forms.EditKeyForm

    validity_choices = dict([
        ('1', '1 day'),
        ('7', '7 days'),
        ('30', '1 month'),
        ('60', '2 months'),
        ('365', '1 year'),
        ('730', '2 years'),
        ('Unlimited', 'Unlimited')
    ])

    def get(self, request, pk):
        try:
            instance = video_models.KeyStorage.objects.get(key=pk)
        except video_models.KeyStorage.DoesNotExist:
            return redirect("/web/staff/serial-keys")

        validity = self.validity_choices.get(instance.validity)

        if instance.videos.exists():
            form = self.form_class(initial={'validity': instance.validity, 'watermark': instance.watermark,
                                            'videos': instance.videos.all(), 'status': instance.status})
        else:
            form = self.form_class(initial={'validity': instance.validity, 'watermark': instance.watermark,
                                            'status': instance.status})
        context = {'page': self.page, 'instance': instance, 'form': form, 'validity': validity}
        return render(self.request, 'staff/serial_keys/detail.html', context)


class GenerateSerialKeyView(StaffMixin):
    page = "keys"
    form_class = forms.GenerateKeyForm

    def get(self, request):
        context = {'form': self.form_class, 'page': self.page}
        return render(self.request, 'staff/serial_keys/generate_keys.html', context)


class RetrieveProductView(StaffMixin):
    page = "products"

    def get(self, request, pk):
        try:
            instance = video_models.Product.objects.get(id=pk)
        except video_models.Product.DoesNotExist:
            # return render(self.request, 'staff/404.html')
            return redirect('/web/admin/products')

        return render(self.request, 'staff/products/detail.html', {'page': self.page, 'product': instance})


class ListProductSerialKeyView(StaffMixin):
    page = "keys"

    def get(self, request, pk):
        try:
            instance = video_models.Product.objects.get(id=pk)
        except video_models.Product.DoesNotExist:
            # return render(self.request, 'staff/404.html')
            return redirect('/web/admin/products')

        return render(self.request, 'staff/products/list_keys.html', {'page': self.page, 'product': instance})


class CreateProductView(StaffMixin):
    page = "products"
    form_class = forms.CreateProductForm

    def get(self, request):
        context = {'form': self.form_class, 'page': self.page}
        return render(self.request, 'staff/products/create.html', context)

from django.views import View
from django.shortcuts import render, redirect
from . import forms
from video import models as video_models


class DashboardView(View):
    def get(self, request):
        return render(self.request, 'staff/dashboard.html')


class ListProductView(View):
    page = "products"

    def get(self, request):
        return render(self.request, 'staff/products/index.html', {'page': self.page})


class ListSerialKeyView(View):
    page = "keys"

    def get(self, request):
        return render(self.request, 'staff/serial_keys/index.html', {'page': self.page})


class GenerateSerialKeyView(View):
    page = "keys"
    form_class = forms.GenerateKeyForm

    def get(self, request):
        context = {'form': self.form_class, 'page': self.page}
        return render(self.request, 'staff/serial_keys/generate_keys.html', context)


class RetrieveProductView(View):
    page = "products"

    def get(self, request, pk):
        try:
            instance = video_models.Product.objects.get(id=pk)
        except video_models.Product.DoesNotExist:
            # return render(self.request, 'staff/404.html')
            return redirect('staff:products')

        return render(self.request, 'staff/products/detail.html', {'page': self.page, 'product': instance})


class CreateProductView(View):
    page = "products"
    form_class = forms.CreateProductForm

    def get(self, request):
        context = {'form': self.form_class, 'page': self.page}
        return render(self.request, 'staff/products/create.html', context)

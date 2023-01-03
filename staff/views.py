from django.views import View
from django.shortcuts import render


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

    def get(self, request):
        return render(self.request, 'staff/serial_keys/generate_keys.html', {'page': self.page})

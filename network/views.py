from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import viewsets, permissions, filters

from .forms import NetworkNodeForm, ProductForm
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer


class IsActiveStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active and request.user.is_staff


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']


class NetworkNodeListView(ListView):
    model = NetworkNode
    template_name = 'network/list.html'
    context_object_name = 'nodes'


class NetworkNodeDetailView(DetailView):
    model = NetworkNode
    template_name = 'network/detail.html'
    context_object_name = 'node'


class NetworkNodeCreateView(CreateView):
    model = NetworkNode
    form_class = NetworkNodeForm
    template_name = 'network/create.html'
    success_url = reverse_lazy('network:list')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'network/product_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.node = get_object_or_404(NetworkNode, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.node = self.node
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('network:detail', args=[self.node.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node'] = self.node
        return context

from django.shortcuts import render, get_object_or_404
from .models import Reference
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import (SearchVector, 
                                            SearchQuery, 
                                            SearchRank)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.text import slugify

class ReferenceListView(LoginRequiredMixin, ListView):
    queryset = Reference.published.all().order_by('-created')
    context_object_name = 'references'
    paginate_by = 2
    template_name = 'reference/page/list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            qs = qs.filter(tags__in=[tag])
            self.tag = tag
        else:
            self.tag = None
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.tag:
            context['tag'] = self.tag

        return context

# class ReferenceDetailView(LoginRequiredMixin, FormView):
#     form_class = FormView
#     template_name = 'reference/page/detail.html'

#     def get_initial(self):
#         pk = self.kwargs.get('pk')
#         slug = self.kwargs.get('slug')
#         self.reference = get_object_or_404(Reference, pk=pk, slug=slug)
#         return super().get_initial()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reference'] = self.reference
#         return context


class ReferenceCreateView(LoginRequiredMixin, CreateView):
    model = Reference
    fields = ['title', 'link', 'description']
    template_name = 'reference/page/reference_form.html'
    success_url = reverse_lazy('reference:reference_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'published'
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)

        return super().form_valid(form)

class ReferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Reference
    fields = ['title', 'link', 'description']
    template_name = 'reference/page/reference_form.html'
    success_url = reverse_lazy('reference:reference_list')
    query_pk_and_slug = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author = self.request.user)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

class ReferenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Reference
    template_name = 'reference/page/reference_confirm_delete.html'
    success_url = reverse_lazy('reference:reference_list')
    query_pk_and_slug = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author = self.request.user)
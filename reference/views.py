from django.shortcuts import render, get_object_or_404
from .models import Post
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

class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.published.all().order_by('-created')
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'reference/post/list.html'
    
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

class PostDetailView(LoginRequiredMixin, FormView):
    form_class = FormView
    template_name = 'reference/post/detail.html'

    def get_initial(self):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        self.post = get_object_or_404(Post, pk=pk, slug=slug)
        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'link', 'description']
    template_name = 'reference/post/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'published'
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)

        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'link', 'description']
    template_name = 'reference/post/post_form.html'
    query_pk_and_slug = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author = self.request.user)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'reference/post/post_confirm_delete.html'
    success_url = reverse_lazy('reference:post_list')
    query_pk_and_slug = True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author = self.request.user)
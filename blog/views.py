from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostEntry, EditEntry, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('blogpost', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_date']
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        meny = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["meny"] = meny
        return context


class PostView(DetailView):
    model = Post
    template_name = 'blogpost.html'

    def get_context_data(self, *args, **kwargs):
        meny = Category.objects.all()
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        likepage = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = likepage.total_likes()

        liked = False
        if likepage.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["meny"] = meny
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class Add_BlogEntry(CreateView):
    model = Post
    form_class = PostEntry
    template_name = 'add-blogentry.html'


class Add_Comment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add-comment.html'
    
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('home')


class Add_Category(CreateView):
    model = Category
    template_name = 'add-category.html'
    fields = '__all__'


class Edit_BlogEntry(UpdateView):
    model= Post
    form_class = EditEntry
    template_name = 'edit-blogentry.html'


class Delete_Entry(DeleteView):
    model = Post
    template_name = 'delete-entry.html'
    success_url = reverse_lazy('home')


def View_By_Category(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})

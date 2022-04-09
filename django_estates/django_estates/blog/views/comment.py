from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from django_estates.blog.forms import CommentForm, DeleteCommentForm
from django_estates.blog.models import Post, Comment


class PostCommentView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.View):
    permission_required = 'blog.add_comment'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = Post.objects.get(slug=self.kwargs['slug'])
        comment = Comment(
            text=form.cleaned_data['text'],
            post=post,
            user=self.request.user,
        )
        comment.save()

        return redirect('post detail', post.slug)

    def form_invalid(self, form):
        pass


class PostCommentDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Comment
    form_class = DeleteCommentForm
    template_name = 'blog/delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('post detail', kwargs={'slug': self.object.post.slug})

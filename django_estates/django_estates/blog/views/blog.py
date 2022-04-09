from django.views import generic as views

from django_estates.blog.forms import CommentForm
from django_estates.blog.models import Post


class PostsGridView(views.ListView):
    paginate_by = 3
    model = Post
    template_name = 'blog/posts_grid.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')


class PostDetailView(views.DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        comments_count = len(post.comment_set.all())

        context['comment_form'] = CommentForm(
            initial={'post_slug': self.object.slug, }
        )
        context['comments'] = post.comment_set.all()
        context.update({
            'comments_count': comments_count,
        })

        return context

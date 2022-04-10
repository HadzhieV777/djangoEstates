from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Category(models.Model):
    TITLE_MAX_LEN = 70
    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Post(models.Model):
    POST_TITLE_MAX_LEN = 200
    SLUG_MAX_LEN = 200

    # Status types
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

    title = models.CharField(
        max_length=POST_TITLE_MAX_LEN,
        unique=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='categories',
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LEN,
        unique=True,
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    image = models.URLField()
    updated_on = models.DateField(
        auto_now=True,
    )
    content = models.TextField()
    created_on = models.DateField(
        auto_now_add=True,
    )
    status = models.IntegerField(
        choices=STATUS,
        default=0,
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    published = models.DateTimeField(auto_now_add=True,)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

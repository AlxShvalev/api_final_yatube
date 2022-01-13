from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        'Текст сообщения'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(verbose_name='Название', max_length=250)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        author = self.author.get_full_name()
        text = self.text[:15]
        return f'{author}: "{text}..."'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        user = self.user.get_full_name()
        author = self.following.get_full_name()
        return f'{user} подписан на {author}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follows',
            ),
            models.CheckConstraint(
                check=~models.Q(following=models.F('user')),
                name='follower_and_author_can_not_be_equal',
            ),
        ]

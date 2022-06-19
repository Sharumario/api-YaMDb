from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    AutoField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    TextField,
    UniqueConstraint
)

from users.models import User


class CreatedModel(Model):
    """Абстрактная модель. Добавляет дату создания."""
    pub_date = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Указывается автоматически при создании'
    )

    class Meta:
        abstract = True


class Title(Model):
    """Модель для произведений."""
    pass


class Review(CreatedModel):
    """Модель для отзывов на произведения."""
    id = AutoField(primary_key=True)
    text = TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва')
    score = PositiveSmallIntegerField(
        validators=(MaxValueValidator(10), MinValueValidator(1)),
        verbose_name='Рейтинг',
        help_text='Укажите рейтинг произведения'
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Выберите автора отзыва'
    )
    title = ForeignKey(
        Title,
        on_delete=CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Выберите произведение на которое будете писать отзыв'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    """Модель для комментариев на отзывы."""
    id = AutoField(primary_key=True)
    text = TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Выберите автора комментария'
    )
    review = ForeignKey(
        Review,
        on_delete=CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Выберите отзыв на который будете писать комментарий'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]

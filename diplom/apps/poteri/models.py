from django.db import models

class Statia(models.Model):
    statia_title = models.CharField('Название статьи', max_length = 250)
    html_texst = models.TextField('Код')
    pub_date = models.DateTimeField('Дата публикации')
    model_img = models.ImageField(upload_to='static/img')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Comment(models.Model):
    name_stati = models.ForeignKey(Statia, on_delete = models.CASCADE)
    name = models.CharField('Автор', max_length = 50)
    comment_text = models.TextField('Текст коментариия', max_length = 5000)

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
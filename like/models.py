from django.db import models


class Users(models.Model):
    login = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=25)

    def __str__(self):
        return self.login

    @classmethod
    def vote(cls, uid, variety, material_id, value):
        try:
            vote = Ratings.objects.filter(variety=variety, uid=uid, material_id=material_id).exists()
            if vote:
                vote = Ratings.objects.get(variety=variety, uid=uid, material_id=material_id)
                vote.value = value
                vote.save()
                return vote.pk, ' value was changed'
            user = Users.objects.get(pk=uid)
            new_vote = Ratings(uid=user, variety=variety, material_id=material_id, value=value)
            new_vote.save()
            return new_vote.pk
        except Exception as err:
            return err

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"


class MaterialTypes(models.Model):
    type_of_material = models.CharField(max_length=50)

    def __str__(self):
        return self.type_of_material


class Posts(models.Model):
    uid = models.ForeignKey(Users, null=True, on_delete=models.PROTECT)
    material = models.ForeignKey(MaterialTypes, null=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(max_length=350)
    published = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_ratings(cls, pid):
        ratings = Ratings.objects.filter(variety="Материал", material_id=pid)
        minus, plus, votes = 0, 0, 0
        for rating in ratings:
            if rating.value == 1:
                plus += 1
            else:
                minus += 1
            votes += 1
        return plus, minus, votes

    class Meta:
        verbose_name_plural = "Материалы"
        verbose_name = "Материал"
        ordering = ['-published']


class Comments(models.Model):
    pid = models.ForeignKey(Posts, null=True, on_delete=models.PROTECT)
    uid = models.ForeignKey(Users, null=True, on_delete=models.PROTECT)
    comment = models.TextField(max_length=255)
    published = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def create_comment(cls, pid, uid, comment):
        post = Posts.objects.get(pk=pid)
        user = Users.objects.get(pk=uid)
        comment = Comments(pid=post, uid=user, comment=comment)
        comment.save()
        return comment.pk


class Ratings(models.Model):
    uid = models.ForeignKey(Users, null=True, on_delete=models.PROTECT)
    variety = models.CharField(max_length=25, null=True)
    material_id = models.IntegerField(default=0)
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name_plural = "Голоса"
        verbose_name = "Голос"

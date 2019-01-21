from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=140)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Message(models.Model):
    nomor = models.CharField(max_length=255)
    name = models.CharField(max_length=140)
    dep = models.CharField(max_length=100, verbose_name="Department")
    div = models.CharField(max_length=100, verbose_name="Division")
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nomor
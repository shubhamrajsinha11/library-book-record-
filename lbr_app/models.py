from django.db import models

class student(models.Model):

    def __str__(self):
        return self.student_name
    student_id=models.CharField(max_length=200)
    student_name=models.CharField(max_length=200)
    student_contact=models.CharField(max_length=200)
    student_address=models.TextField()
    active=models.BooleanField(default=True)
    student_ref_id=models.CharField(max_length=10, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.student_ref_id:
            count = student.objects.count() + 1
            self.student_ref_id = f"{count:04d}"  # like 0001, 0002
        super().save(*args, **kwargs)


class books(models.Model):

    def __str__(self):
        return self.book_name

    book_name=models.CharField(max_length=200)
    book_author=models.CharField(max_length=200)
    book_publisher=models.CharField(max_length=200)
    book_isbn=models.CharField(max_length=50,unique=True)
    book_year=models.PositiveIntegerField()
    book_thumbnail=models.ImageField(upload_to='book_thumbnails/',null=True, blank=True)
    available=models.BooleanField(default=True)



class Rental(models.Model):
    student_ref_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    student_contact = models.CharField(max_length=15)
    student_id = models.CharField(max_length=50)
    book_name = models.CharField(max_length=255)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField()

    def __str__(self):
        return f"{self.student_name} - {self.book_name}"

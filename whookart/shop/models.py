from itertools import product
import sys
from django.db import models
from django.contrib.auth.models import User
import datetime
import os
from PIL import Image,ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
 
def getFileName(request,filename):
  now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
  new_filename="%s%s"%(now_time,filename)
  return os.path.join('uploads/',new_filename)

def resize_and_crop(image, size):
    img = Image.open(image)
    img.thumbnail(size)

    # Creating a new blank image with the desired size
    new_img = Image.new("RGB", size, "white")

    # Calculating the positioning to center the image
    position = ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)

    # Pasting the image onto the new blank image
    new_img.paste(img, position)

    output = BytesIO()
    new_img.save(output, format='JPEG', quality=75)
    output.seek(0)

    return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0],
                                'image/jpeg', sys.getsizeof(output), None)

class Catagory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = resize_and_crop(self.image, (410, 275))
        super(Catagory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
 
class Product(models.Model):
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.product_image:
            self.product_image = resize_and_crop(self.product_image, (410, 275))
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
 

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)
 
  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price
 
class Favourite(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    delivery_mode = models.CharField(max_length=50)  # You may customize this field based on your needs
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_price = models.FloatField()
    total_price = models.FloatField()

class OrderWithProducts(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    delivery_mode = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    item_price = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        managed = False  # Tells Django this model is not managed by Django
        db_table = 'OrderWithProducts'  # Use the name of your denormalized view in the database
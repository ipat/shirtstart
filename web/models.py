from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class UserProfile (models.Model):
	user = models.OneToOneField(User)
	GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	# name_first = models.CharField(max_length=50)
	# name_last = models.CharField(max_length=50)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	# email = models.EmailField(max_length=100)
	# password = models.CharField(max_length=50)
	birthdate = models.DateField(auto_now=False)
	is_designer = models.BooleanField(default=False)
	address_house_no = models.CharField(max_length=10)
	address_building = models.CharField(max_length=50)
	address_road = models.CharField(max_length=50)
	address_subdistrict = models.CharField(max_length=50)
	address_district = models.CharField(max_length=50)
	address_province = models.CharField(max_length=50)
	address_country = models.CharField(max_length=20)
	address_postcode = models.CharField(max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username

class Waiting (models.Model):
	# shirt_id = models.OneToOneField(Shirt)
	require_amount = models.IntegerField()
	require_date = models.DateField()

class Shirt (models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	file_url = models.FileField()
	shirt_color = models.IntegerField()
	owner_id = models.ForeignKey(User)
	is_on_shelf = models.BooleanField()
	color_num = models.IntegerField()
	created_at = models.DateTimeField()
	waiting_id = models.ForeignKey(Waiting)

class Comment (models.Model):
	user_id = models.ForeignKey(User)
	shirt_id = models.ForeignKey(Shirt)
	comment = models.TextField()
	time = models.DateTimeField()

class Like (models.Model):
	user_id = models.ForeignKey(User)
	shirt_id = models.ForeignKey(Shirt)
	time = models.DateTimeField()

	class Meta:
		unique_together = (("user_id", "shirt_id"),)

class Join (models.Model):
	user_id = models.ForeignKey(User)
	shirt_id = models.ForeignKey(Shirt)
	shirt_size = models.CharField(max_length=5)
	amount = models.IntegerField()
	time = models.DateTimeField()
	address_house_no = models.CharField(max_length=10)
	address_building = models.CharField(max_length=50)
	address_road = models.CharField(max_length=50)
	address_subdistrict = models.CharField(max_length=50)
	address_district = models.CharField(max_length=50)
	address_province = models.CharField(max_length=50)
	address_country = models.CharField(max_length=20)
	address_postcode = models.CharField(max_length=10)

	class Meta:
		unique_together = (("user_id", "shirt_id", "shirt_size", "time"),)

class Shirt_in_cart (models.Model):
	user_id = models.ForeignKey(User)
	shirt_id = models.ForeignKey(Shirt)
	shirt_size = models.CharField(max_length=5)
	amount = models.IntegerField()
	time = models.DateTimeField()

	class Meta:
		unique_together = (("user_id", "shirt_id", "shirt_size"),)

class Credit_card (models.Model):
	user_id = models.OneToOneField(User)
	name_on_card = models.CharField(max_length=100)
	number = models.CharField(max_length=30)
	expiry_year = models.CharField(max_length=5)
	expiry_month = models.CharField(max_length=5)

class Designer (models.Model):
	user_id = models.OneToOneField(User)
	wallet = models.DecimalField(max_digits=10, decimal_places=2)
	bank_account_name = models.CharField(max_length=100)
	bank_account_number = models.CharField(max_length=30)

class Transaction (models.Model):
	user_id = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	time = models.DateTimeField()
	to_account_bank = models.CharField(max_length=30)
	to_account_number = models.CharField(max_length=30)
	to_account_name = models.CharField(max_length=100)

class Order (models.Model):
	user_id = models.ForeignKey(User)
	time = models.DateTimeField()
	ship_date = models.DateField()
	ship_tracking_no = models.CharField(max_length=20)
	status = models.IntegerField()
	address_house_no = models.CharField(max_length=10)
	address_building = models.CharField(max_length=50)
	address_road = models.CharField(max_length=50)
	address_subdistrict = models.CharField(max_length=50)
	address_district = models.CharField(max_length=50)
	address_province = models.CharField(max_length=50)
	address_country = models.CharField(max_length=20)
	address_postcode = models.CharField(max_length=10)

class Order_list (models.Model):
	order_id = models.ForeignKey(Order)
	shirt_id = models.ForeignKey(Shirt)
	shirt_size = models.CharField(max_length=5)
	amount = models.IntegerField()
	price_each = models.DecimalField(max_digits=5, decimal_places=2)







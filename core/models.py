from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from djmoney.money import maybe_convert

CATEGORY_CHOICES = (
    ('N', 'Non-sweet'),
    ('SA', 'Sub-acid'),
    ('S', 'Sweet'),
    ('A', 'Acid')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

TRANSPORT_CHOICES = (
    ('R', 'Regular'),
    ('F', 'Fast'),
    ('VF', 'Very Fast'),
)

SELLER_CHOICES = (
    ('N', 'Normal'),
    ('P', 'Premium')
)

DELIVERY_CHOICES = (
    ('R', 'Received'),
    ('O', 'On Process'),
    ('S', 'Shipping'),
    ('D', 'Delevered')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    # price = models.FloatField()
    # discount_price = models.FloatField(blank=True, null=True)
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, blank=True, null=True)
    price = MoneyField(max_digits=14, decimal_places=0, default_currency="IDR")
    discount_price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="IDR")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    print("OrderItem")
    items = models.ManyToManyField(OrderItem)
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_service = models.CharField(max_length=1, choices=TRANSPORT_CHOICES, blank=True, null=True)
    shipping_provider = models.ForeignKey('Transport', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    satus = models.CharField(max_length=20, blank=True)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.user.username
        except Exception:
            return str(self.seller)

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

class BlitzPay(models.Model):
    user = models.ForeignKey(UserProfile,
                             on_delete=models.CASCADE)
    saldo = MoneyField(max_digits=14, decimal_places=0, default_currency="IDR")

    def __str__(self):
        return self.user.user.username

class Seller(models.Model):
    seller = models.CharField(max_length=64)
    rating = models.CharField(max_length=1, choices=SELLER_CHOICES)

    def __str__(self):
        return self.seller

class Transport(models.Model):
    transport = models.CharField(max_length=64)

    def __str__(self):
        return self.transport

class Delivery(models.Model):
    transport = models.ForeignKey('Transport', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True)
    delivery_address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=1, choices=DELIVERY_CHOICES)

    def __str__(self):
        return self.status
    
    def get_seller_address(self):
        return Address.objects.get(seller=self.seller)



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
        print(userprofile.user.id)
        print(UserProfile.objects.get(id=userprofile.user.id))

        blitzPay = BlitzPay(user=UserProfile.objects.get(id=userprofile.user.id), saldo =100000)
        blitzPay.save()
        print("Creating new user")


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

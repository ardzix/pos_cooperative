from __future__ import unicode_literals

from django.db import models
from libs.constants import PRODUCT_CATEGORIES, GENDER_CHOICES, INVESTOR_TYPE_CHOICES, DISCOUNT_TYPES, SALE_STATUSES, INVENTORY_METHOD
from libs.models import BaseModelGeneric, BaseModelUnique
from libs.views import ProtectedMixin
from libs.storages import generate_name, STORAGE_BACKGROUND_COVER, STORAGE_AVATAR
from django.contrib.auth.models import User
from django.utils import timezone
from libs.moment import to_timestamp
from datetime import datetime

# Create your models here.
class Role(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class Profile(BaseModelUnique):
    roles = models.ManyToManyField(Role)
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, default=3)
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=25)
    background_cover = models.ImageField(
        upload_to = generate_name,
        storage = STORAGE_BACKGROUND_COVER,
        blank = True,
        null = True
    )
    avatar = models.ImageField(
        upload_to = generate_name,
        storage = STORAGE_AVATAR,
        blank = True,
        null = True
    )
    is_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.created_by.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Investor(BaseModelUnique):
    investor_type = models.PositiveIntegerField(choices=INVESTOR_TYPE_CHOICES, default=1)

    def __unicode__(self):
        profile = self.get_profile()
        if profile:
            return "%s - %s %s" % (profile.phone, self.created_by.first_name, self.created_by.last_name)
        else:
            return "%s %s" % (self.created_by.first_name, self.created_by.last_name)
    
    def get_profile(self):
        return Profile.objects.filter(created_by=self.created_by).first()
            

    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investors"


class Brand(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Product(BaseModelGeneric):
    category = models.PositiveIntegerField(choices=PRODUCT_CATEGORIES, default=1)
    brand = models.ForeignKey(Brand, related_name="%(app_label)s_%(class)s_brand")
    sku = models.CharField(max_length=100)
    display_name = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)
    base_price = models.DecimalField(max_digits=20, decimal_places=0)
    capital = models.DecimalField(max_digits=20, decimal_places=0)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    method = models.PositiveIntegerField(choices=INVENTORY_METHOD, default=1)    

    def __unicode__(self):
        return "[%s][%s] %s" % (self.sku, self.brand, self.display_name)

    def get_discount(self):
        if self.applied_discount():
            return str(self.applied_discount().reduction) + " %"
        else:
            return "-"

    def get_discounted_price(self):
        if self.applied_discount():
            return float(self.base_price) - (self.applied_discount().reduction * 0.01 * float(self.base_price))
        else:
            return "-"

    def get_discounted_price_int(self):
        if self.applied_discount():
            return float(self.base_price) - (self.applied_discount().reduction * 0.01 * float(self.base_price))
        else:
            return float(self.base_price)

    def applied_discount(self):
        d = DiscountProduct.objects.filter(product=self, discount__deleted_at__isnull = True, discount__start_date_at__lte=datetime.now(), discount__end_date_at__gte=datetime.now()).last()
        if d:
            return d.discount
        else:
            return None
    
    def sale(self, qty):
        if self.method == 1:
            stocks = Stock.objects.filter(product=self, latest_stock__gt=0, deleted_at__isnull = True).order_by("created_at").all()
        else:
            stocks = Stock.objects.filter(product=self, latest_stock__gt=0, deleted_at__isnull = True).order_by("-created_at").all()

        for s in stocks:
            if qty <= s.latest_stock:
                s.latest_stock -= qty
                s.save()
                break
            else:
                qty -= s.latest_stock
                s.latest_stock = 0
                s.save()
        

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Stock(BaseModelGeneric):
    product = models.ForeignKey(Product, related_name="%(app_label)s_%(class)s_product")
    first_stock = models.PositiveIntegerField(default=0)
    latest_stock = models.PositiveIntegerField(default=0)
    last_opnamed_at = models.DateTimeField(blank=True, null=True)
    last_opnamed_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    last_opnamed_by = models.ForeignKey(User, db_index=True, blank=True, null=True, related_name="%(app_label)s_%(class)s_opnamed_by")

    def __unicode__(self):
        return self.product.display_name

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class Discount(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    discount_type = models.PositiveIntegerField(choices=DISCOUNT_TYPES, default=1)
    start_date_at = models.DateTimeField(blank=True, null=True)
    start_date_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    end_date_at = models.DateTimeField(blank=True, null=True)
    end_date_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reduction = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s%% (%s)" % (self.reduction,self.display_name)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

class DiscountProduct(BaseModelGeneric):
    discount = models.ForeignKey(Discount, related_name="%(app_label)s_%(class)s_discount")
    product = models.ForeignKey(Product, related_name="%(app_label)s_%(class)s_product")

    class Meta:
        verbose_name = "Discount Product"
        verbose_name_plural = "Discount Products"


class Checkout(BaseModelGeneric):
    price = models.PositiveIntegerField(default=0)
    paid = models.PositiveIntegerField(default=0)
    sale_at = models.DateTimeField()
    sale_at_timestamp = models.PositiveIntegerField(db_index=True)
    sale_by = models.ForeignKey(User, db_index=True, related_name="%(app_label)s_%(class)s_sale_by")
    closed_at = models.DateTimeField(blank=True, null=True)
    closed_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    closed_by = models.ForeignKey(User, db_index=True, blank=True, null=True, related_name="%(app_label)s_%(class)s_close_by")

    # Please not that created_by is filled with buyer info, and sale_by si filled by sales/admin

    def save(self, *args, **kwargs):
        now = timezone.now()

        if self.sale_at is None:
            self.sale_at = now
            self.sale_at_timestamp = to_timestamp(self.sale_at)

        instance = super(Checkout, self).save(*args, **kwargs)
        return instance

    class Meta:
        verbose_name = "Checkout"
        verbose_name_plural = "Checkouts"


class Sale(BaseModelGeneric):
    checkout = models.ForeignKey(Checkout, related_name="%(app_label)s_%(class)s_checkout", blank=True, null=True)
    product = models.ForeignKey(Product, related_name="%(app_label)s_%(class)s_product")
    discount = models.ForeignKey(Discount, related_name="%(app_label)s_%(class)s_discount", blank=True, null=True)
    amount = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    discounted_price = models.PositiveIntegerField(default=0)
    status = models.PositiveIntegerField(choices=SALE_STATUSES, default=1)
    sale_at = models.DateTimeField()
    sale_at_timestamp = models.PositiveIntegerField(db_index=True)
    sale_by = models.ForeignKey(User, db_index=True, related_name="%(app_label)s_%(class)s_sale_by")
    closed_at = models.DateTimeField(blank=True, null=True)
    closed_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    closed_by = models.ForeignKey(User, db_index=True, blank=True, null=True, related_name="%(app_label)s_%(class)s_close_by")

    # Please not that created_by is filled with buyer info, and sale_by si filled by sales/admin

    def save(self, *args, **kwargs):
        now = timezone.now()

        if self.sale_at is None:
            self.sale_at = now
            self.sale_at_timestamp = to_timestamp(self.sale_at)

        if self.discount:
            self.discounted_price = self.price - ((self.price * self.discount.reduction) / 100)
        else:
            self.discounted_price = self.price

        return super(Sale, self).save(*args, **kwargs)

    def sold(self, staff, buyer):
        amount = 0
        if buyer.id > 0 and self.product.category == 1:
            amount = self.qty * self.discounted_price * 0.05
            cb = CashBack(sale=self, investor=buyer, amount=amount)
            cb.created_by = staff
            cb.save()
        return amount

    def get_final_price(self):
        return self.product.get_discounted_price_int()

    def get_final_amount(self):
        if self.discount:
            return self.amount - self.product.get_discounted_price_int()
        else:
            return self.amount

    def get_discount_name(self):
        if self.discount:
            return self.discount.__unicode__()
        else:
            return "-"
    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

class CashBack(BaseModelGeneric):
    sale = models.ForeignKey(Sale, related_name="%(app_label)s_%(class)s_sale")
    investor = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_investor")
    amount = models.PositiveIntegerField(default=0)
    closed_at = models.DateTimeField(blank=True, null=True)
    closed_at_timestamp = models.PositiveIntegerField(db_index=True, blank=True, null=True)
    closed_by = models.ForeignKey(User, db_index=True, blank=True, null=True, related_name="%(app_label)s_%(class)s_close_by")
    
    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.closed_by:
            if not self.closed_at:
                self.closed_at = now
                self.closed_at_timestamp = to_timestamp(self.closed_at)

        return super(CashBack, self).save(*args, **kwargs)

    def get_product_name(self):
        return "%s (x%s)" % (self.sale.product.display_name, self.sale.qty)

    class Meta:
        verbose_name = "Cashback"
        verbose_name_plural = "Cashbacks"
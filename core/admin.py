from django.contrib import admin
from django.contrib import messages

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, Seller,Transport, BlitzPay


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

def update_delivery(modeladmin, request, queryset):
    if(queryset.get().ordered == True):
        queryset.update(being_delivered=True)
    else:
        messages.error(request, "Item Not Ordered Yet.")

def finish_delivery(modeladmin, request, queryset):
    queryset.update(received=True)

make_refund_accepted.short_description = 'Update orders to refund granted'
update_delivery.short_description = 'Update being delivered'
finish_delivery.short_description = 'Update delivery finished'

OrderAdminGroup = "TransportAdmin"
class OrderAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        admin.site.index_title = "Welcome, "+request.user.username
        if(request.user.groups.filter(name=OrderAdminGroup).exists()):
            admin.site.site_header="Transport Company"
            return True
        elif(request.user.is_superuser) :
            admin.site.site_header="Administrator"

            return True
        else :
            False

    def has_add_permission(self, request):
        if(request.user.is_superuser) :
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if(request.user.is_superuser) :
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if(request.user.is_superuser) :
            return True
        return False
    
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    'billing_address',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',]
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [update_delivery, finish_delivery]

ShopAdminGroup = "ShopAdmin"
class ShopAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        admin.site.index_title = "Welcome, "+request.user.username

        if(request.user.groups.filter(name=ShopAdminGroup).exists()):
            admin.site.site_header = "Shop Company"
            return True
        elif(request.user.is_superuser) :
            admin.site.site_header="Administrator"
            return True
        else :
            return False

    def has_add_permission(self, request):
        if(request.user.is_superuser) :
            return True
        return request.user.groups.filter(name=ShopAdminGroup).exists()

    def has_change_permission(self, request, obj=None):
        if(request.user.is_superuser) :
            return True
        return request.user.groups.filter(name=ShopAdminGroup).exists()

    def has_delete_permission(self, request, obj=None):
        if(request.user.is_superuser) :
            return True
        return request.user.groups.filter(name=ShopAdminGroup).exists()
    
    list_display = ['title', 'price', 'discount_price', 'category', 'label', 'slug', 'description', 'image']
    list_display_links = [
        'title', 'price', 'discount_price', 'category',
    ]
    list_filter = ['price',
                   'discount_price',
                   'title',]
    # search_fields = [
    #     'user__username',
    #     'ref_code'
    # ]
    # actions = [make_refund_accepted, update_delivery, finish_delivery]
    

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Item, ShopAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Seller)
admin.site.register(Transport)
admin.site.register(BlitzPay)

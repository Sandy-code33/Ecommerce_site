from django.contrib import admin
from .models import *
# Register your models here.
# username=Sandy
# password=root

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')
    
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','catagory','quantity','vendor')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
from django.contrib import admin
from .models import *
# Register your models here.
# username=Sandy
# password=root

class CatagoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')
    
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','catagory','quantity','vendor')
  


admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Product,ProductAdmin)

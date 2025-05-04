from django.contrib import admin
from .models import RawMaterial, Product, Supplier, InventoryMovement, RatioOfProduct, MaterialRequest, Unit

admin.site.register(RawMaterial)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(InventoryMovement)
admin.site.register(RatioOfProduct)
admin.site.register(MaterialRequest)
admin.site.register(Unit)
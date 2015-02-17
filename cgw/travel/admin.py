from django.contrib import admin
from travel.models import Group, Person, Quote

class GroupAdmin(admin.ModelAdmin):
	fields = ['name','salt']

class PersonAdmin(admin.ModelAdmin):
	fields = ['group_id','name','email','decided']

class QuoteAdmin(admin.ModelAdmin):
	fields = ['group_id','score','price','direct','origin','dep_date','out_carrier','destination','ret_date','in_carrier']

admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Quote, QuoteAdmin)

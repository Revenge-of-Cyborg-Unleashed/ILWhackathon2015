from django.contrib import admin
from travel.models import Group, Person, Quote, Flight

class GroupAdmin(admin.ModelAdmin):
	fields = ['name','salt']

class PersonAdmin(admin.ModelAdmin):
	fields = ['group_id','name','email','decided']

class QuoteAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['group_id','score','price','direct']}),
		('Outbound Leg', {'fields': ['out_origin', 'out_destination','dep_date','out_carrier']}),
		('Inbound Leg', {'fields': ['in_origin','in_destination','ret_date','in_carrier']}),
	]

class FlightAdmin(admin.ModelAdmin):
	fields = ['quote_id','outgoing','date','origin','destination','carrier']

admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Flight, FlightAdmin)

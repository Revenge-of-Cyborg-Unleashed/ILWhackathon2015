from cgw.skyscanner_query import BrowseCacheQuery
from travel.models import *
import importlib.machinery
import uuid

class saveQuery(object):
	def __init__(self, origin_place, destination_place, outbound_partial_date, inbound_partial_date, group_name, names_emails):
		# Declare constants
		print("STARTING SAVEQUERY")
		self.MARKET = "GB"
		self.CURRENCY = "GBP"
		self.LOCALE = "en-GB"
		print("SETTING PARAMETERS")
		# Declare variables
		self.origin_place = origin_place
		self.destination_place = destination_place
		self.outbound_partial_date = outbound_partial_date
		self.inbound_partial_date = inbound_partial_date
	
		self.name = group_name
		print("GENERATING SALT")
		self.salt = uuid.uuid4().hex
		print(self.salt)
		print("SETTING NAMES_EMAILS")	
		self.names_emails = names_emails
		print(self.names_emails)


	def doQuery(self):
		print("DOING DOQUERY")
		# Get Skyscanner Query
		if self.inbound_partial_date == None:
			self.query = BrowseCacheQuery(market=self.MARKET, currency=self.CURRENCY, locale=self.LOCALE, origin_place=self.origin_place, destination_place=self.destination_place, outbound_partial_date=self.outbound_partial_date)
		else:		
			self.query = BrowseCacheQuery(market=self.MARKET, currency=self.CURRENCY, locale=self.LOCALE, origin_place=self.origin_place, destination_place=self.destination_place, outbound_partial_date=self.outbound_partial_date, inbound_partial_date=self.inbound_partial_date)
		print("SORTING QUOTES")
		# Sort Query by Price
		self.sortedquotes = self.query.sortQuotesByPrice()
		print("TRIMMING QUOTES")
		# Trim off first 20 results
		self.sortedqueries = self.sortedquotes[:20]
		print("FORMATTING QUOTES")
		# Format (up to) 20 queries
		self.final_queries = []
		for q in self.sortedqueries:
			#print(q)
			self.final_queries.append(self.query.formatQuote(q))
		print("MAKING GROUP")
		# Make and fill a new Group
		group = Group(salt=self.salt, name=self.name)
		#self.group_id = group.salt
		group.save()
		#print(self.group_id)
		print("MAKING PEEPS")
		# Make and fill a new Person
		for (name, email) in self.names_emails:
			person = Person(name=name, email=email, decided=False, group_id=group)
			person.save()
		print("MAKING QUOTES")
		# Make and fill new Quotes
		for q in self.final_queries: #CHECK FOR EXISTENCE
			quote_id = q['QuoteId']
			price = q['MinPrice']
			if 'OutboundLeg' in q:
				dep_date = q['OutboundLeg']['DepartureDate']
				out_origin = q['OutboundLeg']['OriginName']
				out_destination = q['OutboundLeg']['DestinationName']
			else:
				dep_date = None
				out_origin = ''
				out_destination=''
			if 'InboundLeg' in q:
				ret_date = q['InboundLeg']['DepartureDate']
				in_origin = q['InboundLeg']['OriginName']
				in_destination = q['InboundLeg']['DestinationName']
			else:
				ret_date = None
				in_origin= ''
				in_destination= ''
			direct = q['Direct']
			quote = Quote(dep_date=dep_date, ret_date=ret_date, direct=direct, price=price, group_id=group, score=0, out_destination=out_destination, in_destination=in_destination, out_origin=out_origin, in_origin=in_origin)
			quote.save()
			# Make and fill new Flights
			if 'OutboundLeg' in q:
				for carrier in q['OutboundLeg']['CarrierNames']:
					flight = Flight(quote_id=quote, carrier=carrier, outgoing=True)
					flight.save()
			if 'InboundLeg' in q:
				for carrier in q['InboundLeg']['CarrierNames']:
					flight = Flight(quote_id=quote, carrier=carrier, outgoing=False)
					flight.save()
		
		print("RETURNING SALT")
		return self.salt

## TEST FUNCTIONS::TO BE DELETED
#q = saveQuery("LON", "ATH", "2015-06-06", "2015-06-08", "Test Group", [("Dave Lead","dave@dave.com"),("Bobby Bobs","bob@bobberty.com")])
#q.doQuery()


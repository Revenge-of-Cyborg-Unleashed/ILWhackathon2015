import requests
import json
import datetime
import copy


class SkyscannerQuery(object):
    """Object containing the data necessary to query the Skyscanner API"""

    def __init__(self, market, currency, locale,
                 origin_place, destination_place='anywhere',
                 outbound_partial_date='anytime', inbound_partial_date='anytime'):

        self.market, self.currency, self.locale = market, currency, locale
        self.origin_place, self.destination_place = origin_place, destination_place
        self.outbound_partial_date = outbound_partial_date
        self.inbound_partial_date = inbound_partial_date

        self.api_key = open('api_key.txt', 'r').read().strip('\n')

        self.results = self.queryBrowseCache()

    def queryBrowseCache(self):
        """Queries the Skyscanner browse cache and returns an array of quotes as dictionaries"""

        request_url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/' +  \
                      '{0}/{1}/{2}/{3}/{4}/{5}/{6}?apiKey={7}''' \
                      .format(self.market, self.currency, self.locale,
                              self.origin_place, self.destination_place,
                              self.outbound_partial_date,
                              self.inbound_partial_date, self.api_key)

        response = requests.get(request_url) # returns JSON string of quote data
        return json.loads(response.text)

    def formatQuote(self, quote):
        """Converts individual quotes to a more usable format, converting IDs to names and dates to datetime objects"""

        # for the outbound leg:
        # put names to origin and destination IDs
        outbound_origin_id = quote['OutboundLeg']['OriginId']
        outbound_origin_name = next(place['Name'] for place in self.results['Places'] if place['PlaceId'] == outbound_origin_id)

        outbound_destination_id = quote['OutboundLeg']['DestinationId']
        outbound_destination_name = next(place['Name'] for place in self.results['Places'] if place['PlaceId'] == outbound_destination_id)

        # put names to each carrier ID in the list
        outbound_carrier_names = []
        for carrier_id in quote['OutboundLeg']['CarrierIds']:
          name = next(place['Name'] for place in self.results['Carriers'] if place['CarrierId'] == carrier_id)
          outbound_carrier_names.append(name)

        # convert date string into a datetime object
        departure_date = datetime.datetime.strptime(quote['OutboundLeg']['DepartureDate'], '%Y-%m-%dT%H:%M:%S')

        # for the outbound leg:
        # put names to origin and destination IDs
        inbound_origin_id = quote['InboundLeg']['OriginId']
        inbound_origin_name = next(place['Name'] for place in self.results['Places'] if place['PlaceId'] == inbound_origin_id)

        inbound_destination_id = quote['InboundLeg']['DestinationId']
        inbound_destination_name = next(place['Name'] for place in self.results['Places'] if place['PlaceId'] == inbound_destination_id)

        # put names to each carrier ID in the list
        inbound_carrier_names = []
        for carrier_id in quote['InboundLeg']['CarrierIds']:
          name = next(place['Name'] for place in self.results['Carriers'] if place['CarrierId'] == carrier_id)
          inbound_carrier_names.append(name)

        # convert date string into a datetime object
        return_date = datetime.datetime.strptime(quote['InboundLeg']['DepartureDate'], '%Y-%m-%dT%H:%M:%S')

        return {'QuoteId': quote['QuoteId'], 'OutboundLeg': {'OriginName': outbound_origin_name, 'CarrierIds': outbound_carrier_names,
                'DepartureDate': departure_date, 'DestinationName': outbound_destination_name},
                'MinPrice': quote['MinPrice'], 'InboundLeg': {'OriginId': inbound_origin_name, 'CarrierIds': inbound_carrier_names,
                'DepartureDate': return_date, 'DestinationName': inbound_destination_name},
                'Direct': quote['Direct']}

    def getSortedQuotes(self):
      """Returns array of quotes sorted by price"""

        quotes = self.queryBrowseCache()['Quotes']
        return sorted(quotes, key=lambda quote: quote['MinPrice'])

# a query with the bare minimum of information
# ssq = SkyscannerQuery('UK', 'GBP', 'En-GB', 'UK')

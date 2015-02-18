import requests
import datetime
import json
import http.client
import os


class SkyscannerQuery(object):
    """Object containing the data necessary to query the Skyscanner API"""

    def __init__(self, market, currency, locale):

        self.market, self.currency, self.locale = market, currency, locale

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'api_key.txt')
        self.api_key = open(filename, 'r').read().strip('\n')


class BrowseCacheQuery(SkyscannerQuery):
    """A query of the Skyscanner browse cache"""

    def __init__(self, market, currency, locale,
                 origin_place, destination_place='anywhere',
                 outbound_partial_date='anytime', inbound_partial_date='anytime'):

        super().__init__(market, currency, locale)

        self.origin_place, self.destination_place = origin_place, destination_place
        self.outbound_partial_date = outbound_partial_date
        self.inbound_partial_date = inbound_partial_date

        self.results = self.makeQuery()

    def makeQuery(self):
        """Queries the Skyscanner browse cache and returns an array of quotes as dictionaries"""

        request_url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/' +  \
                      '{0}/{1}/{2}/{3}/{4}/{5}/{6}?apiKey={7}''' \
                      .format(self.market, self.currency, self.locale,
                              self.origin_place, self.destination_place,
                              self.outbound_partial_date,
                              self.inbound_partial_date, self.api_key)

        response = requests.get(request_url) # returns JSON string of quote data
        return response.json()

    def sortQuotesByPrice(self):
        """Returns array of quotes sorted by price"""

        quotes = self.makeQuery()['Quotes']
        return sorted(quotes, key=lambda quote: quote['MinPrice'])

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

        # for the inbound leg:
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

        return {'QuoteId': quote['QuoteId'], 'OutboundLeg': {'OriginName': outbound_origin_name, 'CarrierNames': outbound_carrier_names,
                'DepartureDate': departure_date, 'DestinationName': outbound_destination_name},
                'MinPrice': quote['MinPrice'], 'InboundLeg': {'OriginName': inbound_origin_name, 'CarrierNames': inbound_carrier_names,
                'DepartureDate': return_date, 'DestinationName': inbound_destination_name},
                'Direct': quote['Direct']}


class LivePriceQuery(SkyscannerQuery):

    def __init__(market, currency, locale,
                 origin_place, destination_place,
                 outbound_date, passengers, *optional_args):
        """Creates a Skyscanner live price query session, queries the session, and returns a dictionary of dictionaries"""

        super().__init__(market, currency, locale)

        self.origin_place = origin_place
        self.destination_place = destination_place
        self.outbound_date = outbound_date
        self.passengers = passengers

        self.results = self.makeQuery()

    def makeQuery(self):

        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'accept': 'application/json'}
        payload = {'apiKey': self.api_key, 'country': self.market, 'currency': self.currency,
                   'locale': self.locale, 'originplace': self.origin_place,
                   'destinationplace': self.destination_place,
                   'outbounddate': self.outbound_date, 'adults': self.passengers}
        url = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'

        session = requests.post(url, data=payload, headers=headers)

        if session.status_code != 201:
            raise http.client.HTTPException(session.json())

        polling_url = session.headers['Location'] + '?apiKey=' + api_key

        results = requests.get(polling_url)


# a query with the bare minimum of information
# bcq = BrowseCacheQuery('UK', 'GBP', 'en-GB', 'UK')
# print(ssq.formatQuote(ssq.results['Quotes'][0]))

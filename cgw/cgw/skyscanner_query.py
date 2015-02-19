import requests
import datetime
import json
from http.client import HTTPException
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

        formatted_quote = {'QuoteId': quote['QuoteId'], 'MinPrice': quote['MinPrice'], 'Direct': quote['Direct']}

        # for the outbound leg:
        # put names to origin and destination IDs
        if 'OutboundLeg' in quote:
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

            formatted_quote['OutboundLeg'] = {'OriginName': outbound_origin_name,
                                              'CarrierNames': outbound_carrier_names,
                                              'DepartureDate': departure_date,
                                              'DestinationName': outbound_destination_name}

        # for the inbound leg:
        # put names to origin and destination IDs
        if 'InboundLeg' in quote:
            inbound_origin_id = quote['InboundLeg']['OriginId']
            inbound_origin_name = next(place['Name'] for place in self.results['Places'] if place['PlaceId'] == inbound_origin_id)

            inbound_destination_id = quote['InboundLeg']['DestinationId']
            inbound_destination_name = next(place['Name'] for place in self.results['Places'] if place['PlaceId'] == inbound_destination_id)

            # put names to each carrier ID in the list
            inbound_carrier_names = []
            for carrier_id in quote['InboundLeg']['CarrierIds']:
                name = next(carrier['Name'] for carrier in self.results['Carriers'] if carrier['CarrierId'] == carrier_id)
                inbound_carrier_names.append(name)

            # convert date string into a datetime object
            return_date = datetime.datetime.strptime(quote['InboundLeg']['DepartureDate'], '%Y-%m-%dT%H:%M:%S')

            formatted_quote['InboundLeg'] = {'OriginName': inbound_origin_name,
                                             'CarrierNames': inbound_carrier_names,
                                             'DepartureDate': return_date, 'DestinationName': inbound_destination_name}

        return formatted_quote


class LivePriceQuery(SkyscannerQuery):

    def __init__(self, market, currency, locale,
                 origin_place, destination_place,
                 outbound_date, passengers):
        """Creates a Skyscanner live price query session, queries the session, and returns a dictionary of dictionaries"""

    # def __init__(*args, **kwargs):

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
                   'outbounddate': self.outbound_date, 'adults': self.passengers,
                   'locationschema': 'Iata'}
        url = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'

        session = requests.post(url, data=payload, headers=headers)

        if session.status_code != 201:
            raise HTTPException(session.json())

        polling_url = session.headers['Location'] + '?apiKey=' + self.api_key
        # add a way to save new location header

        return requests.get(polling_url).json()

    def formatLivePrice(self, itinerary):
        """Combines Itinerary and Leg dictionaries into one dictionary with cheapest flight information.

        IDs are replaced with names and date strings with datetime objects."""

        cheapest_itinerary = itinerary['PricingOptions'][0]

        leg = next(l for l in self.results['Legs'] if l['Id'] == itinerary['OutboundLegId'])

        formatted_live_price = {'Price': cheapest_itinerary['Price'],
                                'DeeplinkUrl': cheapest_itinerary['DeeplinkUrl'],
                                'QuoteAgeInMinutes': cheapest_itinerary['QuoteAgeInMinutes'],
                                'Directionality': leg['Directionality'],
                                'Duration': leg['Duration'], 'JourneyMode': leg['JourneyMode']}

        origin_station_id = leg['OriginStation']
        origin_name = next(place['Name'] for place in self.results['Places'] if place['Id'] == origin_station_id)
        destination_station_id = leg['DestinationStation']
        destination_name = next(place['Name'] for place in self.results['Places'] if place['Id'] == destination_station_id)

        departure_time = datetime.datetime.strptime(leg['Departure'], '%Y-%m-%dT%H:%M:%S')
        arrival_time = datetime.datetime.strptime(leg['Arrival'], '%Y-%m-%dT%H:%M:%S')

        # dict(dict_one.items() | dict_two.items()) combines two dictionaries
        formatted_live_price = dict(formatted_live_price.items() |
                                    {'ArrivalTime': arrival_time,
                                     'DepartureTime': departure_time,
                                     'OriginName': origin_name,
                                     'DestinationName': destination_name}.items())

        carrier_names = []
        for carrier_id in leg['Carriers']:
            name = next(carrier['Name'] for carrier in self.results['Carriers'] if carrier['Id'] == carrier_id)
            carrier_names.append(name)

        formatted_live_price['CarrierNames'] = carrier_names

        return formatted_live_price

    def getCheapest(self, n=1):
        cheapest_live_prices = []
        for x in range(n):
            live_price = self.results['Itineraries'][x]
            cheapest_live_prices.append(self.formatLivePrice(live_price))

        return cheapest_live_prices


class AutoSuggestQuery(SkyscannerQuery):

    def __init__(self, market, currency, locale, query_string):

        super().__init__(market, currency, locale)
        self.query_string = query_string

        self.results = self.makeQuery()

    def makeQuery(self):

        url = 'http://partners.api.skyscanner.net/apiservices/autosuggest/' + \
              'v1.0/{0}/{1}/{2}/?query={3}&apiKey={4}' \
              .format(self.market, self.currency, self.locale,
                      self.query_string, self.api_key)

        response = requests.get(url)
        return response.json()

    def getClosest(self, n=1):
        closest_suggestions = []
        number_of_suggestions = min(len(self.results['Places']), n)
        for x in range(number_of_suggestions):
            suggestion = self.results['Places'][x]
            closest_suggestions.append(suggestion)

        return closest_suggestions

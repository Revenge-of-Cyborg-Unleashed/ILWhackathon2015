import requests
import json


class SkyscannerQuery(object):
    """Object containing data necessary to query API"""
    def __init__(self, market, currency, locale,
                 originPlace, destinationPlace='anywhere',
                 outboundPartialDate='anytime', inboundPartialDate='anytime'):
        self.market, self.currency, self.locale = market, currency, locale
        self.originPlace, self.destinationPlace = originPlace, destinationPlace
        self.outboundPartialDate = outboundPartialDate
        self.inboundPartialDate = inboundPartialDate

        self.api_key = open('api_key.txt', 'r').read().strip('\n')

    def queryBrowseCache(self):
        """Queries the Skyscanner browse cache and returns a dictionary"""
        request_url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/' +  \
                      '{0}/{1}/{2}/{3}/{4}/{5}/{6}?apiKey={7}''' \
                      .format(self.market, self.currency, self.locale,
                              self.originPlace, self.destinationPlace,
                              self.outboundPartialDate,
                              self.inboundPartialDate, self.api_key)

        request = requests.get(request_url)
        quotes = json.loads(request.text)
        return quotes

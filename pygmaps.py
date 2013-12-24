#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This a small wrapper around Google Maps API v3. Mostly based on googlemaps by John Kleint.
"""

import json
from urllib import urlencode

import requests


GEOCODE_QUERY_URL = 'http://maps.googleapis.com/maps/api/geocode/json?'
DIRECTIONS_QUERY_URL = 'http://maps.googleapis.com/maps/api/directions/json?'
DISTANCEMATRIX_QUERY_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json?'
STATUS_OK = 'OK'

__all__ = ['fetch_json', 'directions_request', 'distancematrix_request', 'get_time', 'get_distance']


class GoogleMapsError(Exception):
    """
    Base class for errors and exceptions.
    """
    #: See http://code.google.com/apis/maps/documentation/geocoding/index.html#StatusCodes
    #: for information on the meaning of these status codes.
    G_GEO_SUCCESS = 200
    G_GEO_SERVER_ERROR = 500
    G_GEO_MISSING_QUERY = 601
    G_GEO_UNKNOWN_ADDRESS = 602
    G_GEO_UNAVAILABLE_ADDRESS = 603
    G_GEO_BAD_KEY = 610
    G_GEO_TOO_MANY_QUERIES = 620

    _STATUS_MESSAGES = {
        G_GEO_SUCCESS: 'G_GEO_SUCCESS',
        G_GEO_SERVER_ERROR: 'G_GEO_SERVER_ERROR',
        G_GEO_MISSING_QUERY: 'G_GEO_MISSING_QUERY',
        G_GEO_UNKNOWN_ADDRESS: 'G_GEO_UNKNOWN_ADDRESS',
        G_GEO_UNAVAILABLE_ADDRESS: 'G_GEO_UNAVAILABLE_ADDRESS',
        G_GEO_BAD_KEY: 'G_GEO_BAD_KEY',
        G_GEO_TOO_MANY_QUERIES: 'G_GEO_TOO_MANY_QUERIES',
    }

    def __init__(self, status, response=None):
        """
        Create an exception with a status and optional full response.

        :param status: Either a ``G_GEO_`` code or a string explaining the
         exception.
        :type status: int or string

        :param response: The actual response returned from Google, if any.
        :type response: dict
        """
        Exception.__init__(self, status)
        self.status = status
        self.response = response

    def __str__(self):
        """
        Return a string representation of this :exc:`GoogleMapsError`.
        """
        if self.status in self._STATUS_MESSAGES:
            if self.response is not None and 'responseDetails' in self.response:
                retval = 'Error %d: %s' % (self.status, self.response['responseDetails'])
            else:
                retval = 'Error %d: %s' % (self.status, self._STATUS_MESSAGES[self.status])
        else:
            retval = str(self.status)
        return retval

    def __unicode__(self):
        """
        Return a unicode representation of this :exc:`GoogleMapsError`.
        """
        return unicode(self.__str__())


def fetch_json(query_url, params={}, headers={}, verbose=False):
    """
    Retrieves a JSON object from a (parametrized) URL.

    :param query_url: The base URL to query
    :type query_url: str

    :param params: Dictionary mapping (string) query parameters to values
    :type params: dict

    :param headers: Dictionary giving (string) HTTP headers and values
    :type headers: dict

    :param verbose:
    :type verbose: bool

    :return: Response obj (from requests), constructed from the data fetched from that URL.
    :rtype: requests.Response
    """

    # notice that sensor='false' is True
    params = {k: v for k, v in params.iteritems() if v}

    encoded_params = urlencode(params)
    url = query_url + encoded_params

    if verbose:
        print url

    return requests.get(url, headers=headers)


def _make_request(url, params, verbose=False):
    """
    Makes a request to given url with given params.

    :param url:
    :type url: str

    :param params: Dict of params we pass to url
    :type params: dict

    :param verbose:
    :type verbose: bool

    :return: Response in json
    :rtype: dict
    """
    response = fetch_json(url, params=params, verbose=verbose)
    text = json.loads(response.text)

    status_code = text['status']
    if status_code != STATUS_OK:
            raise GoogleMapsError(status_code, response=response)

    return text


def directions_request(origin, destination, sensor='false', mode='driving', waypoints=None, destination_time=None,
                       arrival_time=None, verbose=False):
    """
    Makes a request to Google Maps Api Directions
    See https://developers.google.com/maps/documentation/directions/#DirectionsRequests for additional information

    :param origin: The address or textual latitude/longitude value from which you wish to calculate directions
    :type origin: string, (latitude,longitude) !no space! or list of them

    :param destination: The address or textual latitude/longitude value from which you wish to calculate directions
    :type destination: string or (latitude,longitude) !no space!

    :param sensor: Indicates whether or not the directions request comes from a device with a location sensor. Default 'false'
    :type sensor: string, but 'true' or 'false'

    :param mode: Specifies the mode of transport to use when calculating directions. Default 'driving'
    :type mode: string, one of (walking, driving, bicycling, transit)

    :param waypoints: pecifies an array of waypoints. Waypoints alter a route by routing it through the specified location(s)
    :type waypoints: string, (latitude, longitude) or list of them. List should be separated with |

    :param destination_time: Specifies the desired time of destination for transit directions as seconds since midnight, January 1, 1970 UTC
    :type destination_time: int

    :param arrival_time: Specifies the desired time of arrival for transit directions as seconds since midnight, January 1, 1970 UTC
    :type arrival_time: int

    :param verbose:
    :type verbose: bool

    :return: Dict obj, constructed from the result data
    :rtype: dict
    """

    params = {
        'origin': origin,
        'destination': destination,
        'sensor': sensor,
        'mode': mode,
        'waypoints': waypoints,
        'destination_time': destination_time,
        'arrival_time': arrival_time
    }

    return _make_request(url=DIRECTIONS_QUERY_URL, params=params, verbose=verbose)


def distancematrix_request(origins, destinations, sensor='false', mode='driving', waypoints=None, destination_time=None,
                           arrival_time=None, verbose=False):
    """
    Makes a request to Google Maps Api DistanceMatrix
    See https://developers.google.com/maps/documentation/distancematrix/ for additional information

    :param origins: The address or textual latitude/longitude value from which you wish to calculate directions
    :type origins: string, (latitude,longitude) !no space! or list of them

    :param destinations: The address or textual latitude/longitude value from which you wish to calculate directions
    :type destinations: string or (latitude,longitude) !no space!

    :param sensor: Indicates whether or not the directions request comes from a device with a location sensor. Default 'false'
    :type sensor: string, but 'true' or 'false'

    :param mode: Specifies the mode of transport to use when calculating directions. Default 'driving'
    :type mode: string, one of (walking, driving, bicycling, transit)

    :param waypoints: pecifies an array of waypoints. Waypoints alter a route by routing it through the specified location(s)
    :type waypoints: string, (latitude, longitude) or list of them. List should be separated with |

    :param destination_time: Specifies the desired time of destination for transit directions as seconds since midnight, January 1, 1970 UTC
    :type destination_time: int

    :param arrival_time: Specifies the desired time of arrival for transit directions as seconds since midnight, January 1, 1970 UTC
    :type arrival_time: int

    :param verbose:
    :type verbose: bool

    :return: Dict obj, constructed from the result data
    :rtype: dict
    """

    params = {
        'origins': origins,
        'destinations': destinations,
        'sensor': sensor,
        'mode': mode,
        'waypoints': waypoints,
        'destination_time': destination_time,
        'arrival_time': arrival_time
    }

    return _make_request(url=DISTANCEMATRIX_QUERY_URL, params=params, verbose=verbose)


def get_time(origin, destination, sensor='false', mode='driving', waypoints=None, destination_time=None,
             arrival_time=None, verbose=False):
    """
    Returns travel time

    :param origin: The address or textual latitude/longitude value from which you wish to calculate directions
    :type origin: string, (latitude,longitude) !no space! or list of them

    :param destination: The address or textual latitude/longitude value from which you wish to calculate directions
    :type destination: string or (latitude,longitude) !no space!

    :param sensor: Indicates whether or not the directions request comes from a device with a location sensor. Default 'false'
    :type sensor: string, but 'true' or 'false'

    :param mode: Specifies the mode of transport to use when calculating directions. Default 'driving'
    :type mode: string, one of (walking, driving, bicycling, transit)

    :param waypoints: pecifies an array of waypoints. Waypoints alter a route by routing it through the specified location(s)
    :type waypoints: string, (latitude, longitude) or list of them. List should be separated with |

    :param destination_time: Specifies the desired time of destination for transit directions as seconds since midnight, January 1, 1970 UTC
    :type destination_time: int

    :param arrival_time: Specifies the desired time of arrival for transit directions as seconds since midnight, January 1, 1970 UTC
    :type arrival_time: int

    :param verbose:
    :type verbose: bool

    :return: Seconds to travel
    :rtype: int
    """

    return distancematrix_request(origin, destination, sensor, mode, waypoints, destination_time, arrival_time,
                                  verbose=verbose)['rows'][0]['elements'][0]['duration']['value']


def get_distance(origin, destination, sensor='false', mode='driving', waypoints=None, destination_time=None,
                 arrival_time=None, verbose=False):
    """
    Returns distance, in metres

    :param origin: The address or textual latitude/longitude value from which you wish to calculate directions
    :type origin: string, (latitude,longitude) !no space! or list of them

    :param destination: The address or textual latitude/longitude value from which you wish to calculate directions
    :type destination: string or (latitude,longitude) !no space!

    :param sensor: Indicates whether or not the directions request comes from a device with a location sensor. Default 'false'
    :type sensor: string, but 'true' or 'false'

    :param mode: Specifies the mode of transport to use when calculating directions. Default 'driving'
    :type mode: string, one of (walking, driving, bicycling, transit)

    :param waypoints: pecifies an array of waypoints. Waypoints alter a route by routing it through the specified location(s)
    :type waypoints: string, (latitude, longitude) or list of them. List should be separated with |

    :param destination_time: Specifies the desired time of destination for transit directions as seconds since midnight, January 1, 1970 UTC
    :type destination_time: int

    :param arrival_time: Specifies the desired time of arrival for transit directions as seconds since midnight, January 1, 1970 UTC
    :type arrival_time: int

    :param verbose:
    :type verbose: bool

    :return: Metres to travel
    :rtype: int
    """

    return distancematrix_request(origin, destination, sensor, mode, waypoints, destination_time, arrival_time,
                                  verbose=verbose)['rows'][0]['elements'][0]['distance']['value']

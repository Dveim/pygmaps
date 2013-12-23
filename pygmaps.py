#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This a small wrapper around Google Maps API v3. Inspired by googlemaps by John Kleint.
"""

import json
from urllib import urlencode

import requests


_DIRECTIONS_QUERY_URL = 'http://maps.googleapis.com/maps/api/directions/json?'
_DISTANCEMATRIX_QUERY_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json?'


def fetch_json(query_url, params={}, headers={}, silent=True):
    """
    Retrieves a JSON object from a (parameterized) URL.

    :param query_url: The base URL to query
    :type query_url: str

    :param params: Dictionary mapping (string) query parameters to values
    :type params: dict

    :param headers: Dictionary giving (string) HTTP headers and values
    :type headers: dict

    :param silent:
    :type silent: bool

    :return: Response obj (from requests), constructed from the data fetched from that URL.
    :rtype: requests.Response
    """

    # notice that sensor='false' is True
    params = {k: v for k, v in params.iteritems() if v}

    encoded_params = urlencode(params)
    url = query_url + encoded_params

    if not silent:
        print url

    return requests.get(url, headers=headers)


def directions_request(origin, destination, sensor='false', mode='driving', waypoints=None, destination_time=None,
                       arrival_time=None, silent=True):
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

    :param silent:
    :type silent: bool

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

    response = fetch_json(_DIRECTIONS_QUERY_URL, params=params, silent=silent)
    return json.loads(response.text)


def distancematrix_request(origins, destinations, sensor='false', mode='driving', waypoints=None, destination_time=None,
                           arrival_time=None, silent=True):
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

    :param silent:
    :type silent: bool

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

    response = fetch_json(_DISTANCEMATRIX_QUERY_URL, params=params, silent=silent)
    return json.loads(response.text)


def get_time(origin, destination, sensor='false', mode='driving', waypoints=None, destination_time=None,
             arrival_time=None, silent=True):
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

    :param silent:
    :type silent: bool

    :return: Seconds to travel
    :rtype: int
    """

    return distancematrix_request(origin, destination, sensor, mode, waypoints, destination_time, arrival_time)[
        'rows'][0]['elements'][0]['duration']['value']


def get_distance(origin, destination, sensor='false', mode='driving', waypoints=None, destination_time=None,
                 arrival_time=None, silent=True):
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

    :param silent:
    :type silent: bool

    :return: Metres to travel
    :rtype: int
    """

    return distancematrix_request(origin, destination, sensor, mode, waypoints, destination_time, arrival_time,
                                  silent=silent)['rows'][0]['elements'][0]['distance']['value']


if __name__ == '__main__':
    def main():
        # TODO: make those tests
        '''
        test_req = 'http://maps.googleapis.com/maps/api/directions/json?origin=Brooklyn&destination=Queens&sensor=false&departure_time=1343641500&mode=transit'
        a = fetch_json(test_req)
        print a
        '''

        '''
        a = directions_request(origin='Москва', destination='Киев', mode='walking')
        print a
        '''

        '''
        a = directions_request(origin='Київ, Сєченова 6', destination='Київ, Сєченова 9', mode='walking')
        print a
        '''

    main()
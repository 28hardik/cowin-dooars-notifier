#!./env/bin/python3
import time
import messaging
import requests
import json
import datetime
import cowinException

# Session schema keys
centers_key = 'centers'
min_age_key = 'min_age_limit'
available_capacity_key = 'available_capacity'
vaccine_key = 'vaccine'
name_key = 'name'
pincode_key = 'pincode'
sessions_key = 'sessions'
date_key = 'date'
address_key = 'address'


date_format = '%d-%m-%y'


def get_avail_centers(district):
    # Api endpoint
    api = '/v2/appointment/sessions/public/calendarByDistrict'
    endpoint = 'https://cdn-api.co-vin.in/api'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                      + ' Chrome/39.0.2171.95 Safari/537.36'
    }

    # Api Params
    today = datetime.date.today()

    all_centers = {}

    while True:
        response = requests.get(endpoint + api, {'district_id': district,
                                                 'date': today.strftime(date_format)}, headers=headers)
        if response.ok:
            print(response)
            return get_available_centers(response)
        else:
            print(response)
            print(response.text)
            print("Taking a break")
            raise cowinException.CowinException()


def get_available_centers(response):
    available_centers = list()
    centers = json.loads(response.text)[centers_key]
    for c in centers:
        available_centre = {sessions_key: list()}
        for s in c[sessions_key]:
            if s[min_age_key] < 45 and s[available_capacity_key] > 0:
                available_centre[sessions_key].append({
                    available_capacity_key: s[available_capacity_key],
                    date_key: s[date_key],
                    vaccine_key: s[vaccine_key]
                })
        if len(available_centre[sessions_key]) > 0:
            available_centre[pincode_key] = c[pincode_key]
            available_centre[name_key] = c[name_key]
            available_centre[address_key] = c[address_key]
            available_centers.append(available_centre)
    return available_centers


def main():
    alipurduar_district = '710'
    avail_centers = get_avail_centers(alipurduar_district)
    if len(avail_centers) > 0:
        print(avail_centers)


if __name__ == "__main__":
    main()

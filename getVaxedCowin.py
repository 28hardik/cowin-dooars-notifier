#!./env/bin/python3
import sys
import traceback
import cowinException
import time
import datetime
import getCentres
import messaging
import pytz


def update(cur_time, district, telegram_group_code):
    centres = getCentres.get_avail_centers(district)
    if len(centres) > 0:
        message = list()
        message.append("=UPDATE AS OF {}=\n".format(cur_time))
        results = 0
        for c in centres:
            results += 1
            message.append('===============')
            message.append(c[getCentres.name_key])
            message.append(c[getCentres.address_key])
            message.append(str(c[getCentres.pincode_key]))
            for s in c[getCentres.sessions_key]:
                message.append('----')
                message.append(str(s[getCentres.available_capacity_key]) + " slots available")
                message.append("for " + s[getCentres.vaccine_key])
                message.append("on " + s[getCentres.date_key])
            message.append('===============\n')
        message.append("=END OF UPDATE=")

        messaging.send('\n'.join(message), telegram_group_code)

        print("{} results sent out".format(results))


def main():
    districts = ['alipurduar', 'jalpaiguri', 'darjeeling']
    telegram_channel = '@telegram_channel' #Use your telegram channel id like this @channel_id
    ist = pytz.timezone("Asia/Kolkata")
    sleep_time = 60 / len(districts)
    i = 0
    while True:
        district = districts[i % len(districts)]
        print('Running for district', district)
        district_code = get_district_code(district)
        telegram_group_code = telegram_channel
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        cur_time = ist.localize(now).strftime('%d-%m-%y %H:%M:%S')
        try:
            update(cur_time, district_code, telegram_group_code)
            i += 1
        except cowinException.CowinException:
            print("waiting a bit more")
            if sleep_time < 600:
                sleep_time *= 2
            else:
                messaging.sendError('cowinException for district {}'.format(sys.argv[1]))
        except:
            print("Error occurred on {}".format(cur_time))
            messaging.sendError("main thread exception for district {}".format(sys.argv[1]))
            traceback.print_exc()
        else:
            print("Run successful on {}".format(cur_time))
            sleep_time = 60 / len(districts)
        time.sleep(sleep_time)


def get_district_code(district):
    switcher = {
        'alipurduar': '710',
        'jalpaiguri': '722',
        'darjeeling': '717'
    }
    if district in switcher:
        return switcher[district]
    else:
        raise NotImplementedError


if __name__ == '__main__':
    main()

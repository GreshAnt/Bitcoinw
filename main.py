import requests
import time

TIME_API = "http://worldtimeapi.org/api/timezone/Etc/UTC/"

def call_api(api_endpoint, params=None):
    try:
        response = requests.get(api_endpoint, params=params)

        # 检查响应状态码
        response.raise_for_status()

        # 解析JSON响应
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    

def now_time_str():
    print('Trying to get time.')
    while True:
        try:
            api_response = call_api(TIME_API, params=None)
            break
        except Exception as e:
            print('Failed, retying...')
            continue
        	
    whole_datetime = api_response['datetime']
    whole_datetime_spilted = whole_datetime.split(':')
    if whole_datetime_spilted[1] != ('1' or '01'):
        datetime_str1 = whole_datetime_spilted[0] + ':' + str(int(whole_datetime_spilted[1])-2)
        datetime_str2 = whole_datetime_spilted[0] + ':' + whole_datetime_spilted[1]
    else:
        datetime_str1 = str(int(whole_datetime_spilted[0])-1) + ':' + '59'
        datetime_str2 = whole_datetime_spilted[0] + ':' + whole_datetime_spilted[1]
    
    if int(whole_datetime_spilted[1]) < 10:
        print('<10')
        datetime_str1 = datetime_str1.split(':')
        datetime_str1 = datetime_str1[0] + ':0' + datetime_str1[1]
    
    return (datetime_str1, datetime_str2)


def bitcoin(*datetime_str):
    print('Trying to get bitcoin prise.')
    bitcoin_api = f'https://production.api.coindesk.com/v2/tb/price/values/BTC?start_date={datetime_str[0]}&end_date={datetime_str[1]}&interval=1m&ohlc=true'
    api_response = call_api(bitcoin_api, params=None)
    while True:
        try:
            bt = api_response['data']['entries'][0][1:]
            break
        except Exception as e:
            continue
    return bt


if __name__ == '__main__':
    datetime_str = now_time_str()
    last_co = bitcoin(*datetime_str)
    co = last_co
    print(f'\n\n>{co[0]}\n>{co[1]}\n>{co[2]}\n\n')
    
    while True:
        try:
            datetime_str = now_time_str()
            co = bitcoin(*datetime_str)
            
            if co != last_co:
                print(f'\n\n>{co[0]}\n>{co[1]}\n>{co[2]}\n\n')
                last_co = co
            else:  # 修正此行的缩进
                print('No updates, retrying...')
            
        except Exception as e:
            print(f"An error occurred: {e}")
            print('Retrying...')

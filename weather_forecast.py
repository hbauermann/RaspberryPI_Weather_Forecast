from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
##import epd4in2b
import time 
import json
import requests

##display = epd4in2b.EPD()
##display.init()

transition_time = 2
data_json = []
sensor_name = []
temperature = []
humidity = []
temp_mix = []
reduced_forecast_date = []
weather_condition = []
condition_icon = []
resized_condition_icon = []
forecast_date = []
forecast_icon = []
min_max_forecast_temperature = []

## Directory's List
dir_fonts = 'fonts/'
dir_project = ''
dir_icons = 'icons/'

## Fonts Style
font_tile = ImageFont.truetype(dir_fonts + 'FreeMonoBold.ttf', 40)
font_names_temp_humid = ImageFont.truetype(dir_fonts + 'DejaVuSans-Bold.ttf', 20)
font_data = ImageFont.truetype(dir_fonts + 'DS-DIGIB.TTF', 35)
font_time_date = ImageFont.truetype(dir_fonts + 'DS-DIGIB.TTF', 35)
font_conection = ImageFont.truetype(dir_fonts + 'FreeMonoBold.ttf', 45)
font_temp_current = ImageFont.truetype(dir_fonts + 'FreeMonoBold.ttf', 45)

## URLs
url_data = 'station_data'
url_forecast = 'url_forecast'


def data_update(data_json):
    while True:
        try:
            data_file = requests.get(url_data, timeout = 1)
            data_json = json.loads(data_file.text)
        except:
            with open(dir_project + 'sensor_data.json', 'r') as data_file:
                data_json = json.load(data_file)
            data_file.close()
            return data_json
        with open(dir_project + 'sensor_data.json', 'w') as save_json:
            json.dump(data_json, save_json)
        save_json.close()
        return data_json


def data_collect(data_json_sensors):
    for a in range(len(data_json_sensors['resultado'])):
        sensor_name.append(str(data_json_sensors['resultado'][a]['nome']))
        temperature.append(str(data_json_sensors['resultado'][a]['tipo_sensor'][0]['ultima_leitura']))
        humidity.append(str(data_json_sensors['resultado'][a]['tipo_sensor'][1]['ultima_leitura']))
        print(sensor_name[a])
        print(temperature[a])
        print(humidity[a])
    return sensor_name, temperature, humidity

def time_update():
    date = datetime.now()
    end_date = date.strftime('%d/%m/%Y')
    time_now = date.strftime('%H:%M')
    return time_now, end_date


def panel_update(transition_time = transition_time):
    tile = 'DISPLAY TILE HERE'
    tile_temperature = 'TEMPERATURE'
    tile_humidity = 'HUMIDITY'
    time_date_separator = ' - '
    while True:       
        counter = 0
        date_time = time_update()[1] + time_date_separator + time_update()[0] 
        for i in range(int(len(data_collect(data_update(data_json))[1])/2)):
            image_red = Image.new('1', (400, 300), 255)
##            image_red = Image.new('1', (display.EPD_WIDTH, display.EPD_HEIGHT), 255)
            draw_red = ImageDraw.Draw(image_red)
            image_black = Image.new('1', (400, 300), 255)
##            image_black = Image.new('1', (display.EPD_WIDTH, display.EPD_HEIGHT), 255)
            draw_black = ImageDraw.Draw(image_black)
            w = draw_black.textsize(tile, font = font_tile)[0]
            draw_black.text(((400 - w) / 2, 25), tile, font = font_tile, fill = 0)

            draw_black.rectangle((0, 0, 399, 4), fill = 0)
            draw_black.rectangle((0, 0, 4, 299), fill = 0)
            draw_black.rectangle((0, 295, 399, 299), fill = 0)
            draw_black.rectangle((395, 0, 399, 299), fill = 0)
            draw_black.rectangle((0, 84, 399, 89), fill = 0)    
            draw_black.rectangle((198, 89, 203, 249), fill = 0)
            draw_black.rectangle((0, 244, 399, 249), fill = 0)

            w = draw_black.textsize(sensor_name[counter], font = font_names_temp_humid)[0]
            draw_black.text(((200 - w)/2, 95), sensor_name[counter], font = font_names_temp_humid, fill = 0)
            w = draw_black.textsize(tile_temperature, font = font_names_temp_humid)[0]
            draw_black.text(((200 - w)/2, 125), tile_temperature, font = font_names_temp_humid, fill = 0)
            w = draw_black.textsize(temperature[counter], font = font_data)[0]
            draw_black.text(((200 - w)/2, 150), temperature[counter], font = font_data, fill = 0)
            w = draw_black.textsize(tile_humidity, font = font_names_temp_humid)[0]
            draw_black.text(((200 - w)/2, 185), tile_humidity, font = font_names_temp_humid, fill = 0)
            w = draw_black.textsize(humidity[counter], font = font_data)[0]
            draw_black.text(((200 - w)/2, 205), humidity[counter], font = font_data, fill = 0)

            w = draw_black.textsize(sensor_name[counter + 1], font=font_names_temp_humid)[0]
            draw_black.text((((200 - w)/2) + 200, 95), sensor_name[counter + 1], font = font_names_temp_humid, fill = 0)
            w = draw_black.textsize(tile_temperature, font = font_names_temp_humid)[0]
            draw_black.text((((200 - w)/2) + 200, 125), tile_temperature, font = font_names_temp_humid, fill = 0)
            w = draw_black.textsize(temperature[counter + 1], font = font_data)[0]
            draw_black.text((((200 - w)/2) + 200, 150), temperature[counter + 1], font = font_data, fill = 0)
            w = draw_black.textsize(tile_humidity, font = font_names_temp_humid)[0]
            draw_black.text((((200 - w)/2) + 200, 185), tile_humidity, font = font_names_temp_humid, fill = 0)
            w = draw_black.textsize(humidity[counter + 1], font = font_data)[0]
            draw_black.text((((200 - w)/2) + 200, 205), humidity[counter + 1], font = font_data, fill = 0)
            w = draw_black.textsize(date_time, font = font_time_date)[0]
            draw_black.text(((400 - w) / 2, 255), date_time, font = font_time_date, fill = 0)

##            display.display_frame(display.get_frame_buffer(image_black), display.get_frame_buffer(image_red))
            image_black.save(dir_project + 'image_black.bmp')
            counter += 2
            forecast_condtion()
            time.sleep(transition_time)
        forecast_condtion()
        return


def forecast_condtion(transition_time = transition_time):
    reduced_forecast_date = [] 
    weather_condition = []
    city_forecast, city_forecast_day, day_forecast, forecast_date, forecast_icon, min_max_forecast_temperature = forecast_update()
    time_date_separator = ' - '
    for a in range(4):
        temp_mix.append(str(min_max_forecast_temperature[a]))
        date_reducer = str(forecast_date[a])
        reduced_forecast_date.append(date_reducer[0:5])
        weather_condition.append(dir_project + dir_icons + str(forecast_icon[a]))
        condition_icon.append(Image.open(weather_condition[a] + '.png'))

    resized_condition_icon.append(condition_icon[0].resize((170, 170)))
    for a in range(1,4):
        resized_condition_icon.append(condition_icon[a].resize((100, 100)))

    temperature_now = city_forecast_day
    weather_condition1 = day_forecast
    tile = str(city_forecast)
    reduced_date_time = time_update()[1] + time_date_separator + time_update()[0]


##    image_red = Image.new('1', (display.EPD_WIDTH, display.EPD_HEIGHT), 255)
    image_red = Image.new('1', (400, 300), 255)
    draw_red = ImageDraw.Draw(image_red)
##    image_black = Image.new('1', (display.EPD_WIDTH, display.EPD_HEIGHT), 255)
    image_black = Image.new('1', (400, 300), 255)

    image_black.paste(resized_condition_icon[0], (0, 0), resized_condition_icon[0])
    draw_black = ImageDraw.Draw(image_black)

    image_black.paste(resized_condition_icon[1], (20, 185), resized_condition_icon[1])
    draw_black = ImageDraw.Draw(image_black)
    image_black.paste(resized_condition_icon[2], (153, 185), resized_condition_icon[2])
    draw_black = ImageDraw.Draw(image_black)
    image_black.paste(resized_condition_icon[3], (286, 185), resized_condition_icon[3])
    draw_black = ImageDraw.Draw(image_black)

    w = draw_black.textsize(tile, font = font_tile)[0]
    draw_black.text((((200 - w) / 2) + 180, 5), tile, font = font_tile, fill = 0)


    draw_black.rectangle((0, 0, 399, 4), fill = 0)
    draw_black.rectangle((0, 0, 4, 299), fill = 0)
    draw_black.rectangle((0, 295, 399, 299), fill = 0)
    draw_black.rectangle((395, 0, 399, 299), fill = 0)
    draw_black.rectangle((0, 174, 399, 179), fill = 0) ## primeira linha 
    draw_black.rectangle((133, 174, 138, 299), fill = 0)
    draw_black.rectangle((266, 174, 271, 299), fill = 0)

    w = draw_black.textsize(temp_mix[1], font = font_names_temp_humid)[0]
    draw_black.text(((133 - w)/2, 270), temp_mix[1], font = font_names_temp_humid, fill = 0)
    w = draw_black.textsize(temp_mix[2] , font = font_names_temp_humid)[0]
    draw_black.text((((133 - w)/2) + 133, 270), temp_mix[2], font = font_names_temp_humid, fill = 0)
    w = draw_black.textsize(temp_mix[3], font = font_names_temp_humid)[0]
    draw_black.text((((133 - w)/2) + 266, 270), temp_mix[3], font = font_names_temp_humid, fill = 0)
 
    w = draw_black.textsize(reduced_forecast_date[1], font = font_names_temp_humid)[0]
    draw_black.text((((133 - w)/2) + 3, 180), reduced_forecast_date[1], font = font_names_temp_humid, fill = 0)
    w = draw_black.textsize(reduced_forecast_date[2], font = font_names_temp_humid)[0]
    draw_black.text((((133 - w)/2) + 136, 180), reduced_forecast_date[2], font = font_names_temp_humid, fill = 0)
    w = draw_black.textsize(reduced_forecast_date[3], font = font_names_temp_humid)[0]
    draw_black.text((((133 - w)/2) + 267, 180), reduced_forecast_date[3], font = font_names_temp_humid, fill = 0)

    w = draw_black.textsize(temperature_now, font = font_temp_current)[0]
    draw_black.text((((200 - w) / 2) + 180, 60), temperature_now , font = font_temp_current, fill = 0)
    w = draw_black.textsize(weather_condition1, font = font_names_temp_humid)[0]
    draw_black.text(((400 - w) / 2, 150), weather_condition1 , font = font_names_temp_humid, fill = 0)
    w = draw_black.textsize(reduced_date_time, font = font_names_temp_humid)[0]
    draw_black.text((((200 - w) / 2) + 180, 120), reduced_date_time, font = font_names_temp_humid, fill = 0)

    time.sleep(transition_time)
##    display.display_frame(display.get_frame_buffer(image_black), display.get_frame_buffer(image_red))
    image_black.save(dir_project + 'image_black.bmp')
    return


def forecast_update():
    time_data_forecast = 16
    try:
        if int(time_update()[0][0:2]) != time_data_forecast:
            data_forecast = requests.get(url_forecast)
            forecast_jason_data = json.loads(data_forecast.text)
            time_data_forecast = int(time_update()[0][0:2])
        else:
            with open('weather_forecast.json', 'r') as data_forecast:
                forecast_jason_data = json.load(data_forecast)
            data_forecast.close()
    except:
        with open('weather_forecast.json', 'r') as data_forecast:
            forecast_jason_data = json.load(data_forecast)
        data_forecast.close()
    with open('weather_forecast.json', 'w') as save_forecast:
        json.dump(forecast_jason_data, save_forecast)
    save_forecast.close()
    city_forecast = forecast_jason_data['name']
    city_forecast_day = str(forecast_jason_data['data'][0]['temperature']['min']) + 'C/' + str(forecast_jason_data['data'][0]['temperature']['max']) + 'C'
    day_forecast = forecast_jason_data['data'][0]['text_icon']['text']['pt']
    for a in range(4):
        forecast_date.append(str(forecast_jason_data['data'][a]['date_br']))
        forecast_icon.append(forecast_jason_data['data'][a]['text_icon']['icon']['day'])
        min_max_forecast_temperature.append(str(forecast_jason_data['data'][a]['temperature']['min']) + 'C/' + str(forecast_jason_data['data'][a]['temperature']['max']) + 'C')
    return city_forecast, city_forecast_day, day_forecast, forecast_date, forecast_icon, min_max_forecast_temperature


if __name__ == '__main__':
    while True:
        panel_update()
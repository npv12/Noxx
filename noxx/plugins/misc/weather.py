import asyncio
from html import escape
from pyrogram import filters
from pyrogram.types import Message
import requests, json 

from ...noxx import Noxx, get_config_var
from ..constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("weather", HANDLING_KEY))
async def ping(app: Noxx, message):
    await message.edit("Fetching weather!")
    OPENWEATHER_API = get_config_var("openweather_api")
    if(OPENWEATHER_API == ""):
        await message.edit("No proper openweather api found")

    if len(message.command) <= 1:
        await message.edit("Enter the place of which weather you need to know`")
        await asyncio.sleep(2)
        await message.delete()
        return
    
    loc = message.command[1]
    OPENWEATHER_API = OPENWEATHER_API.replace('"','')
    openweather_url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={OPENWEATHER_API}"
    response = requests.get(openweather_url) 
    response_json = response.json()

    if(response_json["cod"] == '401'):
        await message.edit("Incorrect API key")

    elif(response_json["cod"]!= '404'):
        temp = response_json['main']['temp']
        feels_like = response_json['main']['feels_like']
        pressure = response_json['main']['pressure']
        humidity = response_json['main']['humidity']
        visibility = response_json['visibility']
        condition = response_json['weather'][0]['main']
        name = response_json['name']
        output_text = f"`The weather condition {name} is {condition}\nMore details are as follows:- \n\n Temperature = {temp}\n Feels like = {feels_like} \n Pressure = {pressure} \n Visibility = {visibility} \n Humidity = {humidity}`"
        await message.edit(output_text)
    else:
        print("Please check your internet connection")

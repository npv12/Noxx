import asyncio
from pyrogram import filters
from pyrogram.types import Message
import requests, json

from ...noxx import Noxx
from noxx import OPENWEATHER_API
from ..constants import HANDLING_KEY

@Noxx.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & ~filters.forwarded & filters.me & filters.command("weather", HANDLING_KEY))
async def ping(app: Noxx, message):
    await message.edit("Fetching weather!")
    if(OPENWEATHER_API == ""):
        await message.edit("No proper openweather api found")

    if len(message.command) <= 1:
        await message.edit("Enter the place of which weather you need to know`")
        await asyncio.sleep(2)
        await message.delete()
        return

    loc = message.command[1]
    openweather_url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={OPENWEATHER_API}"
    
    try:
        response = requests.get(openweather_url)
        response_json = response.json()
    except:
        await message.edit(f"Could not fetch weather")
        await asyncio.sleep(2)
        await message.delete()
        return

    if(response_json["cod"] == '401'):
        await message.edit("Incorrect API key")

    elif(response_json["cod"]!= '404'):
        temp = response_json['main']['temp'] - 273
        feels_like = response_json['main']['feels_like'] - 273
        pressure = response_json['main']['pressure']
        humidity = response_json['main']['humidity']
        visibility = response_json['visibility'] /1000
        condition = response_json['weather'][0]['main']
        name = response_json['name']
        output_text = f"`The weather condition {name} is {condition}\nMore details are as follows:- \n\n Temperature = {temp} ℃\n Feels like = {feels_like} ℃ \n Pressure = {pressure} Pa \n Visibility = {visibility} km \n Humidity = {humidity}`"
        await message.edit(output_text)
    else:
        await message.edit("Please don't force us to find weather of an imaginary place :D")

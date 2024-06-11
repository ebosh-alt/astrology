import logging
import time
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile
import pytz
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import FSInputFile
from geopy.geocoders import Nominatim
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from Bot.entity.NatalChart import ElementNatalChart
from Bot.entity.models import Date


from Bot.Data.config import bot
import asyncio

logger = logging.getLogger("__name__")


class VedicGoro:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.service = Service("geckodriver")

        self.BaseUrl = "https://vedic-horo.ru/analyse.php"
        self.basename = "cities15000"
        self.filename = f"Bot/Data/{self.basename}.zip"
        self.sign = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог",
                     "Водолей", "Рыбы"]
        self.coordinates = {
            1: {"sign": (295, 270), "planet": (300, 150)},
            2: {"sign": (160, 130), "planet": (155, 35)},
            3: {"sign": (135, 155), "planet": (60, 140)},
            4: {"sign": (270, 290), "planet": (155, 290)},
            5: {"sign": (135, 425), "planet": (60, 440)},
            6: {"sign": (160, 450), "planet": (155, 545)},
            7: {"sign": (295, 310), "planet": (310, 440)},
            8: {"sign": (430, 450), "planet": (450, 545)},
            9: {"sign": (450, 425), "planet": (535, 440)},
            10: {"sign": (315, 290), "planet": (460, 290)},
            11: {"sign": (450, 155), "planet": (535, 140)},
            12: {"sign": (430, 130), "planet": (450, 35)}}
        self.path_font = 'Bot/Data/CyrillicHelvet Bold.ttf'
        self.planets_eng = {
            "Асцендент": "As",
            "Солнце": "Su",
            "Луна": "Mo",
            "Марс": "Ma",
            "Меркурий": "Me",
            "Юпитер": "Ju",
            "Венера": "Ve",
            "Сатурн": "Sa",
            "Раху": "Ra",
            "Кету": "Ke"
        }

    def get_photo(self, natal_chart: list[ElementNatalChart]) -> FSInputFile:
        im = self.__get_background()
        draw = ImageDraw.Draw(im)
        self.__drawing_signs(draw, natal_chart)
        im.save("photo.png")
        return FSInputFile("photo.png")

    def get_info_city(self, city):
        data = self.__get_info_city(city)
        return f"{data[0]}, {data[1]}, {data[2]}"

    def get_natal_chart(self, city: str, name: str, date: Date) -> list[ElementNatalChart]:
        utc, lat, lon = self.__get_info_city(city)
        url = f"{self.BaseUrl}?name={name}&date={date.day}.{date.month}.{date.year}&time={date.hour}:{date.minute}:00&" \
              f"latitude={lat}&longitude={lon}&timezone={utc}"
        natal_chart: list[ElementNatalChart] = self.create_natal_chart(url)
        return natal_chart

    def create_natal_chart(self, url) -> list[ElementNatalChart]:
        logger.info(f"Request to {url}")
        driver, html = self.__get_html_natal_chert(url)
        driver.close()
        driver.quit()
        logger.info(f"Complete request to: {url}")
        natal_chart: list[ElementNatalChart] = []
        for i in html:
            el = i.split(" ")
            if el[1] == "(R)":
                planet: str = el[0] + el[1]
                sign: str = el[4]
                id_sign: int = self.sign.index(sign) + 1
            else:
                planet: str = el[0]
                sign: str = el[3]
                id_sign: int = self.sign.index(sign) + 1
            if el[9].isdigit():
                house: int = int(el[9])
            elif el[10].isdigit():
                house: int = int(el[10])
            elif el[11].isdigit():
                house: int = int(el[11])
            else:
                house = 1
            natal_chart.append(ElementNatalChart(planet=planet, sign=sign, id_sign=id_sign, house=house))
        return natal_chart

    def __drawing_signs(self, draw: ImageDraw, natal_charts: list[ElementNatalChart]):
        font = ImageFont.truetype(self.path_font, size=26)
        id_sign = natal_charts[0].id_sign
        for house in range(1, 13):
            text = ""
            for el in natal_charts:
                if el.house == house:
                    if "(R)" in el.planet:
                        text += f'{self.planets_eng[el.planet.replace("(R)", "")]}(R)  '
                    else:
                        text += self.planets_eng[el.planet] + "  "
            cor = self.coordinates[house]["planet"]
            w = draw.textlength(text, font=font)
            draw.text((cor[0] - (w / 2), cor[1]), text, font=font, fill='#1C0606')
            draw.text(self.coordinates[house]["sign"], str(id_sign), font=font, fill='#614e69')
            id_sign += 1
            if id_sign == 13:
                id_sign = 1

    def __get_html_natal_chert(self, url):
        driver = self.__get_driver()
        logger.info("Getting driver")
        driver.implicitly_wait(5)
        driver.get(url)
        logger.info("Getting url")
        el = driver.find_element(By.CLASS_NAME, "planets-info")
        logger.info("Received html natal chart")
        return driver, el.text.split("\n")

    @staticmethod
    def __get_background():
        with Image.open("background.jpg") as im:
            im.load()
        # im = Image.new('RGB', (600, 600), (255, 255, 255))
        # draw = ImageDraw.Draw(im)
        # draw.line(xy=((0, 0), (600, 600)), fill='gray', width=2)
        # draw.line(xy=((0, 600), (600, 0)), fill='gray', width=2)
        # draw.line(xy=((0, 300), (300, 600), (600, 300), (300, 0), (0, 300)), fill='gray', width=2)
        return im

    def __get_info_city(self, city: str):
        city2tz = defaultdict(set)
        with ZipFile(self.filename) as zf, zf.open(self.basename + '.txt') as file:
            for line in file:
                fields = line.split(b'\t')
                if fields:
                    name, asciiname, alternatenames = fields[1:4]
                    timezone = fields[-2].decode('utf-8').strip()
                    if timezone:
                        for ct in [name, asciiname] + alternatenames.split(b','):
                            ct = ct.decode('utf-8').strip()
                            if ct:
                                city2tz[ct].add(timezone)
        for tzname in city2tz[city]:
            if "Europe" in tzname:
                geolocator = Nominatim(user_agent="amvl;emvl;wvml;wmevl;mevl;m")
                location = geolocator.geocode(tzname.split("/")[1])
                lat, lon = float("%.2f" % location.latitude), float("%.2f" % location.longitude)
                now = datetime.now(pytz.timezone(tzname))
                return now.strftime("%z").replace("0", ""), lat, lon
        return "+3", 55.63, 37.61

    def __set_options(self, *args):
        for arg in args:
            self.options.add_argument(arg)
        logger.info("Setting options")

    def __get_driver(self):
        self.__set_options("--headless", "--disable-gpu")
        return webdriver.Firefox(service=self.service, options=self.options)

    async def __screen(self):
        bbox = (460, 120, 790, 440)
        driver = self.__get_driver()
        try:
            driver.maximize_window()
            url = f"{self.BaseUrl}?name=никита&date=12.03.2005&time=12:00:00&latitude=55.45&longitude=37.37&timezone=+3"
            driver.get(url)
            logger.info("request to %s", url)
            time.sleep(1)
            screenshot_bytes = driver.get_screenshot_as_png()
            logger.info("Screenshot taken")
            image = Image.open(BytesIO(screenshot_bytes))
            image.crop(bbox).save("vedic_horo.png")
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    async def __get_natal_chert(self):
        await self.__screen()


async def test():
    client = VedicGoro()
    natal_chart = client.get_natal_chart(city="Стерлитамак", name="Артем",
                                         date=Date(year="1997", month="11", day="22", hour="16", minute="48"))
    photo = client.get_photo(natal_chart=natal_chart)
    await bot.send_photo(
        chat_id=754513655,
        photo=photo
    )

if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.INFO,
    #     # filename="log.logging",
    #     format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
    #     filemode="w",
    #     encoding='utf-8')
    # client = VedicGoro()
    # natal_chart = client.get_natal_chart(city="Стерлитамак", name="Артем",
    #                                      date=Date(year="1997", month="11", day="22", hour="16", minute="48"))
    # client.get_photo(natal_chart=natal_chart)
    asyncio.run(test())

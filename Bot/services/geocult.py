import requests


class GeoCult:
    def __init__(self):
        self.baseURL = "https://geocult.ru/natalnaya-karta-onlayn-raschet"

    def get_photo_link(self, name: str, date: list, city: str, country: str, lot: float, lon: float):
        url = (f"{self.baseURL}?fn={name}&fd={date[0]}&fm={date[1]}&fy={date[2]}&fh={date[3]}&fmn={date[4]}&c1="
               f"{city}%2C+{country}&lt={lot}&ln={lon}&hs=v&sb=1")
        data = requests.get(url)
        text = data.text
        text = text.split("<a id='r660' class='fancybox' target='_blank' href='")[1]
        img = text.split("' width")[0]
        return img


if __name__ == "__main__":
    client = GeoCult()
    a = client.get_photo_link(
        name="Александр",
        date=["01", "01", "2000", "00", "00"],
        city="Москва",
        country="Россия",
        lot=55.7522200,
        lon=37.6155600)
    print(a)

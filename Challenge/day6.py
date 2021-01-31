import requests
from bs4 import BeautifulSoup

url = "https://www.iban.com/currency-codes"

countries = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]

for row in rows:
    items = row.find_all("td")
    name = items[0].text
    code = items[2].text
    if name and code:
        if name != "No universal currency":
            country = {"name": name.capitalize(), "code": code}
            countries.append(country)


def ask():
    try:
        choice = int(input("#: "))
        if choice > len(countries):
            print("Choose a number from the list.")
            return ask()
        else:
            country = countries[choice]
            print(f"{country['name']}")
            name = country["name"]
            code = country["code"]
            return [name, code]

    except ValueError:
        print("That wasn't a number.")
        return ask()


def ask_ver2():
    print("Where are you from? Choose a country by number", end="\n\n")
    from_country = ask()
    print("Now choose another country.", end="\n\n")
    out_country = ask()
    print(from_country, out_country)
    return from_country, out_country


def ask_money(from_country, out_country):
    f_n, f_c = from_country
    o_n, o_c = out_country
    try:
        print(f"How many {f_c} do you want to convert to {o_c}")
        money = int(input())
        return money
    except ValueError:
        print("That wasn't a number.", end="\n\n")
        return ask_money()


def Currency_Converter(from_country, out_country, f_money):
    f_n, f_c = from_country
    o_n, o_c = out_country
    url = f"https://transferwise.com/gb/currency-converter/{f_c.lower()}-to-{o_c.lower()}-rate?amount={f_money}"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    h3 = soup.find("h3", {"class": "cc__source-to-target"})
    # 환율사이트에서 긁어온 숫자 int로 바꾸는 과정 궁금
    ratio = str(h3.find("span", {"class": "text-success"}).string)
    return ratio


def final(ratio, f_money, from_country):
    f_code = from_country[1]
    f_money_form = "{}.00".format(f_money, ",")
    print(f"{f_code} {f_money_form} is ₩{float(ratio)*f_money}")


def ask_convert():
    from_country, out_country = ask_ver2()
    f_money = ask_money(from_country, out_country)
    ratio = Currency_Converter(from_country, out_country, f_money)
    final(ratio, f_money, from_country)


print("Welcome to CurrencyConvert PRO 2000", end="\n\n")
for index, country in enumerate(countries):
    print(f"#{index} {country['name']}")

ask_convert()

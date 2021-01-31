import requests
from bs4 import BeautifulSoup

url = "https://www.iban.com/currency-codes"


def extract_currency_code():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find(
        "table", {"class": "table table-bordered downloads tablesorter"}
    )
    links = pagination.find_all("tr")
    pages = []
    for link in links[1:]:
        list_ex = list(map(lambda x: str(x), link.find_all("td")))
        if "<td>No universal currency</td>" != list_ex[1]:
            list_ex_main = [list_ex[0], list_ex[2]]
            del_td = list(map(lambda x: x[4:-5], list_ex_main))
            pages.append(del_td)

    i = 0
    for C_name, Alpha_3_code in pages:
        print(f"# {i} {C_name} {Alpha_3_code}")
        i += 1

    def try_exception(pages):
        country_num = len(pages)
        try:
            num = int(input("#:"))
            if num > country_num:
                raise Exception("over C_num")
        except ValueError:
            print("That wasn't a number.")
            return try_exception(pages)
        except Exception as e:
            print("Choose a number from the list.")
            return try_exception(pages)
        return num

    num = try_exception(pages)
    print(f"You choose {pages[num][0]}")
    print(f"The currency code is {pages[num][1]}")


extract_currency_code()

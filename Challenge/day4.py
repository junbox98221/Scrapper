import requests


print("Welcome to IsItDown.py!")
print("Please write a URL or URLs you want to check. (separated by comma)")


def url():
    url_input = list(map(lambda x: x.strip(), input().split(",")))

    for link in url_input:
        if ".com" not in link:
            print(f"{link} is not a valid URL")
            continue
        elif "http" not in link:
            link = "http://" + link

        try:
            if requests.get(link).status_code == 200:
                response = "on"
        except requests.exceptions.ConnectionError:
            response = "down"
        print(f"{link} is {response}!")

    while True:
        print("Do you want to start over? y/n")
        yn = input()
        if yn == "y":
            return url()
        elif yn == "n":
            print("k. bye!")
            return
        else:
            print("That's not a valid answer")


url()

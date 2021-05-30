import requests
from datetime import timedelta
from bs4 import BeautifulSoup
from collections import Counter
from django.utils import timezone
from . import models


def get_user_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def google_search(
    words_from_titles,
    words_from_descriptions,
    webiste_links,
    query=None,
    response=None,
):

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

    headers = {
        "user-agent": USER_AGENT,
    }

    if query is not None:
        response = requests.get(f"https://google.pl/search?q={query}", headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("div", class_="yuRUbf")
        for link in links:
            webiste_links.append(link.find("a")["href"])

        for title in soup.find_all("h3", class_="LC20lb DKV0Md"):
            words = title.get_text().split(" ")
            for word in words:
                if word.isalpha():
                    words_from_titles.append(word)

        for description in soup.find_all("span", class_="aCOpRe"):
            words = description.get_text().split(" ")
            for word in words:
                if word.isalpha():
                    words_from_descriptions.append(word)

        next_page = soup.find("a", {"id": "pnnext"})
        if next_page is not None:
            next_page_query = next_page["href"]

            response = requests.get(
                f"https://google.com/{next_page_query}", headers=headers
            )
            return google_search(
                response=response,
                words_from_titles=words_from_titles,
                words_from_descriptions=words_from_descriptions,
                webiste_links=webiste_links,
                query=None,
            )

        else:
            top_10_from_titles = Counter(words_from_titles).most_common((10))
            top_10_from_descriptions = Counter(words_from_descriptions).most_common(
                (10)
            )
            number_of_search = soup.find("div", {"id": "result-stats"}).get_text()
            return (
                top_10_from_titles,
                top_10_from_descriptions,
                webiste_links,
                number_of_search.split("about")[-1],
            )

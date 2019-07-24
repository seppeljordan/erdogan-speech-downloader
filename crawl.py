import argparse
import datetime
import re
import urllib.parse

import bs4
import requests

INDEX = "https://www.tccb.gov.tr/receptayyiperdogan/konusmalar/"


def get_urls():
    return get_urls_from_index(INDEX)


def get_urls_from_index(url):
    current_url = urllib.parse.urlparse(url)
    results = set()
    index_soup = bs4.BeautifulSoup(requests.get(url).content, features="html.parser")
    content_soup = index_soup.find("div", id="divContentList")
    for link in content_soup.find_all("a"):
        href = link.get("href")
        if "?" in href:
            href_path, href_query = href.split("?")
        else:
            href_path = href
            href_query = ""
        link_url = urllib.parse.urlunparse(
            current_url._replace(path=href_path)._replace(query=href_query)
        )
        print("Found on index:", link_url)
        results.add(link_url)
    paging_soup = index_soup.find(class_="paging")
    current_page = paging_soup.find(class_="active")
    next_page = current_page.find_next_sibling()
    if next_page:
        next_path, next_query = next_page.get("href").split("?")
        next_url = urllib.parse.urlunparse(
            current_url._replace(path=next_path)._replace(query=next_query)
        )
        next_results = get_urls_from_index(next_url)
        results = results | next_results
    return results


def fetch_url(url):
    return requests.get(url).content


def parse_date(date_string):
    pattern = r"(?P<day>\d\d)\.(?P<month>\d\d)\.(?P<year>\d\d\d\d)"
    match = re.match(pattern, date_string)
    return datetime.date(
        year=int(match.group("year")),
        month=int(match.group("month")),
        day=int(match.group("day")),
    )


def escape_file_name(text):
    return text.replace(" ", "-").replace("'", "-").replace("/", "-")


def main():
    urls = get_urls()
    for url in urls:
        html_string = fetch_url(url)
        html_soup = bs4.BeautifulSoup(html_string, features="html.parser")
        speech_content = html_soup.find("div", id="divContentArea").get_text()
        detail_soup = html_soup.find("div", id="news-detail")
        date = parse_date(detail_soup.find("h6").get_text())
        title = escape_file_name(detail_soup.find("h1").get_text().strip())
        file_name = "".join(
            [
                str(date.year),
                "-",
                "{:02}".format(date.month),
                "-",
                "{:02}".format(date.day),
                "-",
                title,
                ".txt",
            ]
        )
        print("Start:", file_name)
        with open(file_name, "w") as f:
            print("# Downloaded from {}".format(url), file=f)
            print(file=f)
            print(speech_content, file=f)
        print("Finished:", file_name)


if __name__ == "__main__":
    main()

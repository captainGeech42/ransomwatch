from bs4 import BeautifulSoup


def handle_pages_while(site, pagination_class, soup, p, pagination_element="div"):
    while True:
        page_nav = soup.find(pagination_element, class_=pagination_class)
        if page_nav is None:
            break
        elif page_nav.attrs["href"].startswith("http://") or \
                page_nav.attrs["href"].startswith("https://") or \
                page_nav.attrs["href"].startswith("//"):
            url = page_nav.attrs["href"]
        else:
            url = site.url + page_nav.attrs["href"]
        r = p.get(f"{url}", headers=site.headers)
        soup = BeautifulSoup(r.content.decode(), "html.parser")
        site.handle_page(soup)


def handle_pages_for(site, p, pagination_class="page-numbers", pagination_element="a"):
    r = p.get(f"{site.url}", headers=site.headers)
    soup = BeautifulSoup(r.content.decode(), "html.parser")

    # find all pages
    page_nav = soup.find_all(pagination_element, class_=pagination_class, href=True)

    site_list = [site.url]

    for page in page_nav:
        try:
            # ignore refresh link
            if page.attrs["href"] == "#":
                continue
            # might exist repetition
            if page.attrs["href"] not in site_list:
                if page.attrs["href"].startswith("http://") or \
                        page.attrs["href"].startswith("https://") or \
                        page.attrs["href"].startswith("//"):
                    site_list.append(page.attrs["href"])
                else:
                    site_list.append(site.url + page.attrs["href"])
        except KeyError:
            continue

    for i in site_list:
        r = p.get(f"{i}", headers=site.headers)
        site.handle_page(r.content.decode())


def handle_pages_backwards(site, p, max_page_num):
    # start at the last page and go backwards, in case a new victim was added while running (unlikely but
    # possible)
    for i in range(max_page_num, 0, -1):
        r = p.get(f"{site.url}?page={i}", headers=site.headers)

        site.handle_page(r.content.decode())

    # check one past the last page to see if new orgs were added that caused another page to be added
    r = p.get(f"{site.url}?page={max_page_num + 1}", headers=site.headers)
    site.handle_page(r.content.decode())

import asyncio
import os
import re

import aiohttp
from bs4 import BeautifulSoup


class WebSearch:
    """
    WebSearch - class responsible for web scraping
    """

    @classmethod
    def find_phrase_on_website(
        cls, path_to_file, phrase, list_with_HTML_elements=None, FORMAT_TEXT=False
    ):
        """
        Saves text from tag if there is a "phrase" from given websites, returns path to file
            :param path_to_file: : path to file with websites
            :param phrase: phrase to lookup in website
            :param list_with_HTML_elements: list with HTML tags to lookup for phrase
            :param FORMAT_TEXT: if True formats text: removes \\n \\r \\t \\'\\" and whitespaces
        """
        set_of_websites = cls._set_of_websites(path_to_file)
        phrase = cls._check_for_phrase(phrase)
        if list_with_HTML_elements:
            cls._check_for_list_with_HTML_elements(list_with_HTML_elements)

        # async looping thru pages
        loop = asyncio.get_event_loop()
        web_search_result = loop.run_until_complete(
            asyncio.gather(
                *(
                    cls._get_results(url, phrase, list_with_HTML_elements, FORMAT_TEXT)
                    for url in set_of_websites
                )
            )
        )

        # removes empty dict from results
        web_search_result = [i for i in web_search_result if i]

        return cls._save_to_txt(web_search_result, phrase)

    @classmethod
    def _set_of_websites(cls, path_to_file):
        # returns list of urls from file
        if not isinstance(path_to_file, (str)):
            raise TypeError("path to file should be a string")

        if (
            os.path.isfile(path_to_file) is False
            or os.path.exists(path_to_file) is False
        ):
            raise FileNotFoundError("Path to file is incorrect")

        list_of_websites = open(path_to_file).read().splitlines()
        return set(list_of_websites)

    @classmethod
    def _check_for_phrase(cls, phrase):
        #  checks if phrase is valid and removes whitespaces from phrase
        if not isinstance(phrase, (str)):
            raise TypeError(f"phrase to find should be a string")

        phrase = phrase.strip()
        only_characters = "".join(phrase.split())
        if 2 > len(only_characters) or 40 < len(only_characters):
            raise ValueError(
                "searched phrase must contain at min 2 and max 40 characters"
            )

        return phrase

    @classmethod
    def _check_for_list_with_HTML_elements(cls, html_tags_type):
        # checks if html tags are in correct format
        if not isinstance(html_tags_type, (list, tuple)):
            raise TypeError(
                "accepted format for list_with_HTML_elements is list or tuple"
            )

    @classmethod
    async def _get_results(
        cls, url, phrase, list_with_HTML_elements, REMOVE_WHITESPACES
    ):
        # returns dict with {url: results from search}

        async with aiohttp.ClientSession() as session:
            text_from_website = await cls._download_html(session, url)

            # checks if there is text
            if text_from_website:
                lookup = cls._return_lookup(
                    phrase, text_from_website, list_with_HTML_elements
                )
                # reformat text if there is any
                if lookup:
                    lookup = cls._return_format_lookup(
                        lookup, phrase, REMOVE_WHITESPACES
                    )
                    # add text to the result if there is any
                    if lookup:
                        web_search_results = {url: lookup}
                        return web_search_results

    @classmethod
    async def _download_html(cls, session, url):
        # returns html text with given encoding from html meta charset if there is
        try:
            async with session.get(
                url, ssl=False
            ) as response:  # skip SSL certificate validation
                return await response.text(encoding=response.charset)
        except (
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.InvalidURL,
            aiohttp.client_exceptions.ClientOSError,
        ):
            return None

    @classmethod
    def _return_lookup(cls, phrase, text_from_website, list_with_HTML_elements):
        # returns text with given phrase after removing css/JS from it, lookup in html tag if provided

        # lxml to improve performance change to html.parser if searching is failing
        soup = BeautifulSoup(text_from_website, features="lxml")

        for script in soup(["script", "style"]):
            script.decompose()

        if list_with_HTML_elements:
            lookup = soup.find_all(list_with_HTML_elements, string=re.compile(phrase))
            lookup = [element.get_text() for element in lookup]
        else:
            lookup = soup.find_all(string=re.compile(phrase))

        return lookup

    @classmethod
    def _return_format_lookup(cls, lookup, phrase, REMOVE_WHITESPACES):
        # format given lookups removes result with one word and ones that are exactly the same as searching phrase

        # cleans text if REMOVE_WHITESPACES=True
        if REMOVE_WHITESPACES:
            translate_markups = str.maketrans("\n\t\r'\"", "   '\"")
            lookup = [
                element.strip().translate(translate_markups) for element in lookup
            ]

        for element in lookup:
            if element == phrase or len(element.split()) == 1:
                lookup.remove(element)

        return lookup

    @classmethod
    def _save_to_txt(
        cls, website_dict, phrase, file_name="information_from_websites.txt"
    ):
        # saves search result into txt file, file will be located in the same place as this module, returns path

        with open(file_name, "w", encoding="UTF-8") as info_txt:
            info_txt.write(f"SEARCH PHRASE:{phrase}\n")
            for dict_url in website_dict:
                for key, value in dict_url.items():
                    info_txt.write(f"WEBSITE:{key}\n")
                    info_txt.write(f"RESULTS:{value}\n")

        return os.path.join(os.getcwd(), file_name)

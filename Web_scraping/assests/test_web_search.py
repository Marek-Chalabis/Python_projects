import os

import pytest

import web_search


@pytest.mark.css_js
def test_find_phrase_on_website_css_html():
    # checks if css and JS can be returned from method
    path_to_file_with_test_URLs = os.path.join(os.getcwd(), "TEST_URLS_tag.txt")

    # for JS
    path = web_search.WebSearch.find_phrase_on_website(
        path_to_file_with_test_URLs, '@type": "ListItem",'
    )

    with open(path) as file:
        result_without_JS = file.read()

    assert "WEBSITE" not in result_without_JS

    # for CSS
    path = web_search.WebSearch.find_phrase_on_website(
        path_to_file_with_test_URLs, "   padding: "
    )

    with open(path) as file:
        result_without_css = file.read()

    assert "WEBSITE" not in result_without_css


@pytest.mark.format
def test_find_phrase_on_website_format():
    # compares two same result files one with specify tag other not
    path_to_file_with_test_URLs = os.path.join(os.getcwd(), "TEST_URLS_format.txt")
    path_without_format = web_search.WebSearch.find_phrase_on_website(
        path_to_file_with_test_URLs, "Reform of an overall", FORMAT_TEXT=False
    )
    with open(path_without_format) as file:
        result_without_format = file.read()

    path_with_format = web_search.WebSearch.find_phrase_on_website(
        path_to_file_with_test_URLs, "Reform of an overall", FORMAT_TEXT=True
    )
    with open(path_with_format) as file:
        result_with_format = file.read()

    assert result_with_format != result_without_format


@pytest.mark.tags
def test_find_phrase_on_website_tags():
    # compares two same result files one with specify tag other not
    path_to_file_with_test_URLs = os.path.join(os.getcwd(), "TEST_URLS_tag.txt")
    path_without_tag = web_search.WebSearch.find_phrase_on_website(
        path_to_file_with_test_URLs, "REST API"
    )

    with open(path_without_tag) as file:
        result_without_tag = file.read()

    path_without_tag = web_search.WebSearch.find_phrase_on_website(
        path_to_file_with_test_URLs, "REST API", ["p"]
    )
    with open(path_without_tag) as file:
        result_with_tag = file.read()

    assert result_without_tag != result_with_tag


@pytest.mark.tags_format
def test_find_phrase_on_website_tags_format():
    # tests format of provided html tags
    path_to_file_with_test_URLs = os.path.join(os.getcwd(), "TEST_URLS_correct.txt")
    with pytest.raises(TypeError):
        assert web_search.WebSearch.find_phrase_on_website(
            path_to_file_with_test_URLs,
            "Find something important",
            list_with_HTML_elements="here should be list or tuple",
        )


@pytest.mark.phrase
def test_find_phrase_on_website_phrase():
    # tests phrase
    path_to_file_with_test_URLs = os.path.join(os.getcwd(), "TEST_URLS_correct.txt")

    with pytest.raises(TypeError):
        assert web_search.WebSearch.find_phrase_on_website(
            path_to_file_with_test_URLs, 42
        )

    with pytest.raises(ValueError):
        assert web_search.WebSearch.find_phrase_on_website(
            path_to_file_with_test_URLs, ""
        )

    with pytest.raises(ValueError):
        assert web_search.WebSearch.find_phrase_on_website(
            path_to_file_with_test_URLs, " \n \n     m      \n\t   "
        )

    with pytest.raises(ValueError):
        assert web_search.WebSearch.find_phrase_on_website(
            path_to_file_with_test_URLs,
            "ponaddwustudziewięćdziesięciodziewięciokilometrowy",
        )


@pytest.mark.path
def test_find_phrase_on_website_path():
    # tests path to file
    with pytest.raises(TypeError):
        assert web_search.WebSearch.find_phrase_on_website([], "Ala ma kota")

    with pytest.raises(FileNotFoundError):
        assert web_search.WebSearch.find_phrase_on_website(
            r"C:\Users\Dalmatynczyk^fdsc_-=11111190^", "Ala ma kota"
        )

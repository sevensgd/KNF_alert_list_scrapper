import re
import requests

if __name__ == '__main__':
    page = requests.get("https://www.knf.gov.pl/o_nas/ostrzezenia_publiczne/lista_ostrzezenia.html")
    # I'm using a fact that companies on this list are inside <td> and their names start with a number.
    # That was really tricky to get everything in, few reasons why:
    #   - new lines inside one table cell (flags=re.DOTALL)
    #   - some names start with 1. name and a very small number with 1.&nbsp;name
    #   - a lot of trash in the data
    pattern = re.compile(r"\d{1,3}\.(.+?)</td>", flags=re.DOTALL)
    result = pattern.findall(page.content)

    # one of the items on the KNF list is a link for no reason ...
    link_pattern = re.compile(r"<a href=.+?>(.+?)</a>")
    # <br> pattern is more like a business decision in this case
    # some names have a <br> following them and some additional description
    # since I'm here only for names, I decided to ignore the descriptions after <br> ...
    br_pattern = re.compile(r"(.+?)<br>", flags=re.DOTALL)

    cleaned_up_result = []
    for item in result:
        # clean up trash I found after first run
        item = item.replace("&nbsp;", " ").replace("</p>", "").replace("<em>", "").replace("</em>", "") \
            .replace("&amp;", "").replace("\t", "").replace("\n", "").replace("\r", "").strip(' \t\n\r')
        # extract a name of a link item
        if link_pattern.match(item):
            item = link_pattern.findall(item)[0]
        # remove descriptions after <br> from names
        if br_pattern.match(item):
            item = br_pattern.findall(item)[0]
        # dump the cleaned up result somewhere
        cleaned_up_result.append(item)

    # for some reason I got some trash here in a first position - fuck it, let's pop it
    cleaned_up_result.pop(0)

    for clean_item in cleaned_up_result:
        print(clean_item)

    print ("Total number of positions: " + str(cleaned_up_result.__len__()))

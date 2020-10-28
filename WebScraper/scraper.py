# from bs4 import BeautifulSoup as soup
# from urllib.request import urlopen as uReq
import datetime
import json
import random
import re
import time
import urllib.request

import requests


# gsm_areana_url = 'https:#www.gsmarena.com#'

# try:
#     uClient = uReq(gsm_areana_url,)
#     gsmarena_home_html = uClient.read()
#     uClient.close()
#     home_page_soup = soup(gsmarena_home_html, "html.parser")

#     phone_makers_squares = home_page_soup.find(
#         "div", "class": "brandmenu-v2 light l-box clearfix")
#     # pr(phone_makers_squares)

#     brands_list_items = phone_makers_squares.ul.findAll("li")
#     for brand_li in brands_list_items:
#         pr(re.findall('"([^"]*)"', brand_li))
# except urllib.error.HTTPError as e:
#     pr(e.headers["Retry-After"])

def scrape_phones():
    with open('newphones.json') as phones_json_file:
        new_phones = json.load(phones_json_file)
    phones = 0
    phones_added = 0
    phones_updated = 0
    page_limit = 3
    # phone_html_code = ""
    # img_url = ""
    # tmp_img_url = ""
    # battery_life_html = ""
    # year_html = ""
    # bench_html = ""
    # price_html = ""
    # screen_size_html = ""
    # db_phone_url = ""
    # nfc_html = ""
    # headphone_jack_html = ""
    # current_element_html = ""
    # battery_life = 0
    # price = 0
    # bench = 0
    # year = 0
    eur_to_usd = get_exchange_rate()
    # dxo_score = 0
    # antutu = 0
    # screen_size = 0
    nono_brands = "blackberry sony vivo blu zte plum verykool yu panasonic wiko tecno infinix acer micromax lava " \
                  "lenovo vodafone microsoft energizer cat realme".split(' ')
    # brand_html_code = ""
    # start_keyword = ""
    # phone_url = ""
    # command = ""
    # nfc_presence = False
    # jack_presence = False
    # dual_sim_presence = False
    # ir_presence = False
    # kimovil_antutu_url = "https://www.kimovil.com/en/where-to-buy"
    source_home_page_url = "https://www.gsmarena.com"
    # get source home page HTML
    home_page_html_code = str(urllib.request.urlopen(source_home_page_url).read())  # open("homepage.txt", "r").read()

    brands_list_html = cut_string_upto(
        cut_string_from(home_page_html_code,
                        "Phone finder"),
        "pad")

    href_keyword = "href=\""
    while brands_list_html.find(href_keyword) != -1:  # go over phone brands

        brands_list_html = cut_string_from(brands_list_html, "href=\"")

        base_url_addition = cut_string_upto_including(brands_list_html, ".php")

        brand_url = source_home_page_url + "/" + base_url_addition

        # get brand page source html
        brand_html_code = str(urllib.request.urlopen(brand_url).read())  # open("samsungpage.txt", "r").read()

        # search for nono brand names in current brand url
        if any(x in base_url_addition for x in nono_brands):
            continue

        brand_html_code = cut_string_from(
            cut_string_from(brand_html_code,
                            "review-body"),
            "<li>")

        current_page = 0

        while current_page < page_limit:  # keep flipping brand pages up until (including) page 2
            # flips to the next page
            href_keyword = "href=\""
            # gos over the phones in the page
            while (brand_html_code.find(href_keyword) != -1 and (
                    brand_html_code.find(href_keyword) < brand_html_code.find("</ul>") or brand_html_code.find(
                href_keyword) < brand_html_code.find("</ul >") or brand_html_code.find(
                href_keyword) < brand_html_code.find("</ ul>") or brand_html_code.find(
                href_keyword) < brand_html_code.find("< /ul>") or brand_html_code.find(
                href_keyword) < brand_html_code.find("</ ul >") or brand_html_code.find(
                href_keyword) < brand_html_code.find("< / ul>") or brand_html_code.find(
                href_keyword) < brand_html_code.find("< /ul >") or brand_html_code.find(
                href_keyword) < brand_html_code.find("< / ul >"))):  # keeps finding phones in brand_html_code

                phones += 1
                print("phone: " + str(phones))
                minute = 60
                time.sleep(minute * 5)
                # remove everything up to the link
                brand_html_code = cut_string_from(brand_html_code, "href=\"")

                # remove everything after the link
                base_url_addition = cut_string_upto_including(brand_html_code, ".php")

                phone_url = source_home_page_url + "/" + base_url_addition

                # get brand page source html
                phone_html_code = str(urllib.request.urlopen(phone_url).read())  # open("s20_fe_5g.txt", "r").read()

                nono_phones = ["samsung_galaxy_view",
                               "pad", "gear", "tab", "watch"]
                ok_phone = True

                if any(x in phone_url for x in nono_phones):
                    ok_phone = False

                # if it is an actual phone and not some other device
                if ok_phone:

                    #
                    #  now get data from phone html page and do what needed with it
                    #
                    model = ""
                    img_url = ""
                    db_phone_url = ""
                    battery_life = 0
                    price = 0
                    year = 0
                    dxo_score = 0
                    screen_size = 0
                    nfc_presence = False
                    jack_presence = False
                    dual_sim_presence = False
                    ir_presence = False

                    # retrieve model name

                    out = cut_string_from(phone_html_code, "modelname\">")
                    if out != "-1":
                        model = phone_html_code = out

                        out = cut_string_upto(model, "</h1>")
                        if out != "-1":
                            model = out
                            model = model.replace("'", "")
                            model = model.replace("\"", "")

                    # Get Antutu page url
                    antutu = new_antutu = get_antutu_score(model)

                    if model == "":
                        break

                    found = False
                    found_id = -1
                    for phone in new_phones:
                        found_id += 1
                        if model == phone["devicename"]:
                            found = True
                            new_img_url = phone["ImageURL"]
                            new_phone_url = phone["phoneURL"]
                            new_battery_life = phone["batterylife"]
                            new_price = phone["price"]
                            new_year = phone["year"]
                            new_dxo_score = phone["dxomarkScore"]
                            new_screen_size = phone["screensize"]
                            new_nfc_presence = phone["nfc"]
                            new_jack_presence = phone["headphonejack"]
                            new_dual_sim_presence = phone["dualsim"]
                            new_ir_presence = phone["ir"]
                            new_antutu = phone["antutu"]
                            break
                    # TODO: iterate over json file to find phone if already present and retrieve its info values
                    # TODO: set found to True when found

                    # gather the remaining data and add phone to database
                    if not found:

                        # price can be tricky cause its not always in the same location in relation to the others
                        price_html = phone_html_code

                        # retrieve image URL
                        out = get_image_url(phone_html_code)
                        if out != "-1":
                            img_url = out

                        # retrieve release year

                        out = cut_string_upto(
                            cut_string_from(phone_html_code,
                                            "released-hl"),
                            ",")
                        if out != "-1":
                            year_html = out
                            year = get_int_from_string(year_html)

                        # retrieve display size

                        out = cut_string_upto(
                            cut_string_from(phone_html_code,
                                            "displaysize-hl"),
                            "span")
                        if out != "-1":
                            screen_size_html = out
                            screen_size = get_float_from_string(screen_size_html)

                        # check if Dual SIM
                        # always true if in page in general
                        dual_sim_presence = False if phone_html_code.find(
                            "Dual SIM") == -1 else True

                        # check Infrared port presence
                        # always true if in page in general
                        ir_presence = False if phone_html_code.find(
                            "Infrared port") == -1 else True

                        # check 3.5mm jack presence
                        if phone_html_code.find("3.5mm jack</a>") != -1:
                            out = cut_string_upto(
                                cut_string_from(
                                    cut_string_from(phone_html_code,
                                                    "3.5mm jack</a>"),
                                    "nfo"),
                                "</td>")
                            if out != "-1":
                                headphone_jack_html = out

                                matches = ["yes", "YES", "Yes"]
                                if any(x in headphone_jack_html for x in matches):
                                    jack_presence = True

                        # check NFC presence

                        out = cut_string_upto(
                            cut_string_from(
                                phone_html_code,
                                "data-spec=\"nfc\""),
                            "</td>")
                        if out != "-1":
                            nfc_html = out

                            matches = ["yes", "YES", "Yes"]
                            if any(x in nfc_html for x in matches):
                                nfc_presence = True

                        # retrieve battery life

                        out = cut_string_upto(
                            cut_string_from(
                                phone_html_code,
                                "Endurance rating:"),
                            "h")
                        if out != "-1":
                            battery_life_html = out
                            battery_life = get_int_from_string(battery_life_html)

                        # retrieve price
                        currency = "EUR"
                        out = cut_string_from(phone_html_code, "Price")
                        if out != "-1":
                            price_html = out

                            end_index2 = price_html.find("EUR")
                            if end_index2 == -1:
                                end_index2 = price_html.find("USD")
                                currency = "USD"

                            if end_index2 != -1:

                                price_html = price_html[:end_index2]
                                price = get_float_from_string(price_html)
                                # calculate Israeli Shekel
                                if currency == "EUR":
                                    price = int(price / eur_to_usd)
                                    # price = (int)(price * EUR_to_ILS)

                        # ##########################ADD new device to DB##########################
                        too_old = year <= (datetime.datetime.now().year - 3)
                        if not too_old:
                            device = {
                                "Id": len(new_phones),
                                "devicename": model,
                                "batterylife": battery_life,
                                "price": price,
                                "BasemarkX": 0,
                                "year": year,
                                "ImageURL": img_url,
                                "screensize": screen_size,
                                "phoneURL": phone_url,
                                "nfc": nfc_presence,
                                "headphonejack": jack_presence,
                                "dualsim": dual_sim_presence,
                                "ir": ir_presence,
                                "dxomarkScore": 0,
                                "antutu": antutu
                            }
                            new_phones.append(device)
                            with open('newphones.json', 'w') as outfile:
                                json.dump(new_phones, outfile)
                            phones_added += 1

                    # there is a phone, check for an different data
                    else:
                        # initialize to false
                        btr_update = bench_update = y_update = prc_update = screen_update = img_url_update = \
                            p_url_update = ds_update = nfc_update = ir_update = jack_update = False

                        price_html = phone_html_code

                        # check if Dual SIM

                        start_index2 = phone_html_code.find("Dual SIM")
                        if start_index2 != -1:
                            dual_sim_turned_true = not dual_sim_presence
                            if dual_sim_turned_true:
                                new_dual_sim_presence = True
                                ds_update = True

                        # check Infrared port presence
                        nfc_html = cut_string_upto(
                            cut_string_from(
                                cut_string_from(phone_html_code, "Infrared port"),
                                "nfo"),
                            "</td>")
                        if nfc_html != "-1":
                            matches = ["yes", "YES", "Yes"]
                            if any(x in nfc_html for x in matches):
                                ir_turned_true = not ir_presence
                                if ir_turned_true:
                                    new_ir_presence = True
                                    ir_update = True

                        # retrieve image URL
                        phone_html_code = cut_string_from(phone_html_code, "specs-photo-main")
                        if phone_html_code != "-1":
                            index_str = "src=\""

                            start_index2 = min(phone_html_code.find(
                                index_str), phone_html_code.find("src="))
                            if start_index2 == phone_html_code.find("src="):
                                index_str = "src="
                            if start_index2 != -1:
                                phone_html_code = phone_html_code[start_index2 +
                                                                  len(index_str):]
                                out = cut_string_upto_including(phone_html_code, ".jpg")
                                if out != "-1":
                                    new_img_url = out
                                    if new_img_url != img_url:
                                        new_img_url = new_img_url
                                        img_url_update = True

                        # retrieve release year
                        year_html = cut_string_upto(
                            cut_string_from(phone_html_code,
                                            "released-hl"),
                            ",")
                        if year_html != "-1":
                            # if the spec actually changed then apply the change
                            if get_int_from_string(year_html) != year:
                                new_year = get_int_from_string(year_html)
                                y_update = True

                        # retrieve display size

                        screen_size_html = cut_string_upto(
                            cut_string_from(phone_html_code,
                                            "displaysize-hl"),
                            "span")
                        if screen_size_html != "-1":
                            new_screen_size = get_float_from_string(screen_size_html)
                            if new_screen_size != screen_size:
                                screen_update = True

                        # check 3.5mm jack presence
                        headphone_jack_html = cut_string_upto(
                            cut_string_from(
                                cut_string_from(phone_html_code, "3.5mm jack"),
                                "nfo"),
                            "span")
                        if headphone_jack_html != "-1":
                            if headphone_jack_html.find("Yes") != -1:
                                if not jack_presence:
                                    new_jack_presence = True
                                    jack_update = True
                            elif headphone_jack_html.find("No") != -1:
                                if jack_presence:
                                    new_jack_presence = False
                                    jack_update = True

                        # check NFC presence
                        nfc_html = cut_string_upto(
                            cut_string_from(phone_html_code,
                                            "data-spec=\"nfc\""),
                            "</td>")
                        if nfc_html != "-1":
                            if nfc_html.find("yes") != -1 or nfc_html.find("Yes") != -1:
                                if not nfc_presence:
                                    new_nfc_presence = True
                                    nfc_update = True
                            elif nfc_html.find("no") != -1 or nfc_html.find("No") != -1:
                                if nfc_presence:
                                    new_nfc_presence = False
                                    nfc_update = True

                        # retrieve battery life
                        battery_life_html = cut_string_upto(
                            cut_string_from(phone_html_code,
                                            "Endurance rating"),
                            "h<")
                        if battery_life_html != "-1":
                            # if the spec actually changed then apply the change
                            if battery_life != int(battery_life_html):
                                new_battery_life = int(battery_life_html)
                                btr_update = True

                        # retrieve price
                        price_html = cut_string_upto(
                            cut_string_from(
                                cut_string_from(
                                    cut_string_from(
                                        cut_string_from(price_html,
                                                        "Price"),
                                        "price"),
                                    "<a href"),
                                "\">"),
                            "</a")
                        if price_html != "-1":
                            price_html = price_html.split('/')[0]
                            currency = "EUR"
                            end_index2 = price_html.find(currency)
                            if end_index2 == -1:
                                currency = "USD"
                                end_index2 = price_html.find(currency)  # € $
                            if end_index2 == -1:
                                currency = "&#8364;"  # €
                                end_index2 = price_html.find(currency)  # € $
                            if end_index2 == -1:
                                currency = "&#36;"  # $
                                end_index2 = price_html.find(currency)  # € $

                            if end_index2 != -1:
                                if currency == "&#8364;" or currency == "&#36;":
                                    temp_start_index = price_html.rfind(';')
                                    price_html = price_html[temp_start_index:]
                                else:
                                    price_html = price_html[:end_index2]

                                new_price = get_int_from_string(price_html)
                                # calculate USD from EURO
                                if currency == "EUR" or currency == "&#8364;":
                                    new_price = int(new_price * eur_to_usd)
                                # if the spec actually changed then apply the change
                                if price != new_price:
                                    prc_update = True

                        # phoneURL out of date
                        if new_phone_url != phone_url:
                            p_url_update = True

                        ##########################UPDATE phone######################################

                        there_is_new_data = bench_update or y_update or btr_update or prc_update or screen_update or \
                                            img_url_update or p_url_update or ds_update or ir_update or nfc_update or \
                                            jack_update or antutu != new_antutu and new_antutu != 0

                        if there_is_new_data:  # preform an update only if some value has been updated
                            # TODO: set new parameters in file
                            device = {
                                "Id": len(new_phones),
                                "devicename": model,
                                "batterylife": new_battery_life,
                                "price": new_price,
                                "BasemarkX": 0,
                                "year": new_year,
                                "ImageURL": new_img_url,
                                "screensize": new_screen_size,
                                "phoneURL": new_phone_url,
                                "nfc": new_nfc_presence,
                                "headphonejack": new_jack_presence,
                                "dualsim": new_dual_sim_presence,
                                "ir": new_ir_presence,
                                "dxomarkScore": new_dxo_score,
                                "antutu": new_antutu
                            }
                            new_phones[found_id] = device
                            with open('newphones.json', 'w') as outfile:
                                json.dump(new_phones, outfile)
                            phones_updated += 1

            # ###################################################################################flip to the next page
            no_next_page_button = brand_html_code.find("pages-next") == -1
            next_page_selection_is_disabled = brand_html_code.find(
                "disabled pages-next") != -1
            no_next_page = no_next_page_button or next_page_selection_is_disabled
            if no_next_page:

                current_page = page_limit

            else:

                current_page += 1

            in_page_range = current_page < page_limit
            next_page_exists = brand_html_code.find("pages-next") != -1

            if in_page_range and next_page_exists:
                brand_html_code = cut_string_from(cut_string_from(brand_html_code, "pages-next"), "pages-next")
                brand_html_code = get_brand_next_page_html(
                    brand_html_code, href_keyword, source_home_page_url)

            href_keyword = "href=\""

    output = "Out of " + str(phones) + " gone through, " + str(phones_added) + \
             " new phones were added and " + str(phones_updated) + " phones were updated"
    print(output)


def get_image_url(phone_html_code):
    out = cut_string_from(phone_html_code, "specs-photo-main")
    if out != "-1":
        phone_html_code = out
        index_str = "src=\""
        start_index2 = min(phone_html_code.find(
            index_str), phone_html_code.find("src="))
        if start_index2 == phone_html_code.find("src="):
            index_str = "src="
        if start_index2 != -1:
            phone_html_code = phone_html_code[start_index2 + len(
                index_str):]
            img_url = phone_html_code
            return cut_string_upto_including(img_url, ".jpg")
    return "-1"


def cut_string_from(full_string, start_str):
    if full_string == "-1":
        return "-1"
    start_index = full_string.find(start_str)
    if start_index != -1:
        return full_string[start_index + len(start_str):]
    return "-1"


def cut_string_upto(full_string, end_str):
    if full_string == "-1":
        return "-1"
    end_index = full_string.find(end_str)
    if end_str != -1:
        return full_string[:end_index]
    return "-1"


def cut_string_upto_including(full_string, end_str):
    if full_string == "-1":
        return "-1"
    end_index = full_string.find(end_str)
    if end_str != -1:
        return full_string[:end_index + len(end_str)]
    return "-1"


def get_int_from_string(string):
    return int(re.findall(r'\d+', string)[0])


def get_float_from_string(string):
    return float(re.findall(r'\d+\.?\d+', string)[0])


def get_brand_next_page_html(brand_html_code, href_keyword, source_home_page_url):
    # remove everything up to the start of the link
    out = cut_string_from(brand_html_code, href_keyword)
    if out != "-1":
        brand_html_code = out

        link_end_keyword = ".php\""
        # search for href link of brand
        link_end_index = brand_html_code.find(link_end_keyword)
        if link_end_index != -1:

            # remove everything after the link addition
            link_addition = brand_html_code[:link_end_index + len(link_end_keyword) - 1]

            brands_next_page_url = source_home_page_url + "/" + link_addition
            # get brand next page source html
            brand_html_code = str(urllib.request.urlopen(brands_next_page_url).read())

            start_keyword = "review-body"
            # get phones html code
            brand_phones_start = brand_html_code.find(
                start_keyword)
            if brand_phones_start != -1:
                brand_html_code = brand_html_code[:brand_phones_start + 63]
                return brand_html_code
    return ""


def get_dxomark_scores():
    # get source home page html
    source_home_page_url = "https://www.dxomark.com#category#smartphone-reviews"

    html_code = str(urllib.request.urlopen(source_home_page_url).read())

    area_start = "rankingList"
    start_index = html_code.find(area_start)
    html_code = html_code[start_index + len(area_start):]
    area_start = "listElement"
    start_index = html_code.find(area_start)
    html_code = html_code[start_index + len(area_start):]
    for i in range(50):  # go over phones
        # #################################GET DATA##################################
        # get next score
        score_str = "<div class=\"deviceScore\">"
        start_index = html_code.find(score_str)
        html_code = html_code[start_index + len(score_str):]
        score_end = "<#div>"
        end_index = html_code.find(score_end)
        score_html = html_code[:end_index]
        score = re.findall(r'\d+', score_html)[0]
        print(score)
        # get phone name
        name_str = "deviceName"
        start_index = html_code.find(name_str)
        html_code = html_code[start_index + len(score_str):]
        name_str = "title=\""
        start_index = html_code.find(name_str)
        html_code = html_code[start_index + len(name_str):]
        name_end = "\""
        end_index = html_code.find(name_end)
        name_html = html_code[:end_index]
        device_name = name_html
        # UPDATE PHONE#################################
        print(device_name)


def get_antutu_score(model):
    kimovil_antutu_url = "https://www.kimovil.com/en/where-to-buy"
    # Get Antutu page url
    model = model.replace("+", " plus")
    model_antutu_url = model
    model_antutu_url = model_antutu_url.replace(" ", "-")
    model_antutu_url = model_antutu_url.lower()
    phone_antutu_url = kimovil_antutu_url + "-" + model_antutu_url

    # get phones antutu page source HTML
    downloaded = True

    phone_antutu_html_code = requests.get(phone_antutu_url).text
    page_not_found = phone_antutu_html_code.find("Page not found") != -1
    if page_not_found:
        # try to remove model name last part cause it might be model code which is not specified in kimovil's URL
        name_parts = model_antutu_url.split('-')

        if len(name_parts) > 2:
            model_antutu_url = ""
            for i in range(len(name_parts) - 2):
                model_antutu_url += name_parts[i] + "-"
            model_antutu_url += name_parts[len(name_parts) - 2]
            phone_antutu_url_revised = kimovil_antutu_url + "-" + model_antutu_url

            phone_antutu_html_code = requests.get(phone_antutu_url_revised).text
            page_not_found = phone_antutu_html_code.find("Page not found") != -1
            if page_not_found:
                downloaded = False

    if downloaded:

        out = cut_string_upto(
            cut_string_from(
                cut_string_from(
                    phone_antutu_html_code, "item item-antutu"),
                "spec main"),
            "</li>")
        if out != "-1":
            antutu_html = get_float_from_string(out)

            new_antutu = int(float(antutu_html) * 1000)
            return new_antutu

    return 0


def update_existing_phones_antutu_scores():
    with open('revisedphones.json') as phones_json_file:
        phones_loaded = json.load(phones_json_file)

    i = 0
    updates_phones = 0
    for device in phones_loaded:
        antutu_score = get_antutu_score(device["devicename"])
        if antutu_score != int(device["antutu"]) and antutu_score:
            phones_loaded[i]["antutu"] = antutu_score
            updates_phones += 1
            with open('revisedphones.json', 'w') as outfile:
                json.dump(phones_loaded, outfile)
        time.sleep(random.randint(0, 3))
        i += 1
        print("phone: " + str(i) + " updates_phones: " + str(updates_phones))


def get_exchange_rate():
    # ###########################################GET DAILY EXCHANGE#####################################################
    euro_bank_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    bank_html = requests.get(euro_bank_url).text

    # get EUR to USD
    out = cut_string_from(bank_html, "USD")
    out = cut_string_upto(out, ">")
    eur_to_usd = get_float_from_string(out)

    # # get EUR to ILS
    # out = cut_string_from(bank_html, "ILS")
    # bank_html = cut_string_upto(out, ">")
    # eur_to_ils = get_float_from_string(bank_html)

    return eur_to_usd


def main():
    scrape_phones()
    # print(get_antutu_score("huawei-p40-pro"))
    print('')


main()

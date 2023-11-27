import requests
from bs4 import BeautifulSoup
import csv


def get_all_plane_urls_for_nation(nation):
    nation_aircraft_url = f'https://wiki.warthunder.com/Category:{nation}_aircraft'
    all_plane_urls_for_nation = []

    try:
        page = requests.get(nation_aircraft_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        div_mw_category = soup.find('div', class_='mw-category')

        if div_mw_category:
            li_tags = div_mw_category.find_all('li')
            for li in li_tags:
                a_tag = li.find('a')
                if a_tag:
                    plane_relative_url = a_tag['href']
                    base_url = 'https://wiki.warthunder.com'
                    all_plane_urls_for_nation.append(
                        base_url + plane_relative_url)

    except Exception as e:
        print(f"Failed to get plane URLs for {nation}: {e}")

    return all_plane_urls_for_nation


def get_urls_all_planes_all_nations():
    nations = ['USA', 'Germany', 'USSR', 'Britain', 'Japan',
               'China', 'Italy', 'France', 'Sweden', 'Israel']
    all_planes = []

    for nation in nations:
        all_planes_from_single_nation = get_all_plane_urls_for_nation(nation)
        all_planes.extend(all_planes_from_single_nation)

    return all_planes


def scrape_single_plane(single_plane_url):
    try:
        page = requests.get(single_plane_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        plane_name = soup.find('div', class_='general_info_name').text
        nation = soup.find(
            'div', class_='general_info_nation').find_all('a')[1].text
        rank = soup.find('div', class_='general_info_rank').find(
            'a').text.split()[0]

        div_general_info_br = soup.find('div', class_='general_info_br')
        table_row = div_general_info_br.find_all('tr')[1]
        battle_rating = table_row.find_all('td')[1].text

        wikitables = soup.find_all('table', class_='wikitable')
        wikitable_one = wikitables[0]
        fourth_row = wikitable_one.find_all('tr')[3]
        data_cells = fourth_row.find_all('td')
        max_speed = data_cells[1].text.strip()
        turn_time = data_cells[3].text.strip()
        climb_rate = data_cells[5].text.strip()
        wikitable_two = wikitables[2]
        fourth_row = wikitable_two.find_all('tr')[3]
        data_cells = fourth_row.find_all('td')
        wing_rip_speed = data_cells[0].text.strip()
        combat_flap_rip_speed = data_cells[2].text.strip()

        garage_image = soup.find('img', alt=lambda x: x and 'GarageImage' in x)
        image_url = None

        if garage_image:
            base_url = "https://wiki.warthunder.com"
            relative_url = garage_image.get('src')
            image_url = base_url + relative_url
            print("Found url")
        else:
            print("Image with 'GarageImage' in alt attribute not found on the page.")

        return [plane_name, nation, rank, battle_rating, max_speed, turn_time, climb_rate,
                wing_rip_speed, combat_flap_rip_speed, image_url]

    except Exception as e:
        print(f"Failed to scrape data for {single_plane_url}: {e}")
        return None


def scrape_and_save_csv(list_of_plane_urls, filename):
    print(f'Total number of planes to scrape: {len(list_of_plane_urls)}')

    failed_scrape_urls = []

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header_row = ['plane_name', 'nation', 'rank', 'battle_rating', 'max_speed',
                      'turn_time', 'climb_rate', 'wing_rip_speed', 'combat_flap_rip_speed', 'image_url']
        csv_writer.writerow(header_row)

        for count, url in enumerate(list_of_plane_urls, start=1):

            print(f"{count} Scraping: {url}")

            try:
                row_data = scrape_single_plane(url)

                if row_data:
                    csv_writer.writerow(row_data)
                else:
                    failed_scrape_urls.append(url)

            except Exception as e:
                print(f"Scrape failed for {url}: {e}")
                failed_scrape_urls.append(url)

    print('Scraping completed!')
    print(f"{len(failed_scrape_urls)} plane URLs failed to scrape. See list above.")


if __name__ == "__main__":
    name_file = 'raw-data.csv'
    all_planes_all_nations = get_urls_all_planes_all_nations()
    scrape_and_save_csv(all_planes_all_nations, name_file)

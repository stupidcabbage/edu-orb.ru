import requests
from bs4 import BeautifulSoup
from diary.db.models.users import ParcipiantsID

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

a = requests.get("https://de.edu.orb.ru/edv/index/participant", cookies={"PHPSESSID": f"624bb6f266a41bfe9a3a7394643e9610"}, headers=HEADERS)

# print(a.text)
soup = BeautifulSoup(a.text, "html.parser")


def replace_empty_symbols(string: str):
    return string.replace('\n', '').replace('  ', '')


# def get_participants(soup):
# 	if soup.find_all('ul', id='participants'):
# 		spisok_a = soup.find_all('ul', id='participants')[0].find_all('a')
# 		participants=[]
# 		for participant_html in spisok_a:
# 			guid = participant_html.get('data-guid')
# 			name = participant_html.find_all('div')[0].text
# 			OO = participant_html.find_all('div')[1].text
#
# 			participants.append({'guid': guid,
# 								'name': replace_empty_symbols(name),
# 								'class': replace_empty_symbols(OO.split(',')[0]),
# 								'school': replace_empty_symbols(OO.split(',')[1])})
# 		return participants
# 	else:
# 		participants=[]
# 		spisok_a = soup.find_all('div', 'one-participant')
# 		name = spisok_a[0]
# 		classs = spisok_a[1]
# 		additional=''
# 		school=spisok_a[2]
# 		guid = soup.find_all('div', id='participant')[0]['data-guid']
# 		participants.append({'guid':guid,
# 							'name':name.replace('\n', '').replace('  ', ''),
# 							'class':classs.replace('\n', '').replace('  ', ''),
# 							'school':school.replace('\n', '').replace('  ', ''),
# 							'additional':additional})
#
# 		return participants

def _make_parcipiant_model(user_id: int, parcipiant_id: str,
                           name: str, grade: str, school: str) -> ParcipiantsID:
    return ParcipiantsID(user_id=user_id,
              parcipiant_id=parcipiant_id,
              name=replace_empty_symbols(name),
              grade=replace_empty_symbols(grade),
              school=replace_empty_symbols(school))


def _find_raw_parcipiants_id(soup) -> list:
    return soup.find('ul', id='participants').find_all('a')


def _find_raw_parcipiant_id(soup) -> list:
    return soup.find('div', 'one-participant').text.split(',')


def get_parcipiants():
    a = requests.get("https://archive2021.edu.orb.ru/edv/index/participant",
                     cookies={"PHPSESSID": f"2f929b31652717e963da453a7ef9575"},
                     headers=HEADERS)

    soup = BeautifulSoup(a.text, "html.parser")
    participants=[]

    if soup.find_all('ul', id='participants'):
        raw_parcipiants_id = _find_raw_parcipiants_id(soup)
        for participant_html in raw_parcipiants_id:
            parcipiant_id = participant_html.get('data-guid')
            name = participant_html.find('div').text
            grade, school = participant_html.find_all('div')[1].text.split(",")

            participants.append(_make_parcipiant_model(123, parcipiant_id,
                                                       name, grade, school))
        return participants

    raw_parcipiants_id = _find_raw_parcipiant_id(soup)
    parcipiant_id = soup.find('div', id='participant').get('data-guid')
    name, grade, school = raw_parcipiants_id
    participants.append(_make_parcipiant_model(123, parcipiant_id,
                                               name, grade, school))

    return participants

print(get_parcipiants())


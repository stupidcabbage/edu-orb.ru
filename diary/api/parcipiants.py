import aiohttp
from bs4 import BeautifulSoup

from diary.db.models.users import ParcipiantsID, User

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}


async def get_parcipiants(user: User):
    cookies = {"PHPSESSID": f"{user.phpsessid}"}
    async with aiohttp.ClientSession(headers=HEADERS, 
                                     cookies=cookies) as s:
        response = await s.get("https://de.edu.orb.ru/edv/index/participant")
        page_text = await response.text()

    soup = BeautifulSoup(page_text, "html.parser")
    participants=[]

    if soup.find_all('ul', id='participants'):
        raw_parcipiants_id = _find_raw_parcipiants_id(soup)
        for participant_html in raw_parcipiants_id:
            parcipiant_id = participant_html.get('data-guid')
            name = participant_html.find('div').text
            grade, school = participant_html.find_all('div')[1].text.split(",")

            participants.append(_make_parcipiant_model(user.telegram_id, parcipiant_id,
                                                       name, grade, school,
                                                       False))
        return participants

    raw_parcipiants_id = _find_raw_parcipiant_id(soup)
    parcipiant_id = soup.find('div', id='participant').get('data-guid')
    name, grade, school = raw_parcipiants_id
    participants.append(_make_parcipiant_model(user.telegram_id, parcipiant_id,
                                               name, grade, school))

    return participants


def _make_parcipiant_model(user_id: int, parcipiant_id: str,
                           name: str, grade: str, school: str,
                           is_current: bool = True) -> ParcipiantsID:
    return ParcipiantsID(user_id=user_id,
              parcipiant_id=parcipiant_id,
              name=replace_empty_symbols(name),
              grade=replace_empty_symbols(grade),
              school=replace_empty_symbols(school),
              is_current=is_current)


def _find_raw_parcipiants_id(soup) -> list:
    return soup.find('ul', id='participants').find_all('a')


def _find_raw_parcipiant_id(soup) -> list:
    return soup.find('div', 'one-participant').text.split(',')


def replace_empty_symbols(string: str):
    return string.replace('\n', '').replace('  ', '')

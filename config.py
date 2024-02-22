from dataclasses import dataclass

from environs import Env


internal_links = {
    'Интернет-магазины и IT': '/internet-magazin',
    'Общественное питание': '/obschestvennoe_pitanie',
    'Производство': '/proizvodstvo',
    'Развлечения': '/razvlecheniya',
    'Сельское хозяйство': '/selskoe_hozyaystvo',
    'Строительство': '/stroitelstvo',
    'Сфера услуг': '/sfera_uslug',
    'Магазины и пункты выдачи заказов': '/torgovlya',
    'Автобизнес': '/avtomobilnyi_biznes',
    'Красота и уход': '/krasota_i_ukhod',
    'Стоматология и медицина': '/zdorove_i_medicina',
    'Туризм': '/gostinicy_i_bazy_otdykha',
    'Другое': '/drugoe'
}


@dataclass
class Hidden:
    link: str
    tablename: str
    start_page: int
    pages: int
    db_username: str
    db_password: str
    db_local_port: int
    db_name: str
    db_echo: bool


def load_hidden_vars(path: str):
    env = Env()
    env.read_env()

    return Hidden(
        link=env.str("LINK"),
        tablename=env.str("TABLENAME"),
        start_page=env.int("START_PAGE"),
        pages=env.int("PAGES"),
        db_username=env.str("DB_USERNAME"),
        db_password=env.str("DB_PASSWORD"),
        db_local_port=env.int("DB_LOCAL_PORT"),
        db_name=env.str("DB_NAME"),
        db_echo=env.bool("DB_ECHO")
    )


hidden = load_hidden_vars(path='.env')

russia = [
    'https://www.avito.ru/moskva_i_mo/gotoviy_biznes',
    'https://www.avito.ru/sankt_peterburg_i_lo/gotoviy_biznes',
    'https://www.avito.ru/adygeya/gotoviy_biznes',
    'https://www.avito.ru/altayskiy_kray/gotoviy_biznes',
    'https://www.avito.ru/bashkortostan/gotoviy_biznes',
    'https://www.avito.ru/buryatiya/gotoviy_biznes',
    'https://www.avito.ru/dagestan/gotoviy_biznes',
    'https://www.avito.ru/donetsk/gotoviy_biznes',
    'https://www.avito.ru/ingushetiya/gotoviy_biznes',
]

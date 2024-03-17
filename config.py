from dataclasses import dataclass

from environs import Env

category_dict = {
    'internet_magazin': 'Интернет-магазины и IT',
    'obschestvennoe_pitanie': 'Общественное питание',
    'proizvodstvo': 'Производство',
    'razvlecheniya': 'Развлечения',
    'selskoe_hozyaystvo': 'Сельское хозяйство',
    'stroitelstvo': 'Строительство',
    'sfera_uslug': 'Сфера услуг',
    'torgovlya': 'Магазины и пункты выдачи заказов',
    'avtomobilnyi_biznes': 'Автобизнес',
    'krasota_i_ukhod': 'Красота и уход',
    'zdorove_i_medicina': 'Стоматология и медицина',
    'gostinicy_i_bazy_otdykha': 'Туризм',
    'drugoe': 'Другое',
    'franshizy': 'Франшизы'
}


@dataclass
class Hidden:
    # link: str
    delay: float
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
        # link=env.str("LINK"),
        delay=env.float("DELAY"),
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

russia_eng = [
    'moskva_i_mo',
    'sankt_peterburg_i_lo',
    'adygeya',
    'altayskiy_kray',
    'bashkortostan',
    'buryatiya',
    'dagestan',
    'donetsk',
    'ingushetiya',
    'kabardino-balkariya',
    'kalmykiya',
    'karachaevo-cherkesiya',
    'kareliya',
    'kherson',
    'komi',
    'respublika_krym',
    'lugansk',
    'mariy_el',
    'mordoviya',
    'saha_yakutiya',
    'severnaya_osetiya',
    'tatarstan',
    'tyva',
    'udmurtiya',
    'hakasiya',
    'chechenskaya_respublika',
    'zabaykalskiy_kray',
    'kamchatskiy_kray',
    'krasnodarskiy_kray',
    'permskiy_kray',
    'primorskiy_kray',
    'stavropolskiy_kray',
    'habarovskiy_kray',
    'amurskaya_oblast',
    'arhangelskaya_oblast',
    'astrahanskaya_oblast',
    'belgorodskaya_oblast',
    'bryanskaya_oblast',
    'vladimirskaya_oblast',
    'volgogradskaya_oblast',
    'vologodskaya_oblast',
    'voronezhskaya_oblast',
    'ivanovskaya_oblast',
    'irkutskaya_oblast',
    'kaliningradskaya_oblast',
    'kaluzhskaya_oblast',
    'kemerovskaya_oblast',
    'kirovskaya_oblast',
    'kostromskaya_oblast',
    'kurganskaya_oblast',
    'kurskaya_oblast',
    'lipetskaya_oblast',
    'magadanskaya_oblast',
    'murmanskaya_oblast',
    'nizhegorodskaya_oblast',
    'novgorodskaya_oblast',
    'novosibirskaya_oblast',
    'omskaya_oblast',
    'orenburgskaya_oblast',
    'orlovskaya_oblast',
    'penzenskaya_oblast',
    'pskovskaya_oblast',
    'rostovskaya_oblast',
    'ryazanskaya_oblast',
    'samarskaya_oblast',
    'saratovskaya_oblast',
    'sahalinskaya_oblast',
    'sverdlovskaya_oblast',
    'smolenskaya_oblast',
    'tambovskaya_oblast',
    'tverskaya_oblast',
    'tomskaya_oblast',
    'tulskaya_oblast',
    'tyumenskaya_oblast',
    'ulyanovskaya_oblast',
    'chelyabinskaya_oblast',
    'yaroslavskaya_oblast',
    'sevastopol',
    'evreyskaya_ao',
    'nenetskiy_ao',
    'hanty-mansiyskiy_ao',
    'chukotskiy_ao',
    'yamalo-nenetskiy_ao',
]

russia_rus = [
    'Москва и МО',
    'Санкт-Петербург и ЛО',
    'Республика Адыгея',
    'Алтайский край',
    'Республика Башкортостан',
    'Республика Бурятия',
    'Республика Дагестан',
    'Донецк (Донецкая область)',
    'Республика Ингушетия',
    'Республика Кабардино-Балкария',
    'Республика Калмыкия',
    'Республика Карачаево-Черкесия',
    'Республика Карелия',
    'Херсон',
    'коми',
    'Республика Крым',
    'Луганск',
    'марий эл',
    'мордовия',


]

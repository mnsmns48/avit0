import time

from translate import Translator
from seleniumbase import SB


# url = 'https://whoer.net'
# proxy = "185.238.228.48:80"
#
# if __name__ == "__main__":
#     with SB(uc=True,
#             browser='chrome',
#             headed=True,
#             page_load_strategy='eager',
#             block_images=True,
#             proxy=proxy) as driver:
#         driver.get(url)
#         time.sleep(60)
#
#
stt = 'nizhniy_novgorod'
translator = Translator(from_lang='en', to_lang='ru')
g = ' '.join(stt.split('_'))
print(g)
ru_text = translator.translate(g)
print(ru_text)
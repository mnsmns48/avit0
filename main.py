from DB.crud import out_excel
from DB.engine import sync_db
from DB.models import Base, AvitoData
from logic import start_pars
from config import hidden

if __name__ == '__main__':
    Base.metadata.create_all(sync_db.engine)
    start_pars(url=hidden.link, pages=hidden.pages, output_print=False, db_rec=True)
    # out_excel()
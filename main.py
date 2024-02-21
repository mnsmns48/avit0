import random

from sqlalchemy.exc import OperationalError

from DB.crud import out_excel, create_db
from DB.engine import sync_db
from DB.models import Base
from config import hidden
from logic import start_pars

if __name__ == '__main__':
    try:
        Base.metadata.create_all(sync_db.engine)
    except OperationalError:
        create_db()
        Base.metadata.create_all(sync_db.engine)
    start_pars(
        link=hidden.url,
        start_page=hidden.start_page,
        pages=hidden.pages,
        output_print=False,
        db_rec=True,
        sleep_time=1
    )
    # out_excel()

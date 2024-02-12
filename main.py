import asyncio

from DB.engine import db
from DB.models import Base
from cls import Avito


async def main():
    async with db.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    start = Avito(url='https://www.avito.ru/permskiy_kray/gotoviy_biznes',
                  count=5,
                  items=['']
                  )
    await start.parse()


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        print('Script stopped')

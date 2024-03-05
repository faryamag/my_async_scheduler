import asyncio
from datetime import datetime, time


from sqlalchemy import ForeignKey, Time
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship, selectinload

DB = 'sqlite+aiosqlite:///db.sqlite3'

# Описание таблиц
class Base(AsyncAttrs, DeclarativeBase):
    pass

class Duty(Base):
    __tablename__ = "duty"

    duty_id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.author_id"))
    start_time: Mapped[str] = mapped_column(nullable=True)
    act: Mapped[str]
    obj: Mapped[str] = mapped_column(nullable=True)
    args: Mapped[str] = mapped_column(nullable=True)
    enabled: Mapped[bool] = mapped_column(default=False)
    excludes: Mapped[str] = mapped_column(nullable=True)
    is_working: Mapped[bool] = mapped_column(default=False)
    comment: Mapped[str] = mapped_column(default='')
    last_err: Mapped[str] = mapped_column(default='')




class Author(Base):
    __tablename__ = "author"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default='Anonumous', nullable=False, unique=True)
    tg_id: Mapped[int] = mapped_column(default=0)


# Конец описания таблиц

# Создание методов работы с таблицами

async def add_author(async_session: async_sessionmaker[AsyncSession], name, tg_id=0) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(Author(name=name, tg_id=tg_id))

        #    session.add_all([Author(name='Fairy', tg_id=777),
        #                    Author(name='Farya', tg_id=13)])


async def add_duty(async_session: async_sessionmaker[AsyncSession],
                   author_id=1, start_time="00:00:00", act='pass', **kwargs) -> None:
    async with async_session() as session:
        cells = {key:value for key, value in kwargs.items() if hasattr(Duty, key)}
        async with session.begin():
            session.add(Duty( author_id=author_id,
                             start_time=start_time,
                             act=act, **cells
                             ))


async def update_duty(async_session: async_sessionmaker[AsyncSession],
                      duty_id: int=1, **kwargs) -> None:
    async with async_session.begin() as session:
        query = await session.execute(select(Duty).where(Duty.duty_id == duty_id))
        duty = query.scalar()
        atrs_to_change = {key: value for key, value in kwargs.items() if hasattr(duty, key)}
        for key, value in atrs_to_change.items():
            object.__setattr__(duty, key, value)
#        session.commit()


async def check_duty(async_session: async_sessionmaker[AsyncSession],
                   duty_id: int, cells) -> None:
    async with async_session.begin() as session:
        query = await session.execute(select(Duty).where(Duty.duty_id==duty_id))
        duty = query.scalar()
        cells_to_return = {key: duty.__dict__[key] for key in cells if hasattr(duty,key)}
        return cells_to_return


async def get_duty(async_session: async_sessionmaker[AsyncSession],
                   start_time: str, cells) -> None:
    async with async_session.begin() as session:
        query = await session.execute(select(Duty).where(Duty.start_time==start_time and Duty.is_working==False and Duty.enabled==True ))
        #duty = query.scalar()
        duties = query.scalars().all()
        #print('In func ', duties)
        cells_to_return = [{key: duty.__dict__[key] for key in cells if hasattr(duty,key)} for duty in duties]

        return cells_to_return


# Конец блока создания  методов работы с таблицами

async def operate_base(my_func, *args, **kwargs):
    engine = create_async_engine(DB)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # await add_author(async_session, name="Anonimous", tg_id=13)
    # await add_duty(async_session, author_id=1, start_time="20:30:01", act="test_func1", args="obj1")
    # await update_duty(async_session, duty_id=3, author_name='NoFar', system='OS', act='print', args="my_obj ased asdew", is_working=False, enabled=True)#, enabled=True)
    result = await my_func(async_session=async_session, *args, **kwargs)
    #print(result)
    # await my_func
    await engine.dispose()
    return result

async def init_base():
    engine = create_async_engine(DB)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session.begin() as session:

        query_author = await session.execute(select(Author))
        if not query_author.scalar():
            await add_author(async_session, name="Anonimous", tg_id=13)
            print("Created Anonimous author")

        query_duties = await session.execute(select(Duty))
        if not query_duties.scalar():
            await asyncio.gather(
                add_duty(async_session, author_id=1, start_time=datetime.now().strftime('%H:%M:%S'), act="test_func1", obj="test_obj", enabled=True),
                add_duty(async_session, author_id=1, start_time=datetime.now().strftime('%H:%M:%S'), act="print", obj="test_obj", enabled=True),
                add_duty(async_session, author_id=1, start_time='07:00:00', act="sunrise_hue", obj="KidsLamp1", args="duration_m=3 reversed=False", enabled=True),
                add_duty(async_session, author_id=1, start_time='08:00:00', act="lamp_off", obj="KidsLamp1", args="duration_m=3 reversed=False", enabled=True)
            )

    await engine.dispose()

#asyncio.run(operate_base(update_duty, duty_id=1, enabled=True, name='Farit', act='print', args="1234 sdcd ewcdsdc"))
#asyncio.run(init_base())
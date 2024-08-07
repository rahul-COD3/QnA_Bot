from sqlalchemy.future import select
from qna_bot.src.config.db import AsyncSessionLocal
from qna_bot.src.models.model import DataSource, DataSourceType, DataSpace, User, Bot

class SeedData:
    def __init__(self):
        self.db = None

    async def save_user(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def save_bot(self, bot: Bot):
        self.db.add(bot)
        await self.db.commit()
        await self.db.refresh(bot)

    async def seed(self):
        async with AsyncSessionLocal() as session:
            self.db = session

            # Check if user exists
            result = await self.db.execute(select(User))
            user = result.scalars().first()
            if not user:
                user = User(
                    name="John Doe",
                    email="john@gmail.com",
                    password="password"
                )
                await self.save_user(user)

            # Check if bot exists
            result = await self.db.execute(select(Bot))
            bot = result.scalars().first()
            if not bot:
                bot = Bot(
                    name="QnA Bot",
                    instruction="A question and answer bot",
                    created_by=user.id
                )
                await self.save_bot(bot)

            # check DataSpace exists
            result = await self.db.execute(select(DataSpace))
            data_space = result.scalars().first()
            if not data_space:
                data_space = DataSpace(
                    name="DataSpace",
                    description="A data space",
                    created_by=user.id
                )
                self.db.add(data_space)
                await self.db.commit()
                await self.db.refresh(data_space)

            # check DataSources exists
            result = await self.db.execute(select(DataSource))
            data_source = result.scalars().first()
            if not data_source:
                data_source = DataSource(
                    type=DataSourceType.DOCUMENT,
                    location="daefc74c-e48b-48a6-9ca9-0b076a1d215c_wallpaperflare.com_wallpaper.jpg",
                    data_space_id=data_space.id
                )
                self.db.add(data_source)
                await self.db.commit()
                await self.db.refresh(data_source)

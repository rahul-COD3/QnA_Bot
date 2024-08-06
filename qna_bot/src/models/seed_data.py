from sqlalchemy.future import select
from qna_bot.db import AsyncSessionLocal
from qna_bot.src.models.model import User, Bot
from sqlalchemy.ext.asyncio import AsyncSession

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

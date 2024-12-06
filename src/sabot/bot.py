import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router

from jira import pull_into_crap


load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("bot_token"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)


class TaskForm(StatesGroup):
    task = State()


@router.message(Command(commands=["task"]))
async def cmd_task(message: types.Message, state: FSMContext):
    await state.set_state(TaskForm.task)
    await message.reply("жги")


@router.message(Command(commands=["cancel"]))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Отменено")


@router.message(TaskForm.task)
async def process_task(message: types.Message, state: FSMContext):
    if "\n" in message.text:
        await message.reply(pull_into_crap(*message.text.split("\n", 1)))
        await state.clear()
    else:
        await message.reply("вот так надо: заголовок\\nописание")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

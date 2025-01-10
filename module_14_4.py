from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions

api = '7697264052:AAGNsVz1Elae-RB_ZRKtBl8aC9uGVAMwUUY'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
all_products = crud_functions.get_all_products()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text="Купить")
kb.row(button, button2)
kb.add(button3)

Inlane_menu = InlineKeyboardMarkup(resize_keyboard=True)
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
Inlane_menu.row(button4, button5)

prod_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Продукт1', callback_data="product_buying"),
            InlineKeyboardButton(text='Продукт2', callback_data="product_buying"),
            InlineKeyboardButton(text='Продукт3', callback_data="product_buying"),
            InlineKeyboardButton(text='Продукт4', callback_data="product_buying")
        ]
    ]
)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=Inlane_menu)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for id, title, description, price in all_products:
        await message.answer(f"Название: {title} | Описание: {description} | Цена: {price}")
        with open(f'foto/{id}.jpg', 'rb') as img:
            await message.answer_photo(img, parse_mode='HTML')
    await message.answer("Выберите продукт для покупки:", reply_markup=prod_menu)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг)  6,25 x рост (см) – 5 x возраст (г) – 161')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ваша норма калорий {10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161}")


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

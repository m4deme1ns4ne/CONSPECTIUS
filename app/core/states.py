from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    waiting_for_response = State()  # Состояние ожидания ответа от бота

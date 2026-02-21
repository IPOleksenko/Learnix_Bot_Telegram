from aiogram.fsm.state import StatesGroup, State

class StartMenuFSM(StatesGroup):
    waiting_for_course_title = State()
    waiting_for_course_to_continue = State()
    waiting_for_lesson_answer = State()
from aiogram import  Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from src.utils.forms import CreateTaskFSBForm
from src.database.database import local_session
from src.crud.tasks import TaskCrud
from datetime import datetime

task = Router()

@task.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    # клавиатуру вынести отдельно
    kb =[[types.InlineKeyboardButton(text="Посмотреть все задачи",callback_data="all_tasks")],
         [types.InlineKeyboardButton(text="Посмотреть невыполненные задачи",callback_data="not_completed_tasks")],
         [types.InlineKeyboardButton(text="Посмотреть выполненные задачи", callback_data="completed_tasks")],
         [types.InlineKeyboardButton(text="Создать задачу",callback_data="create_task")],
         [types.InlineKeyboardButton(text="Обновить статус", callback_data="completed_tasks")]
         ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(text="Привет,я бот. Выбери что нибудь",reply_markup=keyboard)

@task.callback_query(F.data == "all_tasks")
async def create_task(callback_query: types.CallbackQuery):
    try:
        async with local_session() as session:
            all_tasks = await TaskCrud.get_all(session=session)
            if all_tasks:
                for task in all_tasks:
                    await callback_query.message.answer(text=f"Новое задание для {task.executor}.\n"
                                                      f"Название: {task.name}.\n"
                                                      f"Описание: {task.description}.\n"
                                                      f"Срок: {task.term}.\n"
                                                      f"Активна:{task.is_active}"
                                                        )
    except Exception as e:
        await callback_query.message.answer(text=f"Что-то случилось: {str(e)}")



@task.callback_query(F.data == "create_task")
async def create_task(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(CreateTaskFSBForm.name)
        await callback_query.message.answer(text="Введите название")
    except Exception as e:
        await callback_query.message.answer(text=f"Что-то случилось: {str(e)}")

@task.message(CreateTaskFSBForm.name)
async def enter_name(message: types.Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        await state.set_state(CreateTaskFSBForm.description)
        await message.answer(text="Введите описание")
    except Exception as e:
        await message.answer(text=f"Что-то случилось: {str(e)}")

@task.message(CreateTaskFSBForm.description)
async def enter_description(message: types.Message, state: FSMContext):
    try:
        await state.update_data(description=message.text)
        await state.set_state(CreateTaskFSBForm.term)
        await message.answer(text="Введите срок (форма ввода: дд-мм-гггг)")
    except Exception as e:
        await message.answer(text=f"Что-то случилось: {str(e)}")

@task.message(CreateTaskFSBForm.term)
async def enter_term(message: types.Message, state: FSMContext):
    try:
        await state.update_data(term=message.text)
        await state.set_state(CreateTaskFSBForm.executor)
        await message.answer(text="Введите исполнителя")
    except Exception as e:
        await message.answer(text=f"Что-то случилось: {str(e)}")

@task.message(CreateTaskFSBForm.executor)
async def enter_executor(message: types.Message, state: FSMContext):
    try:
        await state.update_data(executor=message.text)
        data = await state.get_data()

        async with local_session() as session:
            new_task = await TaskCrud.create(session= session,
                                               name=data["name"],
                                               description=data["description"],
                                               term=datetime.strptime(data["term"],"%d-%m-%Y"),
                                               executor=data["executor"]
                                               )
            if new_task:
                    await message.answer(text=f"Новое задание для {new_task.executor}.\n"
                                                  f"Название: {new_task.name}.\n"
                                                  f"Описание: {new_task.description}.\n"
                                                  f"Срок: {new_task.term}.")

    except Exception as e:
        await message.answer(text=f"Что-то случилось: {str(e)}")
    finally:
        await state.clear()

@task.callback_query(F.data == "not_completed_tasks")
async def get_not_completed_tasks(callback_query: types.CallbackQuery):
    try:
        async with local_session() as session:
            all_tasks = await TaskCrud.get_filtered_by_param(session=session,is_active=True)
            if all_tasks:
                for task in all_tasks:
                    await callback_query.message.answer(text=f"Новое задание для {task.executor}.\n"
                                                      f"Название: {task.name}.\n"
                                                      f"Описание: {task.description}.\n"
                                                      f"Срок: {task.term}.\n"
                                                      f"Активна:{task.is_active}"
                                                        )
    except Exception as e:
        await callback_query.message.answer(text=f"Что-то случилось: {str(e)}")

@task.callback_query(F.data == "completed_tasks")
async def get_completed_tasks(callback_query: types.CallbackQuery):
    try:
        async with local_session() as session:
            all_tasks = await TaskCrud.get_filtered_by_param(session=session, is_active=False)
            if all_tasks:
                for task in all_tasks:
                    await callback_query.message.answer(text=f"Новое задание для {task.executor}.\n"
                                                             f"Название: {task.name}.\n"
                                                             f"Описание: {task.description}.\n"
                                                             f"Срок: {task.term}.\n"
                                                             f"Активна:{task.is_active}"
                                                        )
    except Exception as e:
        await callback_query.message.answer(text=f"Что-то случилось: {str(e)}")

@task.callback_query(F.data == "update_status")
async def update_task(message: types.Message):
    await message.answer(text="скоро будет")











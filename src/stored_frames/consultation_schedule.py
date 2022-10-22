import os
from datetime import datetime

import pandas as pd
import requests
from aiogram.types import ReplyKeyboardMarkup, ParseMode
from dotenv import load_dotenv

load_dotenv()


class ConsultationSchedule:
    dateUpdate = None
    schedule = None


def isTimeExpired():
    now = datetime.now()
    if ConsultationSchedule.dateUpdate is None:
        ConsultationSchedule.dateUpdate = now
        return True
    period = now - ConsultationSchedule.dateUpdate
    if period.days > 0:
        ConsultationSchedule.dateUpdate = now
        return True
    return False


def deletePreviousFileOnDisk():
    headers = {
        'Accept': 'application/json',
        'Authorization': 'OAuth ' + os.getenv('YANDEX_DISK_TOKEN'),
    }

    params = {
        'path': 'bot/consultation_schedule.xlsx',
    }

    response = requests.delete('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
    if response.status_code in [204, 404]:
        return True
    else:
        # ERROR Необходимо сделать обработку
        return False


def uploadFileOnDisk():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'OAuth ' + os.getenv('YANDEX_DISK_TOKEN'),
    }

    params = {
        'public_key': os.getenv('YANDEX_DISK_FILE'),
        'name': 'consultation_schedule.xlsx',
        'save_path': 'bot',
    }

    response = requests.post('https://cloud-api.yandex.net/v1/disk/public/resources/save-to-disk', params=params,
                             headers=headers)
    if response.status_code in [201]:
        return True
    else:
        # ERROR Необходимо сделать обработку
        return False


def downloadFileFromDisk():
    headers = {
        'Accept': 'application/json',
        'Authorization': 'OAuth ' + os.getenv('YANDEX_DISK_TOKEN'),
    }

    params = {
        'path': 'bot/consultation_schedule.xlsx',
    }

    response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/download', params=params, headers=headers)

    if response.status_code in [200]:
        return response.json()['href']
    else:
        # обработать
        return None


def updateData():
    if isTimeExpired():
        deletePreviousFileOnDisk()
        uploadFileOnDisk()
        downloadFileUrl = downloadFileFromDisk()
        pandasExcelFile = pd.read_excel(downloadFileUrl)
        ConsultationSchedule.schedule = pandasExcelFile


async def consultation_schedule(data, message, bot, dp):
    STATE = dp.current_state(user=message.from_user.id)
    await STATE.set_state('stored_frame_id_consultation_schedule_stage_1_000574788794')
    try:
        updateData()
        KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=False)
        pandasExcelFileColumns = ConsultationSchedule.schedule.columns
        uniqueInstitutes = ConsultationSchedule.schedule[pandasExcelFileColumns[0]].unique()
        for value in uniqueInstitutes:
            KEYBOARD.add(value)

        return await message.answer(
            parse_mode=ParseMode.HTML,
            text="Выберите институт",
            reply_markup=KEYBOARD
        )
    except Exception as error:
        pass


async def consultation_schedule_stage_1(message, bot, dp):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state('stored_frame_id_consultation_schedule_stage_2_322282694270')

    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=False)

    pandasExcelFileColumns = ConsultationSchedule.schedule.columns
    dataframe = ConsultationSchedule.schedule.loc[
        ConsultationSchedule.schedule[
            pandasExcelFileColumns[0]
        ] == message.text
        ]
    uniqueDepartments = dataframe[pandasExcelFileColumns[1]].unique()
    for value in uniqueDepartments:
        KEYBOARD.add(value)

    return await message.answer(
        parse_mode=ParseMode.HTML,
        text="Выберите кафедру",
        reply_markup=KEYBOARD
    )


async def consultation_schedule_stage_2(message, bot, dp):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state('stored_frame_id_consultation_schedule_stage_3_042298741485')
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=False)

    pandasExcelFileColumns = ConsultationSchedule.schedule.columns
    dataframe = ConsultationSchedule.schedule.loc[
        ConsultationSchedule.schedule[
            pandasExcelFileColumns[1]
        ] == message.text
        ]
    uniqueTeachers = dataframe[pandasExcelFileColumns[2]].unique()
    for value in uniqueTeachers:
        KEYBOARD.add(value)

    return await message.answer(
        parse_mode=ParseMode.HTML,
        text="Выберите преподавателя",
        reply_markup=KEYBOARD
    )


async def consultation_schedule_stage_3(message, bot, dp):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state('start')

    pandasExcelFileColumns = ConsultationSchedule.schedule.columns
    dataframe = ConsultationSchedule.schedule.loc[
        ConsultationSchedule.schedule[
            pandasExcelFileColumns[2]
        ] == message.text
        ]
    text = ''
    for i, row in dataframe.iterrows():
        text += f'\n- День недели: {row[3]}, \n  Неделя: {row[4]}, \n  Время: {row[5]}, \n  Аудитория: {row[6]}'
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=False)
    KEYBOARD.add('Назад')

    return await message.answer(
        parse_mode=ParseMode.HTML,
        text=text,
        reply_markup=KEYBOARD
    )

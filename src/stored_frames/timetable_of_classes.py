from io import BytesIO
import re
import requests as request
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ParseMode
from bs4 import BeautifulSoup
from pdf2image import convert_from_bytes
from datetime import datetime


class CurrentData(object):
    InstituteNames = None
    Schedule = None


def getSchedule():
    SIBSIU_PAGE_URL = 'https://www.sibsiu.ru'
    SIBSIU_SHEDULE_PAGE_URL = SIBSIU_PAGE_URL + '/raspisanie/'

    response = request.get(SIBSIU_SHEDULE_PAGE_URL)
    responseHTML = BeautifulSoup(response.text, 'html.parser')
    instituteDivs = responseHTML.select('.institut_div')
    resultStructure = []
    listOfInstituteNames = []

    for institute in instituteDivs:
        instituteTitle = institute.select('p.p_title > strong')
        instituteTitle = re.findall(r"\>(.*?)\<", str(instituteTitle))
        instituteTitle = [i for i in instituteTitle if i][0].strip()
        listOfInstituteNames.append(instituteTitle)
        instituteFilesLinkList = institute.select(
            'li.ul_file > a')
        for item in instituteFilesLinkList:
            pdfFileName = item.getText()
            pdfLink = SIBSIU_PAGE_URL + \
                item['href'].replace('\\', '/').replace(' ', '%20')

            resultStructure.append(
                {'group_name': f'{instituteTitle}',
                 'file_name': f'{pdfFileName}',
                 'file_link': f'{pdfLink}'})

    return resultStructure, listOfInstituteNames


def getFileAndLastModifiedDate(link):
    res = request.get(link)
    res.encoding = 'utf-8'
    lastModified = res.headers['Last-Modified']
    date = correctDate(lastModified)
    return res, date


def ConvertPDFtoPNG(res):
    images = convert_from_bytes(res.content, dpi=300)
    countOfPics = len(images)
    listOfBytesImages = []

    for i, v in enumerate(images):
        buf = BytesIO()
        v.save(buf, format('PNG'))
        buf.seek(0)
        listOfBytesImages.append(buf)

    return listOfBytesImages, countOfPics


def correctDate(date):
    date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    return date


def updateData():
    CurrentData.Schedule, \
    CurrentData.InstituteNames = getSchedule()


async def timetable_of_classes(data, message, bot, dp):
    STATE = dp.current_state(user=message.from_user.id)
    await STATE.set_state("stored_frame_id_timetable_of_classes_stage_1_523442133421")
    try:
        updateData()
        KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True)
        for value in CurrentData.InstituteNames:
            KEYBOARD.add(value)

        return await message.answer(
            parse_mode=ParseMode.HTML,
            text="институты",
            reply_markup=KEYBOARD
        )
    except Exception as error:
        pass


async def timetable_of_classes_stage_1(message, bot, dp):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("stored_frame_id_timetable_of_classes_stage_2_616470294411")

    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)

    selectedInstitudeFiles = []
    for value in CurrentData.Schedule:
        if value['group_name'] == message.text:
            selectedInstitudeFiles.append(
                {
                    'file_name': value['file_name'],
                    'file_link': value['file_link'],
                }
            )
            KEYBOARD.add(value['file_name'])

    await message.answer(
        parse_mode=ParseMode.HTML,
        text="группа",
        reply_markup=KEYBOARD
    )
    async with state.proxy() as data:
        data['selectedInstitudeFiles'] = selectedInstitudeFiles
    return None


async def timetable_of_classes_stage_2(message, bot, dp):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("start")
    CHAT_ID = message.chat.id
    date = None
    MEDIA = types.MediaGroup()
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)
    async with state.proxy() as data:
        selectedInstitudeFiles = data['selectedInstitudeFiles']
    for value in selectedInstitudeFiles:
        if value['file_name'] == message.text:
            await bot.send_message(CHAT_ID, text="Идет загрузка, пожалуйста подождите...")
            file, date = getFileAndLastModifiedDate(value['file_link'])
            listOfBytesImages, countOfImages = ConvertPDFtoPNG(file)
            if countOfImages > 10:
                await bot.send_message(message.chat.id,
                                       text=(f'В файле {countOfImages} изображений, расписание будет'
                                             + f' отправлено порционно.'))
                countTensFiles = countOfImages // 10
                residueCountTensFiles = countOfImages % 10
                currentNumberOfTensFiles = 0
                for cTF in range(countTensFiles):
                    MEDIACTF = types.MediaGroup()
                    for cTFP in range(10):
                        bPhoto = listOfBytesImages[currentNumberOfTensFiles]
                        MEDIACTF.attach_photo(bPhoto, f'Страница документа: {currentNumberOfTensFiles + 1}')
                        currentNumberOfTensFiles += 1
                    await bot.send_media_group(message.from_user.id, MEDIACTF)
                if residueCountTensFiles:
                    MEDIACTFR = types.MediaGroup()
                    for cTFR in range(countOfImages)[-residueCountTensFiles:]:
                        bPhoto = listOfBytesImages[cTFR]
                        MEDIACTFR.attach_photo(bPhoto, f'Страница документа: {cTFR + 1}')
                    await bot.send_media_group(message.from_user.id, MEDIACTFR)
            else:
                for index, image in enumerate(listOfBytesImages):
                    MEDIA.attach_photo(image, f'Страница документа: {index + 1}')
                await bot.send_media_group(CHAT_ID,
                                           media=MEDIA)
    KEYBOARD.add('Назад')
    await bot.send_message(CHAT_ID,
                           text=f'Дата обновления на сайте: {date}',
                           reply_markup=KEYBOARD)

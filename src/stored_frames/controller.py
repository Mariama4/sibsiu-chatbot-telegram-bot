from src.stored_frames.timetable_of_classes import *
from src.stored_frames.consultation_schedule import *
from src.stored_frames.current_week import *

STORED_FRAMES_IDS = [
    'stored_frame_id_timetable_of_classes_stage_1_523442133421',
    'stored_frame_id_timetable_of_classes_stage_2_616470294411',
    'stored_frame_id_consultation_schedule_stage_1_000574788794',
    'stored_frame_id_consultation_schedule_stage_2_322282694270',
    'stored_frame_id_consultation_schedule_stage_3_042298741485',
]


async def getState(dp, message):
    state = dp.current_state(user=message.from_user.id)
    async with state.proxy() as data:
        return data.state


async def storedFramesController(data, message, bot, dp):
    match data['stored_frame_id']:
        case 'timetable_of_classes':
            return await timetable_of_classes(data, message, bot, dp)
        case 'current_week':
            return await current_week(data, message, bot, dp)
        case 'consultation_schedule':
            return await consultation_schedule(data, message, bot, dp)
        case _:
            pass


async def storedStatesController(message, bot, dp):
    state = await getState(dp, message)
    match state:
        case 'stored_frame_id_timetable_of_classes_stage_1_523442133421':
            return await timetable_of_classes_stage_1(message, bot, dp)
        case 'stored_frame_id_timetable_of_classes_stage_2_616470294411':
            return await timetable_of_classes_stage_2(message, bot, dp)
        case 'stored_frame_id_consultation_schedule_stage_1_000574788794':
            return await consultation_schedule_stage_1(message, bot, dp)
        case 'stored_frame_id_consultation_schedule_stage_2_322282694270':
            return await consultation_schedule_stage_2(message, bot, dp)
        case 'stored_frame_id_consultation_schedule_stage_3_042298741485':
            return await consultation_schedule_stage_3(message, bot, dp)

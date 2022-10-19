from src.stored_frames.timetable_of_classes import *

STORED_FRAMES_IDS = [
    'stored_frame_id_timetable_of_classes_stage_1_523442133421',
    'stored_frame_id_timetable_of_classes_stage_2_616470294411',
]


async def getState(dp, message):
    state = dp.current_state(user=message.from_user.id)
    async with state.proxy() as data:
        return data.state


def storedFramesController(data, message, bot, dp):
    match data['stored_frame_id']:
        case 'timetable_of_classes':
            return timetable_of_classes(data, message, bot, dp)
        case 'current_week':
            pass
        case 'consultation_schedule':
            pass
        case _:
            pass


async def storedStatesController(message, bot, dp):
    state = await getState(dp, message)
    match state:
        case 'stored_frame_id_timetable_of_classes_stage_1_523442133421':
            return await timetable_of_classes_stage_1(message, bot, dp)
        case 'stored_frame_id_timetable_of_classes_stage_2_616470294411':
            return await timetable_of_classes_stage_2(message, bot, dp)

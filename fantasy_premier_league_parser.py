from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from fake_useragent import UserAgent
import requests
import json

ua = UserAgent()

fantasy_data = []
fantasy_team_data = []

BOT_TOKEN = 'YOUR_TOKEN'

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

user_id = 0
current_event = 0


def fantasy_premier_league():
    response = requests.get(
        url="https://fantasy.premierleague.com/api/entry/your_id/",
        headers={
            "user-agent": f"{ua.random}"
        }
    )

    with open(f"{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

    data = response.json()

    fantasy_id = data["id"]
    joined_time = data["joined_time"]
    player_first_name = data["player_first_name"]
    player_last_name = data["player_last_name"]
    player_region_name = data["player_region_name"]
    summary_overall_points = data["summary_overall_points"]
    summary_overall_rank = data["summary_overall_rank"]
    summary_event_points = data["summary_event_points"]
    global current_event
    current_event = data["current_event"]
    name = data["name"]
    last_deadline_total_transfers = data["last_deadline_total_transfers"]

    fantasy_data.append(
        [
            fantasy_id,
            joined_time,
            player_first_name,
            player_last_name,
            player_region_name,
            summary_overall_points,
            summary_overall_rank,
            summary_event_points,
            current_event,
            name,
            last_deadline_total_transfers
        ]
    )


def fantasy_premier_league_team():
    response = requests.get(
        url=f"https://fantasy.premierleague.com/api/entry/your_id/event/{current_event}/picks/",
        headers={
            "user-agent": f"{ua.random}"
        }
    )

    with open(f"{user_id}.json", "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

    data = response.json()

    for i in data["picks"]:
        position = i["position"]
        multiplier = i["multiplier"]
        is_captain = i["is_captain"]
        is_vice_captain = i["is_vice_captain"]

        fantasy_team_data.append(
            [
                position,
                multiplier,
                is_captain,
                is_vice_captain
            ]
        )


@dp.message_handler(commands='start')
async def start(message: types.Message):
    global user_id
    user_id = message.from_user.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Main datas"))
    keyboard.insert(types.KeyboardButton(text="Datas of team"))
    await message.answer("Choose the data", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def main_datas(message: types.Message):
    fantasy_premier_league()
    if message.text == "Main datas":
        main_data = ''
        for i in fantasy_data:
            text_main_data = f"id: {i[0]}\njoined_time: {i[1]}\nplayer_first_name: {i[2]}\nplayer_last_name: {i[3]}\nplayer_region_name: {i[4]}\nsummary_overall_points: {i[5]}\nsummary_overall_rank: {i[6]}\nsummary_event_points: {i[7]}\ncurrent_event: {i[8]}\nname: {i[9]}\nlast_deadline_total_transfers: {i[10]}"
            main_data += text_main_data
        await message.answer(main_data)
    elif message.text == "Datas of team":
        fantasy_premier_league_team()
        data = ''
        for j in fantasy_team_data:
            text_data = f"position: {j[0]}\nmultiplier: {j[1]}\nis_captain: {j[2]}\nis_vice_captain: {j[3]}\n\n"
            data += text_data
        await message.answer(data)
    else:
        await message.answer("Please choose the type data below")
        return start


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

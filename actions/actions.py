# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests

CITY_MAP = {
    "서울": "Seoul",
    "부산": "Busan",
    "대구": "Daegu",
    "인천": "Incheon",
    "광주": "Gwangju",
    "순천": "Suncheon",
}


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # OpenWeather API 키 설정
        api_key = "27b08031f6cebbcb6e3a51926dc36502"

        # 사용자 입력에서 'city' 슬롯 가져오기
        city = tracker.get_slot('city')

        if city is None:
            dispatcher.utter_message(text="어떤 도시의 날씨를 알고 싶으신가요?")
            return []

        # 도시명을 표준화하고 한국어일때 영어로 변환
        city = city.capitalize()
        city = CITY_MAP.get(city.strip(), city)

        # OpenWeather API 호출
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=kr"
        response = requests.get(url).json()

        # API 응답 데이터 확인
        if response.get("cod") != 200:
            dispatcher.utter_message(text=f"{city}의 날씨 정보를 찾을 수 없습니다. 다시 시도해 주세요.")
            return []

        # 날씨 정보 추출
        temperature = response["main"]["temp"]
        feels_like = response["main"]["feels_like"]
        description = response["weather"][0]["description"]
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]

        # 사용자에게 응답
        dispatcher.utter_message(
            text=f"{city}의 현재 날씨는 {description}입니다. 기온은 {temperature}도이며, 체감 온도는 {feels_like}도입니다. "
                 f"바람은 시속 {wind_speed} m/s로 불고 있으며, 습도는 {humidity}%입니다."
        )
        return []

class ActionResetCitySlot(Action):
    def name(self) -> Text:
        return "action_reset_city_slot"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("city", None)]
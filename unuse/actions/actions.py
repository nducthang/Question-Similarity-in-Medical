# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import feedparser

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionKetQuaSoXo(Action):
    def name(self) -> Text:
        return "action_kq_xo_so"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Khai bao dia chi luu tru ket qua so xo. O day lam vi du nen minh lay ket qua SX Mien Bac
        url = 'https://xskt.com.vn/rss-feed/mien-bac-xsmb.rss'
        # Tien hanh lay thong tin tu URL
        feed_cnt = feedparser.parse(url)
        # Lay ket qua so xo moi nhat
        first_node = feed_cnt['entries']
        # Lay thong tin ve ngay va chi tiet cac giai
        return_msg = first_node[0]['title'] + "\n" + first_node[0]['description']
        # Tra ve cho nguoi dung
        dispatcher.utter_message(return_msg)
        return []

class ActionExtract(Action):
    def name(self) -> Text:
        return "action_extract"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # lấy ra đoạn hội thoại cuối
        text = tracker.latest_message['text'].lower()
        with open('data/benh.txt') as f:
            benh = f.read().split('\n')
        with open('data/trieuchung.txt') as f:
            trieuchung = f.read().split('\n')
        show_benh = []
        show_trieuchung = []
        for b in benh:
            if b in text:
                show_benh.append(b)

        for tt in trieuchung:
            if tt in text:
                show_trieuchung.append(tt)

        if len(show_benh)==0 and len(show_trieuchung)==0:
            dispatcher.utter_message("Bệnh/triệu chứng chưa có trong CSDL")
        
        mess_benh = ','.join(show_benh)
        mess_trieuchung = ','.join(show_trieuchung)

        print("Mess benh:", mess_benh)
        print("Mess trieu chung:", mess_trieuchung)

        if len(show_benh)!=0:
            dispatcher.utter_message('Bệnh: '+mess_benh)
        if len(show_trieuchung)!=0:
            dispatcher.utter_message('Triệu chứng:'+mess_trieuchung)
        
        return []

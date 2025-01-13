from asyncio import get_event_loop

import grpc
from pyrogram import Client
from grpc_utils.proto import message_pb2_grpc, message_pb2


class ProgressTracker:
    def __init__(self, client: Client = None, bot_name:str = None, static_key:str = None):
        self.last_percent = 0
        self.pyro_client: Client = client
        self.bot_name: str = bot_name
        self.static_key: str = static_key
        self.current_id = None
        self.channel = grpc.insecure_channel('aioyou:50051')
        self.stub = message_pb2_grpc.MessageServiceStub(self.channel)

    def set_cur_id(self, new_id):
        self.current_id = new_id

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100 if d['total_bytes'] else 0

            if percent - self.last_percent >= 3:

                percent = round(percent)
                self.stub.SendMessage(message_pb2.Message(text=f"{percent}",
                                                          tg_user_id=str(self.current_id),
                                                          type_mess="progress"))
                self.last_percent = percent

        elif d['status'] == 'finished':
            print(f"Загрузка завершена: {d['filename']}")
            self.last_percent = 0



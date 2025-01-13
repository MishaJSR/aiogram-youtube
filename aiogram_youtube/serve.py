import asyncio

import grpc
import validators
from aiogram import Bot
from aiogram.enums import ParseMode

from grpc_utils.proto import message_pb2, message_pb2_grpc


async def start_progress_bar(bot, tg_user_id, duration_in_seconds, mess_id, stop_event):
    while not stop_event.is_set():
        addition = "."
        for i in range(3):
            await bot.edit_message_text(
                text=f"Video is being sent {addition}",
                chat_id=tg_user_id,
                message_id=mess_id,
            )
            addition += "."
            await asyncio.sleep(.5)
    await bot.delete_message(chat_id=tg_user_id, message_id=mess_id)


class MessagingServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.last_message_id = None
        self.message_status_id = None
        self.message_send_video_id = None
        self.stop_event = asyncio.Event()

    def is_valid_url(self, url):
        return validators.url(url)

    async def SendMessage(self, request, context):
        text = request.text
        tg_user_id = request.tg_user_id
        type_mess = request.type_mess
        response = message_pb2.Message(text="Message received: " + request.text)
        if type_mess == "repeat":
            await self.bot.send_message(chat_id=tg_user_id, text=f"{text}")
        if type_mess == "position":
            await self.bot.send_message(chat_id=tg_user_id, text=f"{text}")
        if type_mess == "url":
            url, img_url, description = text.split("`")
            await self.bot.send_photo(chat_id=tg_user_id, photo=f"{img_url}", caption=f"<b>{description}</b>", parse_mode=ParseMode.HTML)
            mess = await self.bot.send_message(chat_id=tg_user_id, text="Start loading")
            self.last_message_id = mess.message_id
        if type_mess == "progress":
            mess = await self.bot.edit_message_text(text=f"Loading status: {text}%",
                                             chat_id=request.tg_user_id,
                                             message_id=self.last_message_id)
            self.message_status_id = mess.message_id
        if type_mess == "error_load":
            await self.bot.send_message(chat_id=tg_user_id, text=f"{text}")
        if type_mess == "error_server":
            await self.bot.send_message(chat_id=tg_user_id, text=f"{text}")
        if type_mess == "send_video":
            await self.bot.delete_message(chat_id=tg_user_id, message_id=self.message_status_id)
            self.message_status_id = None
            m = await self.bot.send_message(chat_id=tg_user_id, text="Send video")
            self.message_send_video_id = m.message_id
            asyncio.create_task(start_progress_bar(bot=self.bot, tg_user_id=tg_user_id, duration_in_seconds=int(text),
                                                   mess_id=self.message_send_video_id, stop_event=self.stop_event))
            self.last_message_id = None
        if type_mess == "video_delivered":
            await stop_task(self.stop_event)
            self.stop_event = asyncio.Event()
        return response


async def stop_task(stop_event: asyncio.Event):
    stop_event.set()


async def serve(bot):
    server = grpc.aio.server()
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessagingServiceServicer(bot), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting...")
    await server.start()
    await server.wait_for_termination()

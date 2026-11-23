import os, asyncio
from aiohttp import web
from telethon import TelegramClient, events
from google import genai

ai_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
tg_client = TelegramClient("shoxrux_session", int(os.environ["API_ID"]), os.environ["API_HASH"])
SYSTEM_PROMPT = "Sen Shoxruxning shaxsiy AI yordamchisisan. Kelgan xabarlarga qisqa, do'stona va o'sha tilda javob ber."

@tg_client.on(events.NewMessage(incoming=True))
async def handler(event):
    if not event.is_private or getattr(await event.get_sender(), "bot", False) or not event.raw_text:
        return
    try:
        res = ai_client.models.generate_content(model="gemini-2.5-flash", contents=f"{SYSTEM_PROMPT}\n\nXabar: {event.raw_text}")
        await event.reply(res.text.strip())
    except Exception as e:
        print(e)

async def main():
    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="OK"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8000))).start()
    await tg_client.start()
    await tg_client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

from pyrofork import Client, filters
import re

api_id = 22051826  # جایگزین با API ID واقعی
api_hash = "your_api_hash"  # جایگزین با API Hash واقعی

app = Client("stars_bot", api_id=api_id, api_hash=api_hash, test_mode=True)

@app.on_message(filters.me & filters.regex(r'^استارز\s+(https?://t\.me/\S+)\s+(\d+)$'))
async def handle_stars(client, message):
    link = message.matches[0].group(1)
    count = int(message.matches[0].group(2))

    match = re.match(r'https://t.me/([^/]+)/(\d+)', link)
    if not match:
        await message.reply("لینک معتبر نیست.")
        return

    username = match.group(1)
    msg_id = int(match.group(2))

    success = 0
    for _ in range(count):
        try:
            await client.send_paid_reaction(
                chat_id=username,
                message_id=msg_id,
                emoji="⭐"
            )
            success += 1
        except Exception as e:
            await message.reply(f"خطا هنگام ارسال استارز: {e}")
            return

    await message.reply(f"{success} عدد استارز با موفقیت ارسال شد.")

app.run()

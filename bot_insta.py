from instagrapi import Client
import time
import os

cl = Client()

# Load session (مهم)
cl.load_settings("session.json")
print("Login with session ✅")

last_seen_file = "last_seen.txt"

# قراءة آخر رسالة
if os.path.exists(last_seen_file):
    with open(last_seen_file, "r", encoding="utf-8") as f:
        last_seen_id = f.read().strip()
else:
    last_seen_id = ""

while True:
    try:
        threads = cl.direct_threads()
        print("Checking messages...")

        for thread in threads:
            if not thread.messages:
                continue

            last_message = thread.messages[0]
            message_id = str(last_message.id)
            text = (last_message.text or "").lower()
            user_id = thread.users[0].pk

            # ignore messages ديالك
            if getattr(last_message, "is_sent_by_viewer", False):
                continue

            # ignore القديم
            if message_id == last_seen_id:
                continue

            # الردود
            if "salam" in text or "slm" in text:
                reply = "Salam 👋 kif n9dr n3awnk?"
            elif "prix" in text or "taman" in text:
                reply = "Marhba 👌 sift liya chno bghiti w نعطيك التمن"
            elif "bot" in text:
                reply = "Eywa 🤖 kanbi3 bots Instagram"
            else:
                reply = "Merhba 😊 kif n9dr n3awnk?"

            cl.direct_send(reply, [user_id])
            print("Reply sent:", reply)

            # حفظ آخر message
            with open(last_seen_file, "w") as f:
                f.write(message_id)

        time.sleep(5)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
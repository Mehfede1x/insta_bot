from instagrapi import Client
import os
import time

cl = Client()

cl = Client()

cl.login("siham.14z", "smaili3200")
cl.dump_settings("session.json")

print("Session saved ✅")

cl.dump_settings("session.json")

print("Session updated ✅")

last_seen_file = "last_seen.txt"

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

            if getattr(last_message, "is_sent_by_viewer", False):
                continue

            if message_id == last_seen_id:
                continue

            if "salam" in text or "slm" in text:
                reply = "Salam 👋 kif n9dr n3awnk?"
            elif "prix" in text or "taman" in text:
                reply = "Marhba 👌 sift liya chno bghiti w an3tik taman."
            elif "bot" in text:
                reply = "Eywa, n9dro nsaybo lik bot 3la hsab talab dialk 🤖"
            else:
                reply = "Merhba 😊 chrah liya chno bghiti w anjawbk."

            cl.direct_send(reply, [user_id])
            print("Reply sent ✅ ->", reply)

            last_seen_id = message_id
            with open(last_seen_file, "w", encoding="utf-8") as f:
                f.write(message_id)

        time.sleep(5)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
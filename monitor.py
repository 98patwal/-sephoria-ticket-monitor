import time
import requests

WEEZEVENT_URL = "https://api.weezevent.com/ticket/widgets/resale-sephoria-london-2026?locale=en-gb"
NTFY_URL = "https://ntfy.sh/PA1998-SepLDN"
TICKET_URL = "https://widget.weezevent.com/ticket/resale-sephoria-london-2026?locale=en-gb"

last_available = False

print("SEPHORiA monitor started")
print("Checking every 10 seconds...")

while True:
    try:
        response = requests.get(
            WEEZEVENT_URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            },
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        def find_on_resale(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == "on_resale":
                        return value
                    result = find_on_resale(value)
                    if result is not None:
                        return result

            elif isinstance(obj, list):
                for item in obj:
                    result = find_on_resale(item)
                    if result is not None:
                        return result

            return None

        available = find_on_resale(data)

        print(
            time.strftime("%Y-%m-%d %H:%M:%S"),
            "on_resale =",
            available
        )

        if available is True and last_available is False:
            print("TICKET AVAILABLE — sending notification!")

            requests.post(
                NTFY_URL,
                data=f"SEPHORiA London resale ticket available! Tap here: {TICKET_URL}".encode(),
                headers={
                    "Title": "🚨 SEPHORiA London ticket available!",
                    "Priority": "max",
                    "Tags": "ticket"
                },
                timeout=20
            )

            last_available = True

        elif available is False:
            last_available = False

    except Exception as e:
        print("ERROR:", e)

    time.sleep(10)

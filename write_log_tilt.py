import asyncio
from datetime import datetime
from bleak import BleakScanner

TILT_UUIDS = {
    "a495bb10c5b14b44b5121370f02d74de": "Red",
    "a495bb20c5b14b44b5121370f02d74de": "Green",
    "a495bb30c5b14b44b5121370f02d74de": "Black",
    "a495bb40c5b14b44b5121370f02d74de": "Purple",
    "a495bb50c5b14b44b5121370f02d74de": "Orange",
    "a495bb60c5b14b44b5121370f02d74de": "Blue",
    "a495bb70c5b14b44b5121370f02d74de": "Yellow",
    "a495bb80c5b14b44b5121370f02d74de": "Pink",
}

LOG_FILE = "tilt_log.csv"

# Write header to file if it doesn't exist
with open(LOG_FILE, "a") as f:
    f.write("Timestamp,Color,Temp_C,Gravity,Device_Address\n")

def decode_tilt(data):
    uuid = data[2:18].hex()
    major = int.from_bytes(data[18:20], "big")
    minor = int.from_bytes(data[20:22], "big")

    temp_f = major
    gravity = minor / 1000

    return uuid, temp_f, gravity


def detection_callback(device, advertisement_data):
    for company_id, data in advertisement_data.manufacturer_data.items():
        if company_id == 0x004C and data.hex().startswith("0215"):
            uuid, temp_f, gravity = decode_tilt(data)
            temp_c = (temp_f - 32) / 1.8

            if uuid in TILT_UUIDS:
                color = TILT_UUIDS[uuid]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_line = f"{timestamp},{color},{temp_c:.2f},{gravity:.3f},{device.address}"
                print(log_line)

                # Append to log file
                with open(LOG_FILE, "a") as f:
                    f.write(log_line + "\n")


async def main():
    scanner = BleakScanner(detection_callback)
    await scanner.start()

    print("Listening for Tilt...")
    while True:
        await asyncio.sleep(1)


asyncio.run(main())

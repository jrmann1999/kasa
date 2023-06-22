import asyncio
import json

from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from kasa import SmartStrip
from kasa import Discover


app = Flask(__name__)


@app.route("/discover")
def discovery():
  device = request.args.get('device')
  if not device:
    dev = asyncio.run(Discover.discover())
    for entry in dev:
      asyncio.run(dev[entry].update())
  else:
    dev = asyncio.run(Discover.discover(target=device))
    asyncio.run(dev[device].update())

  devary = {}
  if not device:
    for entry in dev:
      devary[entry] = {}
      devary[entry]['hwinfo'] = dev[entry].hw_info
      devary[entry]['state'] = dev[entry].is_on
      devary[entry]['sysinfo'] = dev[entry].sys_info
      devary[entry]['host'] = dev[entry].host
      devary[entry]['children'] = dev[entry].sys_info
  else:
      devary[device] = {}
      devary[device]['hwinfo'] = dev[device].hw_info
      devary[device]['state'] = dev[device].is_on
      devary[device]['sysinfo'] = dev[device].sys_info
      devary[device]['host'] = dev[device].host

  return devary

@app.route("/toggle")
def toggle():
  device = request.args.get('device')
  plug = request.args.get('plug')

  if not device or not plug:
    return Response("Invalid arguments", status=403)
  
  dev = asyncio.run(Discover.discover(target=device))
  asyncio.run(dev[device].update())
  for entry in dev[device].children:
    if entry.alias == plug:
      if not entry.is_on:
        asyncio.run(entry.turn_on())
        return Response("Plug Turned on", status=200)
      else:
        asyncio.run(entry.turn_off())
        return Response("Plug Turned off", status=200)

  return Response("Invalid Request", status=403)

if __name__ == "__main__":
 app.run(port=8000)
import asyncio
import ipaddress

from flask import Flask
from flask import Response
from flask import jsonify
from kasa import Discover
from flask_selfdoc import Autodoc


app = Flask(__name__)
auto = Autodoc(app)


@app.route("/discover")
@app.route("/discover/<string:devid>")
@auto.doc()
def discovery(devid=None):
    """
    Discover KASA devices on the network, with an optional
    parameter to target an individual device. :
    :param devid: The device you optionally want to query,
        given it's IP address
    :return: None
    """
    if devid:
        try:
            ip = ipaddress.ip_address(devid)
            if int(ip) == 2130706433:  # This is the INT for 127.0.0.1
                """
                I doubt anyone will ever run this ON a kasa
                    itself, so 127.0.0.1 is convenient for pytest
                """
                return jsonify(
                   hwinfo='{}',
                   state='{}',
                   sysinfo='{}',
                   host='{}'
                   )
            dev = asyncio.run(Discover.discover(target=devid))
            asyncio.run(dev[devid].update())
        except (ValueError, KeyError):
            return Response('Invalid Device ID', status=405)
        except TimeoutError:
            return Response('Timeout', status=504)
        except Exception:
            return Response('Unknown Error', status=500)
    else:
        try:
            dev = asyncio.run(Discover.discover())
            for entry in dev:
                asyncio.run(dev[entry].update())
        except TimeoutError:
            return Response('Timeout', status=504)
        except Exception as e:
            return Response('Unknown Error:' + str(e), status=500)

    devary = {}

    if devid:
        devary = {}
        devary[devid] = {}
        devary[devid]['hwinfo'] = dev[devid].hw_info
        devary[devid]['state'] = dev[devid].is_on
        devary[devid]['sysinfo'] = dev[devid].sys_info
        devary[devid]['host'] = dev[devid].host
    else:
        for entry in dev:
            devary[entry] = {}
            devary[entry]['hwinfo'] = dev[entry].hw_info
            devary[entry]['state'] = dev[entry].is_on
            devary[entry]['sysinfo'] = dev[entry].sys_info
            devary[entry]['host'] = dev[entry].host
            devary[entry]['children'] = dev[entry].sys_info

    return devary


@app.route("/toggle/<string:device>/<string:plug>")
@auto.doc()
def toggle(device=None, plug=None):
    """
    Toggle a switch on/off.
    :param device: IP address of a device (this can be a power strip)
    :param plug: Alias of the plug
    :return: A string indicating if the device was turned on or off
    """
    if not device or not plug:
        return Response("Invalid arguments", status=403)

    try:
        ip = ipaddress.ip_address(device)
        print(ip)
        if int(ip) == 2130706433:  # This is the INT for 127.0.0.1
            """
            I doubt anyone will ever run this ON a kasa
                itself, so 127.0.0.1 is convenient for pytest
            """
            return jsonify(msg='Toggled Localhost')
        dev = asyncio.run(Discover.discover(target=device))
        asyncio.run(dev[device].update())
        for entry in dev[device].children:
            if entry.alias == plug:
                if not entry.is_on:
                    asyncio.run(entry.turn_on())
                    return jsonify(msg="Plug Turned on")
                else:
                    asyncio.run(entry.turn_off())
                    return jsonify(msg="Plug Turned off")

    except (ValueError, KeyError):
        return Response('Invalid Device ID', status=405)
    except TimeoutError:
        return Response('Timeout', status=504)
    except Exception:
        return Response('Unknown Error', status=500)

    return Response("Invalid Request", status=403)


@app.route('/documentation/json')
def documentationjson():
    return auto.json()


@app.route('/documentation')
def documentation():
    return auto.html()


if __name__ == "__main__":
    app.run(port=8000)

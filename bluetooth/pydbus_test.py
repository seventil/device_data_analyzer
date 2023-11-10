import pydbus
from gi.repository import GLib

discovery_time = 20

bus = pydbus.SystemBus()
mainloop = GLib.MainLoop()

# Connect to the DBus api for the Bluetooth adapter
adapter = bus.get('org.bluez', '/org/bluez/hci0')

def end_discovery():
    """Handler for end of discovery"""
    mainloop.quit()
    adapter.StopDiscovery()

# Run discovery
adapter.StartDiscovery()
GLib.timeout_add_seconds(discovery_time, end_discovery)
print('Finding nearby devices...')
mainloop.run()

# Iterate around the devices to find audio devices
mngr = bus.get('org.bluez', '/')
mng_objs = mngr.GetManagedObjects()

for path in mng_objs:
    uuids = mng_objs[path].get('org.bluez.Device1', {}).get('UUIDs', [])
    # print(path, uuids)
    for uuid in uuids:
        # Service discovery UUIDs
        # https://www.bluetooth.com/specifications/assigned-numbers/service-discovery/
        # AudioSink - 0x110B - Advanced Audio Distribution Profile (A2DP)
        if uuid.startswith('0000110b'):
            print(mng_objs[path].get('org.bluez.Device1', {}).get('Name'),
                  mng_objs[path].get('org.bluez.Device1', {}).get('Address'))
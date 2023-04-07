from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from timeit import time
# import bluetooth
from bleak import BleakScanner
import asyncio
import time

Window.size=(640,480)
Builder.load_file('loop.kv')


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(name=kwargs.get('name'))
        self.loop_thread = None

    def on_enter(self):
        self.loop_thread = Clock.schedule_interval(self.callback_to_loop, 1)

        #self._get_blt_devices()
        #time.sleep(5)
        self._get_lte_devices()


    def on_leave(self):  
        Clock.unschedule(self.loop_thread)

    def callback_to_loop(self, dt):
        try:
            current = int(self.ids.label_print.text)
        except:
            current = 0

        self.ids.label_print.text = str(current+1)

    # def _get_blt_devices(self):
    #     print("Started blt scan")
    #     nearby_blt_devices = bluetooth.discover_devices(lookup_names=True)
    #     print(f"nearby blt devices got {nearby_blt_devices}")
    #     found_blt_devices = "\n".join([f"<{addr}> - <{name}>" for addr, name in nearby_blt_devices])
    #     self.ids.blt_devices.text = found_blt_devices

    def _get_lte_devices(self):
        print("Started lte scan")
        nearby_lte_devices = asyncio.run(BleakScanner.discover())
        print(f"nearby lte devices got {nearby_lte_devices}")
        found_lte_devices = "\n".join([f"<{device.address}> - <{device.name}>" for device in nearby_lte_devices])
        print(f"found lte devices: {found_lte_devices}")
        self.ids.lte_devices.text = found_lte_devices


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_screen'))
        return sm

if __name__=='__main__':
    MainApp().run()
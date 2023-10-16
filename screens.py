from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.app import App


class MenuScreen(Screen):
    pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__()
        self.loop_thread = None
        
    def on_enter(self):
        self.loop_thread = Clock.schedule_interval(self.callback_to_loop, 1)

    def on_leave(self):  
        Clock.unschedule(self.loop_thread)

    def callback_to_loop(self, dt):
        try:
            current = int(self.ids.label_print.text)
        except:
            current = 0

        self.ids.label_print.text = str(current+1)

    def start_scan(self):
        self.ids.label.text = "Scanning blt"
        scan_devices = App.get_running_app().blt_processor.scan_tpc_devices
        App.get_running_app().command_queue.append((scan_devices,[]))

    def stop_client(self):
        print("pressed to stop client")
        self.ids.label.text = "Stopping client"
        stop_client = App.get_running_app().blt_processor.stop_client_for_device
        App.get_running_app().command_queue.append((stop_client,[]))
        print("stop client command added to queue")
        print(App.get_running_app().command_queue)

        
    def sleeping_callback(self):
        self.ids.label.text = "Connecting client"
        command_to_send = App.get_running_app().blt_processor.run_client_for_device
        args = ["TPC-7PRO #91"] # TODO delete hardcode, implement choice from UI
        App.get_running_app().command_queue.append((command_to_send, args))
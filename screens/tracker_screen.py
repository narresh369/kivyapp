# tracker_screen.py
import os
import traceback
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from jnius import autoclass
from android.runnable import run_on_ui_thread
from kivy.clock import Clock

class TrackerScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.index = 0

        # Animate marker every 1.25 seconds
        Clock.schedule_interval(self.move_marker, 1.25)

        if platform == "android":
            # Delay WebView setup until the next frame
            Clock.schedule_once(lambda dt: self._init_webview(), 0)

    def _init_webview(self):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView        = autoclass('android.webkit.WebView')
        WebViewClient  = autoclass('android.webkit.WebViewClient')

        @run_on_ui_thread
        def init_webview():
            try:
                # Create & configure WebView
                self.webview = WebView(PythonActivity.mActivity)
                self.webview.getSettings().setJavaScriptEnabled(True)
                self.webview.setWebViewClient(WebViewClient())

                html = "<html><body><h1>Hello WebView</h1></body></html>"
                self.webview.loadData(html, "text/html", "utf-8")


                # Load your asset
                url = "file:///android_asset/content/assets/map.html"
                print("🔍 Loading map.html from", url)
                self.webview.loadUrl(url)

                # Add WebView into the Android view hierarchy
                decor = PythonActivity.mActivity.getWindow().getDecorView()
                decor.addView(self.webview)
            except Exception:
                traceback.print_exc()

        init_webview()

    def move_marker(self, dt):
        if hasattr(self, 'webview'):
            # schedule JS evaluation on the UI thread
            self._eval_js(self.index)
            self.index += 1

    @run_on_ui_thread
    def _eval_js(self, idx):
        try:
            js = f"moveMarkerTo({idx});"
            self.webview.evaluateJavascript(js, None)
        except Exception:
            traceback.print_exc()

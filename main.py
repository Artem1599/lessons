from jnius import autoclass, cast
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

PythonActivity = autoclass("org.kivy.android.PythonActivity")
Settings = autoclass("android.provider.Settings")
Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")
WindowManager = autoclass("android.view.WindowManager")
LayoutParams = autoclass("android.view.WindowManager$LayoutParams")
View = autoclass("android.view.View")
Color = autoclass("android.graphics.Color")
PixelFormat = autoclass("android.graphics.PixelFormat")
Gravity = autoclass("android.view.Gravity")
BuildVersion = autoclass("android.os.Build$VERSION")
BuildVersionCodes = autoclass("android.os.Build$VERSION_CODES")


class OverlayController:
    def __init__(self):
        self.activity = PythonActivity.mActivity
        self.wm = cast(
            WindowManager,
            self.activity.getSystemService(self.activity.WINDOW_SERVICE),
        )
        self.overlay_view = None

    def has_overlay_permission(self) -> bool:
        if BuildVersion.SDK_INT >= BuildVersionCodes.M:
            return bool(Settings.canDrawOverlays(self.activity))
        return True

    def request_overlay_permission(self):
        if BuildVersion.SDK_INT >= BuildVersionCodes.M:
            intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:" + self.activity.getPackageName()),
            )
            self.activity.startActivityForResult(intent, 1001)

    def show_cover(self, x: int = 300, y: int = 80, width: int = 240, height: int = 70):
        if self.overlay_view is not None:
            return

        def _create_on_ui_thread():
            view = View(self.activity)
            view.setBackgroundColor(Color.parseColor("#1E2229"))

            if BuildVersion.SDK_INT >= BuildVersionCodes.O:
                win_type = LayoutParams.TYPE_APPLICATION_OVERLAY
            else:
                win_type = LayoutParams.TYPE_PHONE

            # FLAG_SECURE удалён: плашка остаётся видимой при захвате экрана и трансляции
            flags = (
                LayoutParams.FLAG_NOT_FOCUSABLE
                | LayoutParams.FLAG_LAYOUT_IN_SCREEN
            )

            params = LayoutParams(
                width,
                height,
                win_type,
                flags,
                PixelFormat.TRANSLUCENT,
            )
            params.gravity = Gravity.TOP | Gravity.START
            params.x = x
            params.y = y

            self.wm.addView(view, params)
            self.overlay_view = view

        self.activity.runOnUiThread(_create_on_ui_thread)

    def hide_cover(self):
        if self.overlay_view is None:
            return

        def _remove_on_ui_thread():
            if self.overlay_view is not None:
                self.wm.removeView(self.overlay_view)
                self.overlay_view = None

        self.activity.runOnUiThread(_remove_on_ui_thread)


class HomeCoverApp(App):
    def build(self):
        self.controller = OverlayController()

        root = BoxLayout(orientation="vertical", padding=24, spacing=16)

        btn_start = Button(text="Включить закрытие дистанции")
        btn_start.bind(on_press=self._on_start)

        btn_stop = Button(text="Выключить плашку")
        btn_stop.bind(on_press=self._on_stop)

        root.add_widget(btn_start)
        root.add_widget(btn_stop)
        return root

    def _on_start(self, _instance):
        if not self.controller.has_overlay_permission():
            self.controller.request_overlay_permission()
            return
        self.controller.show_cover(x=300, y=80, width=240, height=70)

    def _on_stop(self, _instance):
        self.controller.hide_cover()

    def on_pause(self):
        # Разрешаем паузу активности Kivy без выгрузки процесса и снятия оверлея
        return True

    def on_stop(self):
        # Не удаляем оверлей при уходе приложения в фон
        pass


if __name__ == "__main__":
    HomeCoverApp().run()
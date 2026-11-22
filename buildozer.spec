[app]

# Название приложения на пульте
title = Home Cover

# Имя пакета (латиницей, без пробелов)
package.name = homecover
package.domain = org.example

# Исходный код
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения
version = 0.1

# Зависимости Python (нужны kivy и pyjnius)
requirements = python3,kivy,pyjnius

# Ориентация экрана (для пульта чаще всего landscape)
orientation = landscape

# Разрешение на показ поверх других приложений
android.permissions = SYSTEM_ALERT_WINDOW

# Целевой и минимальный API Android
android.api = 33
android.minapi = 24

# Архитектура (для современных Android-устройств обычно arm64-v8a)
android.archs = arm64-v8a

fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1
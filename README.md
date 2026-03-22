# LibertyScripts
Набор утилит для решения разных задач поддержки VPN Liberty

# Содержимое
# 1. BypassRouting

---

# Требования

* Python 3.8+
* пакет `requests`

---

# Установка

```bash
python -m pip install requests
```

---

# Запуск

```bash
python bypass_routing.py
```

---

# Возможности

Скрипт получает по ссылке ключ bypass и затем позволяет настроить роутинг для полученных ключей.
 
Можно настроить правила:

   * direct

   * proxy

   * block

Поддерживает:

* IP адреса

* Домены

* geoip:*

* geosite:*

В конце сохраняет измененные ключи в формате для передачи в Telegram в файл в директории скрипта.

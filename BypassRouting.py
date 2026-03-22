import requests
import ipaddress
import json

def parse_input(value):
    items = [x.strip() for x in value.split(";") if x.strip()]

    ips = []
    domains = []

    for item in items:
        if item.startswith("geoip:"):
            ips.append(item)
            continue
        if item.startswith("geosite:"):
            domains.append(item)
            continue
        if item.startswith("domain:"):
            domains.append(item)
            continue
        try:
            ipaddress.ip_address(item)
            ips.append(item)
            continue
        except ValueError:
            pass
        domains.append(item)

    return ips, domains

def add_rule(config, ips, domains, outbound):
    if not ips and not domains:
        return  # ничего не добавляем

    # защита (на всякий случай)
    if "routing" not in config:
        config["routing"] = {}

    if "rules" not in config["routing"]:
        config["routing"]["rules"] = []

    rule = {
        "type": "field",
        "outboundTag": outbound
    }

    if ips:
        rule["ip"] = ips

    if domains:
        rule["domain"] = domains

    # ВАЖНО — вставляем в начало
    config["routing"]["rules"].insert(0, rule)


url = input("Вставь ссылку на VPN-ключ: ")

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    text = response.text.strip()

    if not text:
        print("Пустой ответ от сервера")
        exit()

    try:
        data = response.json()
        print("JSON успешно распарсен")

    except ValueError:
        print("Невозможно распарсить как JSON. Возможно ключ другого формата")

except requests.exceptions.RequestException as e:
    print("Ошибка запроса:", e)
print("--------------------------------")
print("Введите новые настройки роутинга(оставьте пустым, чтобы не изменять):")
new_direct = input("Правила для direct. ip и имена сайтов через ; (пример: 127.0.0.1;2ip.ru;geoip:ru):")
new_proxy = input("Правила для proxy. ip и имена сайтов через ; (пример: 127.0.0.1;2ip.ru;geoip:ru):")
new_block = input("Правила для block. ip и имена сайтов через ; (пример: 127.0.0.1;2ip.ru;geoip:ru):")

new_direct_ips, new_direct_domains = parse_input(new_direct)
new_proxy_ips, new_proxy_domains = parse_input(new_proxy)
new_block_ips, new_block_domains = parse_input(new_block)

configs = data if isinstance(data, list) else [data]

for config in configs:
    add_rule(config, new_direct_ips, new_direct_domains, "direct")
    add_rule(config, new_proxy_ips, new_proxy_domains, "proxy")
    add_rule(config, new_block_ips, new_block_domains, "block")

with open("new_keys.txt", "w", encoding="utf-8") as f:
    for config in configs:
        json_string = json.dumps(config, separators=(",", ":"), ensure_ascii=False)
        line = f"`{json_string}`\n"
        f.write(line)

print("--------------------------------")
print("Настройки роутинга успешно обновлены и сохранены в new_keys.txt")
print("--------------------------------")
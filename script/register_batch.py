#!/usr/bin/env python3
# coding: utf-8
"""
Автоматическая регистрация WhatsApp через SMS-Activate.org
Автоматический выбор страны, где есть номера
"""


import os, sys, time, re, requests, logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conf.constants import SysVar
SysVar.loadConfig()  # <-- инициализация путей и конфигов

from yowsup.registration.coderequest import WACodeRequest
from yowsup.registration.regrequest import WARegRequest
from yowsup.config.v1.config import Config

# ---------------- CONFIG ----------------
API_KEY = "64d77ffBcfec678398B1467547eB5e32"  # <-- вставь сюда API-ключ SMS-Activate
API_URL = "https://api.sms-activate.org/stubs/handler_api.php"
SERVICE = "wa"
OPERATOR = "any"

# https://api.sms-activate.org/stubs/handler_api.php?
# https://api.sms-activate.org/stubs/handler_api.php?api_key=64d77ffBcfec678398B1467547eB5e32&action=getNumber&country=22&service=wa&operator=any
# ----------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whatsapp_reg")

class Utils:
    """Stub replacement for missing Utils.getLGLC"""
    @staticmethod
    def getLGLC(cc: str):
        """
        Returns language and country code based on calling code.
        Example: 7 -> (ru, RU), 91 -> (en, IN)
        """
        mapping = {
            "7": ("ru", "RU"),
            "1": ("en", "US"),
            "91": ("en", "IN"),
            "55": ("pt", "BR"),  # Brazil
            "43": ("tr", "TR"),
            "6": ("id", "ID"),
            "79": ("en", "KE"),
            "161": ("en", "NG")
        }
        return mapping.get(str(cc), ("en", "US"))

class DummyDeviceEnv:
    """Minimal fake device environment"""
    def __init__(self):
        self.os_name = "Android"
        self.os_version = "12"
        self.device = "Pixel 7"
        self.manufacturer = "Google"
    def getOSName(self):
        return self.os_name
    def getOSVersion(self):
        return self.os_version


class DummyEnv:
    """Wrapper providing .deviceEnv like in real YowEnvironment"""
    def __init__(self):
        self.deviceEnv = DummyDeviceEnv()


def get_available_country():
    return 73


def get_number(country):
    """Создает заказ на номер для WhatsApp"""
    logger.info(f"Пробую получить номер для страны ID={country}...")
    resp = requests.get(API_URL, params={
        "api_key": API_KEY,
        "action": "getNumber",
        "service": SERVICE,
        "country": country,
        "operator": OPERATOR
    })
    text = resp.text.strip()
    if text.startswith("ACCESS_NUMBER"):
        _, activation_id, phone = text.split(":")
        logger.info(f"Получен номер {phone}, activation_id={activation_id}")
        return activation_id, phone
    else:
        logger.error(f"Ошибка получения номера: {text}")
        return None, None


def set_status(activation_id, status):
    """Устанавливает статус заказа (1=ожидание, 3=готово, 6=ошибка и т.д.)"""
    try:
        requests.get(API_URL, params={
            "api_key": API_KEY,
            "action": "setStatus",
            "id": activation_id,
            "status": status
        })
    except Exception as e:
        logger.warning(f"Не удалось установить статус: {e}")


def wait_for_code(activation_id, timeout=180):
    """Ожидает код из SMS"""
    code_pattern = re.compile(r"\b\d{4,6}\b")
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(API_URL, params={
            "api_key": API_KEY,
            "action": "getStatus",
            "id": activation_id
        })
        text = resp.text.strip()
        if text.startswith("STATUS_OK"):
            match = code_pattern.search(text)
            if match:
                code = match.group(0)
                logger.info(f"Получен код: {code}")
                set_status(activation_id, 6)
                return code
        elif text.startswith("STATUS_WAIT_CODE"):
            logger.info("Код пока не пришёл...")
        elif text.startswith("STATUS_CANCEL"):
            logger.error("Активация отменена оператором.")
            return None
        else:
            logger.debug(text)
        time.sleep(5)
    logger.error("Таймаут ожидания кода.")
    return None


def make_config(phone):
    """Создает минимальный Config для запроса WhatsApp"""
    cc = phone[0] if not phone.startswith("7") else "7"
    return Config(phone=phone, cc=cc, id=None, pushname="SMSActivateReg", login=None)


def request_code(cfg):
    """Запрашивает код у WhatsApp"""
    env = DummyEnv()
    req = WACodeRequest("sms", cfg, env)
    ok, result = req.rawSend(preview=False)
    logger.info(f"Ответ на запрос кода: {result}")
    return ok, result


def confirm_code(cfg, code):
    """Подтверждает регистрацию"""
    req = WARegRequest(cfg, code)
    try:
        result = req.send(preview=False)
        logger.info(f"Регистрация завершена: {result}")
        return True, result
    except Exception as e:
        logger.exception("Ошибка подтверждения регистрации")
        return False, str(e)


def main():
    country = get_available_country()
    if not country:
        logger.error("Нет доступных стран для регистрации.")
        return

    activation_id, phone = get_number(country)
    if not activation_id:
        return

    set_status(activation_id, 1)  # готов к приему SMS
    cfg = make_config(phone)

    ok, res = request_code(cfg)
    if not ok:
        logger.error(f"Не удалось запросить код у WhatsApp: {res}")
        set_status(activation_id, 8)
        return

    code = wait_for_code(activation_id)
    if not code:
        logger.error("Код не получен, отменяем активацию.")
        set_status(activation_id, 8)
        return

    confirm_code(cfg, code)
    logger.info("✅ Процесс регистрации завершён.")


if __name__ == "__main__":
    main()

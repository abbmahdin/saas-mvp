#!/usr/bin/env python3
"""
Telegram Notifier - Service Python pour envoi de notifications Telegram.
Partagé par tous les micro-produits du SaaS MVP.
"""

import os
import json
import logging
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Client pour envoyer des messages via le bot Telegram."""

    BASE_URL = "https://api.telegram.org/bot{token}/{method}"

    def __init__(
        self,
        token: Optional[str] = None,
        chat_id: Optional[str] = None,
        parse_mode: str = "HTML"
    ):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.parse_mode = parse_mode

        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN requis")
        if not self.chat_id:
            raise ValueError("TELEGRAM_CHAT_ID requis")

        logger.info(f"Notifier initialisé (chat_id={self.chat_id}, mode={self.parse_mode})")

    def _call_api(self, method: str, payload: dict) -> dict:
        """Appel API Telegram générique."""
        url = self.BASE_URL.format(token=self.token, method=method)
        data = json.dumps(payload).encode("utf-8")
        req = Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            error_body = e.read().decode("utf-8")[:200]
            logger.error(f"HTTP {e.code}: {error_body}")
            return {"ok": False, "error_code": e.code, "description": error_body}
        except URLError as e:
            logger.error(f"URL Error: {e.reason}")
            return {"ok": False, "error": str(e.reason)}
        except Exception as e:
            logger.error(f"Exception: {e}")
            return {"ok": False, "error": str(e)}

    def send(self, text: str, parse_mode: Optional[str] = None, disable_notification: bool = False) -> dict:
        """Envoyer un message texte."""
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode or self.parse_mode,
            "disable_notification": disable_notification,
        }
        result = self._call_api("sendMessage", payload)
        if result.get("ok"):
            logger.info(f"Message envoyé à {self.chat_id}")
        return result

    def send_html(self, html: str, **kwargs) -> dict:
        """Envoyer un message formaté HTML."""
        return self.send(html, parse_mode="HTML", **kwargs)

    def send_markdown(self, md: str, **kwargs) -> dict:
        """Envoyer un message formaté Markdown."""
        return self.send(md, parse_mode="MarkdownV2", **kwargs)

    def send_alert(self, emoji: str, title: str, body: str) -> dict:
        """Envoyer une alerte formatée."""
        text = f"{emoji} <b>{title}</b>\n<code>{body}</code>"
        return self.send_html(text)

    def send_payment(self, amount: float, currency: str = "€", product: str = "") -> dict:
        """Notifier un paiement reçu."""
        text = (
            f"💰 <b>Paiement reçu</b>\n"
            f"Montant: <code>{amount} {currency}</code>\n"
            f"Produit: {product or 'N/A'}"
        )
        return self.send_html(text)

    def send_error(self, error_msg: str, service: str = "") -> dict:
        """Notifier une erreur."""
        text = (
            f"🚨 <b>Erreur</b>\n"
            f"Service: {service or 'N/A'}\n"
            f"Message: <code>{error_msg}</code>"
        )
        return self.send_html(text)

    def send_health_report(self, services: list[dict]) -> dict:
        """Envoyer un rapport de santé formaté."""
        lines = ["📊 <b>Rapport santé</b>\n"]
        for svc in services:
            icon = "✅" if svc.get("status") == "up" else "❌"
            lines.append(f"{icon} {svc.get('name', '?')}: <code>{svc.get('status', '?')}</code>")
        return self.send_html("\n".join(lines))

    def get_bot_info(self) -> dict:
        """Récupérer les infos du bot."""
        return self._call_api("getMe", {})


def main():
    """Test rapide."""
    notifier = TelegramNotifier()
    info = notifier.get_bot_info()
    logger.info(f"Bot info: {info}")
    notifier.send("🤖 SaaS Telegram Notifier prêt!")


if __name__ == "__main__":
    main()

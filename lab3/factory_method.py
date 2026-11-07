from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailChannel(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"[SMTP] Письмо отправлено на {recipient}: '{message}'")


class TelegramChannel(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"[Telegram Bot API] Сообщение отправлено пользователю @{recipient}: '{message}'")


class NotificationService(ABC):
    @abstractmethod
    def create_channel(self) -> NotificationChannel:
        pass

    def notify_user(self, recipient: str, message: str) -> None:
        channel = self.create_channel()
        print(f"[Audit Log] Инициация доставки уведомления...")
        channel.send(recipient, message)


class EmailNotificationService(NotificationService):
    def create_channel(self) -> NotificationChannel:
        return EmailChannel()


class TelegramNotificationService(NotificationService):
    def create_channel(self) -> NotificationChannel:
        return TelegramChannel()


def main() -> None:
    service_email = EmailNotificationService()
    service_email.notify_user("dev@company.com", "Прод пятисотит!")

    print()

    service_tg = TelegramNotificationService()
    service_tg.notify_user("dev_lead", "База данных снова доступна")


if __name__ == "__main__":
    main()
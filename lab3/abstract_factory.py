from abc import ABC, abstractmethod

class RecipientValidator(ABC):
    @abstractmethod
    def validate(self, recipient: str) -> bool:
        pass


class MessageFormatter(ABC):
    @abstractmethod
    def format(self, title: str, body: str) -> str:
        pass


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, formatted_message: str) -> None:
        pass


class EmailValidator(RecipientValidator):
    def validate(self, recipient: str) -> bool:
        return "@" in recipient and "." in recipient


class HtmlEmailFormatter(MessageFormatter):
    def format(self, title: str, body: str) -> str:
        return f"<html><body><h1>{title}</h1><p>{body}</p></body></html>"


class EmailChannel(NotificationChannel):
    def send(self, recipient: str, formatted_message: str) -> None:
        print(f"[SMTP] Отправка на {recipient}:\n{formatted_message}")


class TelegramValidator(RecipientValidator):
    def validate(self, recipient: str) -> bool:
        return recipient.startswith("@") and len(recipient) > 3


class MarkdownTelegramFormatter(MessageFormatter):
    def format(self, title: str, body: str) -> str:
        return f"**{title}**\n_{body}_"


class TelegramChannel(NotificationChannel):
    def send(self, recipient: str, formatted_message: str) -> None:
        print(f"[Telegram API] Отправка для {recipient}:\n{formatted_message}")


class NotificationFactory(ABC):
    @abstractmethod
    def create_validator(self) -> RecipientValidator:
        pass

    @abstractmethod
    def create_formatter(self) -> MessageFormatter:
        pass

    @abstractmethod
    def create_channel(self) -> NotificationChannel:
        pass


class EmailNotificationFactory(NotificationFactory):
    def create_validator(self) -> RecipientValidator:
        return EmailValidator()

    def create_formatter(self) -> MessageFormatter:
        return HtmlEmailFormatter()

    def create_channel(self) -> NotificationChannel:
        return EmailChannel()


class TelegramNotificationFactory(NotificationFactory):
    def create_validator(self) -> RecipientValidator:
        return TelegramValidator()

    def create_formatter(self) -> MessageFormatter:
        return MarkdownTelegramFormatter()

    def create_channel(self) -> NotificationChannel:
        return TelegramChannel()

class NotificationService:
    def __init__(self, factory: NotificationFactory) -> None:
        self._validator = factory.create_validator()
        self._formatter = factory.create_formatter()
        self._channel = factory.create_channel()

    def notify(self, recipient: str, title: str, body: str) -> None:
        if not self._validator.validate(recipient):
            print(f"[Ошибка] Некорректный получатель: {recipient}")
            return

        payload = self._formatter.format(title, body)
        self._channel.send(recipient, payload)


def main():
    email_service = NotificationService(EmailNotificationFactory())
    email_service.notify("dev@company.com", "Оповещение", "Прод пятисотит!")

    print("-" * 40)

    tg_service = NotificationService(TelegramNotificationFactory())
    tg_service.notify("@dev_lead", "Статус", "База данных снова доступна")


if __name__ == "__main__":
    main()

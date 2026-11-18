from abc import ABC, abstractmethod
from typing import Optional


class SupportHander(ABC):
    def __init__(self):
        self._next_handler: Optional[SupportHander] = None

    def set_next(self, handler: SupportHander) -> SupportHander:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle_issue(self, level: int, description: str) -> None:
        if self._next_handler:
            self._next_handler.handle_issue(level, description)
        else:
            print(f"Обращение не решено. Описание: {description}, уровень: {level}")


class ChatBotHandler(SupportHander):
    def handle_issue(self, level: int, description: str) -> None:
        if level == 1:
            print(f"[Чат-бот] Вопрос решён. Описание: {description}.")
        else:
            super().handle_issue(level, description)


class JuniorSupportOperatorHandler(SupportHander):
    def handle_issue(self, level: int, description: str) -> None:
        if level == 2:
            print(f"[Оператор 1-й линии] Вопрос решён. Описание: {description}.")
        else:
            super().handle_issue(level, description)


class SeniorSupportOperatorHandler(SupportHander):
    def handle_issue(self, level: int, description: str) -> None:
        if level == 3:
            print(f"[Старший специалист поддержки] Вопрос решён. Описание: {description}. ")
        else:
            super().handle_issue(level, description)

class DeveloperSupportHandler(SupportHander):
    def handle_issue(self, level: int, description: str) -> None:
        if level == 4:
            print(f"[Команда разработки] Проблема устранена. Описание: {description}.")
        else:
            super().handle_issue(level, description)


bot = ChatBotHandler()
junior_operator = JuniorSupportOperatorHandler()
senior_operator = SeniorSupportOperatorHandler()
dev_team = DeveloperSupportHandler()

bot.set_next(junior_operator).set_next(senior_operator).set_next(dev_team)

bot.handle_issue(1, "Как узнать сумму задолженности?")
bot.handle_issue(2, "Не проходит оплата картой.")
bot.handle_issue(3, "Аккаунт был заблокирован после смены региона.")
bot.handle_issue(4, "При создании отчёта о тратах возникает ошибка 500.")


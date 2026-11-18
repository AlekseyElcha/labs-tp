from abc import ABC, abstractmethod
from collections.abc import Iterator, Iterable
from typing import List


class Ticket:
    def __init__(self, ticket_id: int, title: str, priority: int):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority # 1 - низкий, 2 - средний, 3 - высокий

    def __str__(self):
        return f"#{self.ticket_id} | Заголовок: {self.title} | Приоритет: {self.priority}"

class TicketQueueIterator(Iterator):
    def __init__(self, tickets: List[Ticket], by_priority: bool = False):
        if by_priority:
            self._tickets = sorted(tickets, key=lambda ticket: ticket.priority, reverse=True)
        else:
            self._tickets = tickets
        self._index = 0

    def __next__(self) -> Ticket:
        if self._index >= len(self._tickets):
            raise StopIteration
        ticket = self._tickets[self._index]
        self._index += 1
        return ticket

class TicketQueue(Iterable):
    def __init__(self):
        self._tickets: List[Ticket] = []

    def add_ticket(self, ticket: Ticket) -> None:
        self._tickets.append(ticket)

    # стандартный итератор
    def __iter__(self) -> TicketQueueIterator:
        return TicketQueueIterator(self._tickets, by_priority=False)

    # итератор с учётом срочности обращения
    def get_priority_iterator(self) -> TicketQueueIterator:
        return TicketQueueIterator(self._tickets, by_priority=True)


queue = TicketQueue()
queue.add_ticket(Ticket(ticket_id=1, title="Как скачать отчёт за прошлый месяц?", priority=1))
queue.add_ticket(Ticket(ticket_id=2, title="Произошло двойное списание средств с карты за подписку.", priority=3))
queue.add_ticket(Ticket(ticket_id=3, title="Хочу сменить тарифный план со следующего месяца.", priority=1))
queue.add_ticket(Ticket(ticket_id=4, title="Мой аккаунт был заблокирован после смены региона.", priority=3))
queue.add_ticket(Ticket(ticket_id=5, title="Не приходит сообщение на электронную почту с кодом подтверждения операции", priority=2))

print("Обычный обход по очереди - порядку поступления обращений:")
for ticket in queue:
    print(f">> обращение в обработку: {ticket}")

print("---"*45)

print("Приоритетный обход обращений (по убыванию срочности):")
for ticket in queue.get_priority_iterator():
    print(f">> обращение в обработку: {ticket}")


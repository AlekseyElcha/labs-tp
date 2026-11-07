from abc import ABC, abstractmethod


class Attacker(ABC):
    @abstractmethod
    def attack(self, unit: 'Unit') -> None:
        pass


class Moveable(ABC):
    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass


class GameObject(ABC):
    def __init__(self, id: int, name: str, x: int, y: int) -> None:
        self._id = id
        self._name = name
        self._x = x
        self._y = y

    def getId(self) -> int:
        return self._id

    def getName(self) -> str:
        return self._name

    def getX(self) -> int:
        return self._x

    def getY(self) -> int:
        return self._y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}', pos=({self._x}, {self._y}))"


class Unit(GameObject):
    def __init__(self, id: int, name: str, x: int, y: int, hp: float = 100.0) -> None:
        super().__init__(id, name, x, y)
        self._hp = float(hp)

    def isAlive(self) -> bool:
        return self._hp > 0

    def getHp(self) -> float:
        return self._hp

    def receiveDamage(self, damage: float) -> None:
        self._hp = max(0.0, self._hp - damage)

    def __repr__(self) -> str:
        status = "Жив" if self.isAlive() else "Мертв"
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}', hp={self._hp:.1f}, статус={status})"


class Archer(Unit, Attacker, Moveable):
    def __init__(self, id: int, name: str, x: int, y: int, hp: float = 80.0, damage: float = 20.0) -> None:
        super().__init__(id, name, x, y, hp=hp)
        self._damage = damage

    def attack(self, unit: Unit) -> None:
        if self.isAlive() and unit.isAlive():
            unit.receiveDamage(self._damage)

    def move(self, x: int, y: int) -> None:
        if self.isAlive():
            self._x, self._y = x, y


class Building(GameObject):
    def __init__(self, id: int, name: str, x: int, y: int, is_built: bool = False) -> None:
        super().__init__(id, name, x, y)
        self._is_built = is_built

    def isBuilt(self) -> bool:
        return self._is_built

    def __repr__(self) -> str:
        status = "Построено" if self._is_built else "Строится"
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}', статус={status})"


class Fort(Building, Attacker):
    def __init__(self, id: int, name: str, x: int, y: int, damage: float = 50.0, is_built: bool = True) -> None:
        super().__init__(id, name, x, y, is_built=is_built)
        self._damage = damage

    def attack(self, unit: Unit) -> None:
        if self.isBuilt() and unit.isAlive():
            unit.receiveDamage(self._damage)


class MobileHouse(Building, Moveable):
    def move(self, x: int, y: int) -> None:
        self._x, self._y = x, y


def main() -> None:
    legolas = Archer(id=1, name="Леголас", x=10, y=20, hp=100.0, damage=25.0)
    enemy_warrior = Unit(id=2, name="Вражеский воин", x=12, y=20, hp=80.0)
    citadel = Fort(id=3, name="Цитадель", x=50, y=50, damage=40.0, is_built=True)
    wagon = MobileHouse(id=4, name="Фургон кочевников", x=0, y=0, is_built=True)

    print(f"Создан лучник: {legolas}")
    print(f"Создан противник: {enemy_warrior}")
    print(f"Построена крепость: {citadel}")
    print(f"Построен дом на колесах: {wagon}")
    print()

    print(f"Координаты лучника до перемещения: ({legolas.getX()}, {legolas.getY()})")
    legolas.move(15, 25)
    print(f"Координаты лучника после move(15, 25): ({legolas.getX()}, {legolas.getY()})")

    print(f"Координаты дома до перемещения: ({wagon.getX()}, {wagon.getY()})")
    wagon.move(5, 5)
    print(f"Координаты дома после move(5, 5): ({wagon.getX()}, {wagon.getY()})")
    print()

    print(f"HP противника до атаки лучника: {enemy_warrior.getHp()} (Жив: {enemy_warrior.isAlive()})")
    legolas.attack(enemy_warrior)
    print(f"Лучник атаковал! HP противника: {enemy_warrior.getHp()}")

    print("Крепость производит выстрел по противнику...")
    citadel.attack(enemy_warrior)
    print(f"HP противника после выстрела форта: {enemy_warrior.getHp()}")

    print("Крепость производит добивающий выстрел...")
    citadel.attack(enemy_warrior)
    print(f"HP противника: {enemy_warrior.getHp()} (Жив: {enemy_warrior.isAlive()})")
    print()

    print("--- Проверка полиморфизма ---")
    attackers: list[Attacker] = [legolas, citadel]
    test_target = Unit(id=99, name="Тренировочная цель", x=10, y=10, hp=100.0)

    for attacker in attackers:
        if isinstance(attacker, GameObject):
            print(f"Атакует {attacker.getName()}...")
        attacker.attack(test_target)
        print(f"Здоровье манекена: {test_target.getHp()}")


if __name__ == "__main__":
    main()

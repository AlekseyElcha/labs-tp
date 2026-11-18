from abc import abstractmethod, ABC
from os import name


class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, order_weight: float, distance_km: float) -> float:
        pass


class CourierShipping(ShippingStrategy):
    def calculate_price(self, order_weight: float, distance_km: float) -> float:
        return (order_weight * 20) + (distance_km * 10) + 500


class PostalShipping(ShippingStrategy):
    def calculate_price(self, order_weight: float, distance_km: float) -> float:
        return (order_weight * 10) + 200


class PickupPointShipping(ShippingStrategy):
    def calculate_price(self, order_weight: float, distance_km: float) -> float:
        return 0


class Order:
    def __init__(self, weight: float, distance: float, strategy: ShippingStrategy):
        self.order_weight = weight
        self.distance = distance
        self._strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy) -> None:
        self._strategy = strategy

    def get_total_shipping_cost(self) -> float:
        return self._strategy.calculate_price(
            self.order_weight,
            self.distance
        )

order = Order(weight=5.5, distance=15.0, strategy=CourierShipping())
print(f"Доставка курьером: {order.get_total_shipping_cost()} руб.")

order.set_strategy(PostalShipping())
print(f"Доставка по почте: {order.get_total_shipping_cost()} руб.")

order.set_strategy(PickupPointShipping())
print(f"Самовывоз из ПВЗ: {order.get_total_shipping_cost()} руб.")

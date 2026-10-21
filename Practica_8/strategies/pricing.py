class StandardPricing:

    def calculate_price(self, base_price: float) -> float:
        return base_price


class DiscountPricing:

    def calculate_price(self, base_price: float) -> float:
        return base_price * 0.8


class UrgentPricing:

    def calculate_price(self, base_price: float) -> float:
        return base_price * 1.5

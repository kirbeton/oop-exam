from datetime import datetime
import random


# ===================== Order Item ===================== פרטים על ההזמנה
class OrderItem:
    def __init__(self, item_id, name, price):
        self.id = item_id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.name} ({self.price}₪)" #מגדירה איך האובייקט ייצא כשמדפיסים בטקסט לדוגמא : laptop", (4000₪)


# ===================== Gift =====================
class Gift:
    def open_gift(self):
        print("Congratulations! you got a new gift! Enjoy!")

# ===================== Product Gift =====================
class ProductGift(Gift):
    def __init__(self, product_name):
        self.product_name = product_name

    def open_gift(self):
        print(f"Congratulations! You got a free product: {self.product_name}! Enjoy!")


# ===================== Customer ===================== פרטי הלקוח
class Customer:

    POSSIBLE_GIFTS = ["Wireless Mouse", "Laptop Bag", "USB Drive", "Headphones"] # מנגון שאני הוספתי שנותןם ללקוח לקבל מתנה רנדומלית מהרשימה בכך יגרום לו יותר להתרגש מהמתנה

    def __init__(self, customer_id, first_name, last_name, email, address, customer_type):
        self.id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.customer_type = customer_type  # REGULAR / VIP
        self.favorite_items = []
        self.gift = None

    def add_favorite_item(self, item):
        # מניעת כפילות לפי שם פריט
        if item.name not in [fav.name for fav in self.favorite_items]:
            self.favorite_items.append(item)

    def remove_favorite_item(self, item_name):
        self.favorite_items = [item for item in self.favorite_items if item.name != item_name]

    # מנגנון פתיחת מתנות אם היה קבלה של מתנה
    def take_gift(self, gift):
        self.gift = gift

    def open_gift(self):
        if self.gift:
            self.gift.open_gift()
        else:
            print("No gift to open.")

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_type})" # שוב פעם לתת טקסט יותר נוח וקריא למשתמש או לעסק


# ===================== Order Base Class =====================
class Order:
    def __init__(self, order_id, name, address, items, customer, payment_type, order_date=None):
        self.id = order_id
        self.name = name
        self.address = address
        self.items = items
        self.customer = customer
        self.payment_type = payment_type
        self.order_date = order_date if order_date else datetime.now() # בדיקת זמן ההזמנה המדויק
        self.total_price = self.calculate_total_price()

        #   הוספת כל הפריטים לרשימת המועדפים של הלקוח ללא כפילויות
        for item in items:
            self.customer.add_favorite_item(item)
    # חישוב הסכום הכולל של הלקוח
    def calculate_total_price(self):
        return sum(item.price for item in self.items)

    def __repr__(self):
        return f"Order #{self.id} for {self.customer} - Total: {self.total_price}₪"


# ===================== Regular Order =====================
class RegularOrder(Order):
    def calculate_total_price(self):
        return super().calculate_total_price()


# ===================== VIP Order =====================
# לקוח VIP נהנה מהנחה של 10%
class VIPOrder(Order):
    def calculate_total_price(self):
        if self.customer.customer_type != "VIP":
            raise ValueError("VIP order must be made by a VIP customer!")
        total = super().calculate_total_price()
        discount = 0.10  # 10% הנחה מהסכום הכולל
        return total * (1 - discount)


# ===================== Example Usage =====================
# בדיקה
if __name__ == "__main__":
    # יצירת פריטים
    item1 = OrderItem(1, "Laptop", 4000)
    item2 = OrderItem(2, "Mouse", 100)
    item3 = OrderItem(3, "Keyboard", 300)

    # יצירת לקוחות
    cust1 = Customer(101, "David", "Cohen", "david@example.com", "Tel Aviv", "REGULAR")
    cust2 = Customer(102, "Dana", "Levi", "dana@example.com", "Jerusalem", "VIP")

    # הזמנה רגילה
    order1 = RegularOrder(201, "Office Equipment", "Tel Aviv", [item1, item2], cust1, "CASH")
    print(order1)

    # הזמנת VIP
    order2 = VIPOrder(202, "Gaming Setup", "Jerusalem", [item1, item3], cust2, "CREDIT CARD")
    print(order2)

    # מתנה
    gift = Gift()
    cust2.take_gift(gift)
    cust2.open_gift()

    # הצגת מועדפים
    print("Dana's favorites:", [item.name for item in cust2.favorite_items])
    print("David's favorites:", [item.name for item in cust1.favorite_items])

from abc import ABC, abstractmethod


from abc import ABC, abstractmethod

# ===================== Abstract Animal =====================
class Animal(ABC):
    def __init__(self, legs: int):
        self.legs = legs

    def walk(self):
        print(f"This animal walks on {self.legs} legs.")

    @abstractmethod
    def eat(self):
        pass


# ===================== Interface Pet =====================
class Pet(ABC):
    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def setName(self, name: str):
        pass

    @abstractmethod
    def play(self):
        pass


# ===================== Spider =====================
class Spider(Animal):
    def __init__(self):
        super().__init__(legs=8)# לעכביש יש 8 רגליים

    def eat(self):
        print("The spider eats insects.")


# ===================== Cat =====================
class Cat(Animal, Pet):
    def __init__(self, name: str):
        super().__init__(legs=4)
        self.name = name

    def getName(self) -> str:
        return self.name

    def setName(self, name: str):
        self.name = name

    def play(self):
        print(f"{self.name} is playing with a ball.")

    def eat(self):
        print(f"{self.name} is eating fish.")


# ===================== Fish =====================
class Fish(Animal, Pet):
    def __init__(self, name: str):
        super().__init__(legs=0)  # דג אין לו רגליים
        self.name = name

    def getName(self) -> str:
        return self.name

    def setName(self, name: str):
        self.name = name

    def play(self):
        print(f"{self.name} is swimming around happily.")

    def walk(self):
        print(f"{self.name} cannot walk, but can swim.")

    def eat(self):
        print(f"{self.name} is eating algae.")


# ===================== Test Code =====================
if __name__ == "__main__":
    # בדיקה של Spider
    spider = Spider()
    spider.walk()
    spider.eat()

    print("-" * 40)

    # בדיקה של Cat
    cat = Cat("Whiskers")
    cat.walk()
    print(cat.getName())
    cat.play()
    cat.eat()
    cat.setName("Mittens")
    print(cat.getName())

    print("-" * 40)

    # בדיקה של Fish
    fish = Fish("Nemo")
    fish.walk()
    fish.play()
    fish.eat()
    print(fish.getName())




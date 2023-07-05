class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self):
        # Логика использования предмета
        pass


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.characters = []
        self.puzzles = []
        self.items = []
        self.exits = {}

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)

    def add_puzzle(self, puzzle):
        self.puzzles.append(puzzle)

    def remove_puzzle(self, puzzle):
        self.puzzles.remove(puzzle)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def add_exit(self, direction, location):
        self.exits[direction] = location

    def get_exit(self, direction):
        return self.exits.get(direction)


class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def talk(self, message):
        print(f"{self.name}: {message}")

    def move(self, location):
        location.add_character(self)


class Animal(Character):
    def __init__(self, name, description, location):
        super().__init__(name, description)
        self.location = location

    def interact(self):
        print(f"{self.name}: Ты забрал меня с собой, милый путник, спасибо. Теперь мы путешествуем вместе!")


class Player(Character):
    def __init__(self, name, description, location):
        super().__init__(name, description)
        self.location = location
        self.inventory = []

    def move(self, direction):
        new_location = self.location.get_exit(direction)
        if new_location:
            self.location.remove_character(self)
            new_location.add_character(self)
            self.location = new_location
            print(f"Вы перешли в локацию. {new_location.name}.")
            self.look_around()
        else:
            print("В этом направлении нет выхода.")

    def look_around(self):
        print(self.location.description)
        print("Персонажи в этой локации:")
        for character in self.location.characters:
            print(f"- {character.name}")
        print("Предметы в этой локации:")
        for item in self.location.items:
            print(f"- {item.name}")

    def take_item(self, item):
        self.inventory.append(item)
        self.location.remove_item(item)
        print(f"Вы взяли {item.name}.")

    def use_item(self, item):
        if item in self.inventory:
            item.use()
        else:
            print(f"У вас нет {item.name} в вашем инвентаре.")

    def talk_to_character(self, character):
        if isinstance(character, Animal):
            character.talk("Мяу.")
            return True
        elif character in self.location.characters and character != cat:
            character.talk(self)
            return True
        return False

    def show_inventory(self):
        if self.inventory:
            print("Инвентарь:")
            for item in self.inventory:
                print(f"- {item.name}")
        else:
            print("Ваш инвентарь пуст.")


class Puzzle:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def solve(self, answer):
        if answer.lower() == self.answer.lower():
            return True
        else:
            return False

class NPC1(Character):
    def __init__(self, name, description, location):
        super().__init__(name, description)
        self.location = location

    def talk(self, player):
            print("Добро пожаловать, хорошей игры!")

class NPC2(Character):
    def __init__(self, name, description, location):
        super().__init__(name, description)
        self.location = location

    def talk(self, player):
        book = Item("Книга", "Старинная книга заклинаний.")
        if book not in player.inventory:
            print(" О, ты проделал такой путь и я точно знаю, что тебе нужно. У меня есть книга для тебя.")
            print(" Ответь на мой вопрос и она твоя.")
            puzzle = self.location.puzzles[0]
            print(puzzle.question)
            answer = input("Твой ответ: ")
            if puzzle.solve(answer):
                player.take_item(book)
            else:
                print("Это неправильный ответ, подумай ещё.")
        else:
            print("Не будь наглым, ты уже получил свой приз.")


class NPC3(Character):
    def talk(self, player):
        print("В последнее время я чувствую себя очень подавлено. Хотелось бы мне, чтобы что-нибудь могло меня подбодрить.")
        book = Item("Книга", "Старинная книга заклинаний.")
        if book in player.inventory:
            player.location.characters.remove(npc3)
            print("У тебя есть книга! Я люблю заклинания. Спасибо!")
            print("Поздравляю! Вы прошли игру и победили!")  # Вывод сообщения о победе
        else:
            print("У тебя нет ничего, что могло бы меня подбодрить. Я зол.")
            print("Предлагаю тебе игру. Я загадываю число от 1 до 10.")
            print("У тебя есть 3 попытки угадать его. Удачи!")

            number = random.randint(1, 10)
            attempts = 3
            while attempts > 0:
                guess = int(input("Your guess: "))
                if guess == number:
                    player.location.characters.remove(npc3)
                    print("Поздравляю! Ты угадал!")
                    print("Поздравляю! Вы прошли игру и победили!")  # Вывод сообщения о победе
                    break  # Игра завершается, игрок победил
                else:
                    print("Это не то число, которое я загадал.")
                    attempts -= 1
                    if attempts > 0:
                        print(f"NPC3: У тебя осталось {attempts} попытки/а.")
            else:
                print("Ты не отгадал число. Я выиграл!")
                print("Игра окончена. Ты проиграл.")  # Вывод сообщения о проигрыше


# Создание локаций
kitchen = Location("Кухня", "Маленькая и аккуратная кухня")
bedroom = Location("Спальня", "Уютная спальня с большой кроватью.")
garden = Location("Сад", "Через ворота виднеется красивый сад с прекрасными цветами.")
hallway = Location("Холл", "Длинный холл, соединяющий много комнат")
living_room = Location("Гостинная", "Обычная гостинная")
dining_room = Location("Столовая", "Тут стоит оггромный стол")

# Создание персонажей
player = Player("Игрок", "Игрок - это ты.", kitchen)
npc1 = NPC1("NPC1", "Улыбающаяся девушка.", kitchen)
npc2 = NPC2("NPC2", "Мужчина в мантии с бородой.", garden)
npc3 = NPC3("NPC3", "Недовольный мужчина, ростом метра два.")
cat = Animal("Кот", "Вислоухий трехцветный кот.", bedroom)

# Создание предметов
key = Item("Ключ", "Золотой ключик.")
book = Item("Книга", "Старинная книга заклинаний.")

# Добавление персонажей в локации
kitchen.add_character(player)
kitchen.add_character(npc1)
garden.add_character(npc2)
dining_room.add_character(npc3)
bedroom.add_character(cat)

# Добавление предметов в локации
kitchen.add_item(key)

# Добавление выходов между локациями
kitchen.add_exit("север", hallway)
bedroom.add_exit("юг", hallway)
hallway.add_exit("север", bedroom)
hallway.add_exit("юг", kitchen)
hallway.add_exit("восток", garden)
garden.add_exit("запад", hallway)
hallway.add_exit("запад", living_room)
living_room.add_exit("восток", hallway)
living_room.add_exit("юг", dining_room)
dining_room.add_exit("север", living_room)

# Создание головоломки
puzzle2 = Puzzle("Число Пи?", "3,14")

# Добавление головоломки в локацию
garden.add_puzzle(puzzle2)

import random

# Основной игровой цикл
while True:
    player.look_around()

    # Диалог с NPC2
    player.talk_to_character(npc2)
    if npc2.location == player.location:
        if player.talk_to_character(npc2):
            npc2.talk(player)

    # Диалог с NPC3
    player.talk_to_character(npc3)
    if npc3 in player.location.characters:
        if player.talk_to_character(npc3):
            npc3.talk(player)

    # Получение команды от игрока
    while True:
        command = input("Введи команду (напишите 'help' для получения доступных комманд): ").lower().split()
        if command[0] == "move":
            if len(command) < 2:
                print("Выбери направление движения(север, юг, запад, восток).")
            else:
                direction = command[1]
                player.move(direction)
        elif command[0] == "look":
            player.look_around()
        elif command[0] == "take":
            if len(command) < 2:
                print("Выбери предмет или персонажа, который/ого хочешь взять.")
            else:
                item_name = " ".join(command[1:])
                item = None
                for location_item in player.location.items:
                    if location_item.name.lower() == item_name:
                        item = location_item
                        break
                if not item:
                    for location_character in player.location.characters:
                        if location_character.name.lower() == item_name:
                            item = location_character
                            break

                if item:
                    if isinstance(item, Item):
                        player.take_item(item)
                        print(f"Вы взяли {item.name}.")
                    elif isinstance(item, Character):
                        if item == cat:
                            player.take_item(item)
                            print("Кот очень напуган, но ты забрал его с собой.")
                        else:
                            print(f"Вы не можете взять персонажа {item.name}.")
                else:
                    print("Предмет или персонаж не найден.")

        elif command[0] == "use":
            if len(command) < 2:
                print("Выбери предмет, который хочешь использовать.")
            else:
                item_name = " ".join(command[1:])
                item = None
                for inventory_item in player.inventory:
                    if inventory_item.name.lower() == item_name:
                        item = inventory_item
                        break
                if item:
                    player.use_item(item)
                else:
                    print("Предмет не найден.")
        elif command[0] == "talk":
            if len(command) < 2:
                print("Выбери персонажа с которым хочешь поговорить.")
            else:
                character_name = " ".join(command[1:])
                character = None
                for location_character in player.location.characters:
                    if location_character.name.lower() == character_name:
                        character = location_character
                        break
                if character:
                    player.talk_to_character(character)
                    if character == cat:
                        print("Ты такой милый кот!")
                        print("Мяу.")
                else:
                    print("Персонаж не найдет.")
        elif command[0] == "inventory":
            player.show_inventory()
        elif command[0] == "help":
            print("Доступные команды:")
            print("- look: Осмотреться .")
            print("- inventory: Показать мой инвентарь.")
            print("- move <direction>: Перейти в другую локацию в указанном направлении.")
            print("- take <item>: Взять предмет.")
            print("- use <item>: Использовать предмет из инвенторя.")
            print("- talk <character>: Поговорить с персонажем.")
            print("- help: Показывает данное сообщение.")
            print("- quit: Выйти из игры.")
        elif command[0] == "quit":
            print("Выход из игры. Заходи ещё!")
            break
        else:
            print("Invalid command. Type 'help' for available commands.")

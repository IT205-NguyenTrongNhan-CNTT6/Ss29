from abc import ABC, abstractmethod  

class BaseCharacter(ABC):
    def __init__(self, base_hp):
        self.__base_hp = base_hp

    @property
    def base_hp(self):
        return self.__base_hp

    @abstractmethod 
    def attack_enemy(self) -> int:
        pass

    def __add__(self, other):
        total_hp = self.base_hp + other.base_hp
        return total_hp


class MagicalStance:
    def attack_enemy(self) -> float:
        return 150.0


class Warrior(BaseCharacter):
    def __init__(self, base_hp, strength):
        super().__init__(base_hp)
        self.strength = strength

    def attack_enemy(self) -> float:
        return self.strength * 2.5


class Spellblade(Warrior, MagicalStance):
    def __init__(self, base_hp, strength):
        super().__init__(base_hp, strength)

    def attack_enemy(self) -> float:
        warrior_dmg = Warrior.attack_enemy(self)  
        magical_dmg = MagicalStance.attack_enemy(self)
        return warrior_dmg + magical_dmg


class VolcanoZone:
    def activate_buff(self, character):
        print("[Duck Typing]: Xác thực môi trường trận đấu thành công!")
        print("[Volcano Zone Effect]: Sức nóng dung nham kích hoạt! Gia tăng +20% sát thương cho Warrior!")



def apply_battleground_effect(environment, character):
    environment.activate_buff(character)


def main():
    current_hero = None

    while True:
        print("\n--- RPG GAME CORE MENU ---")
        print("1. Khởi tạo Ma kiếm sĩ Spellblade & Xem cấu trúc MRO")
        print("2. Ra lệnh tấn công & Kích hoạt chiến trường (Duck Typing)")
        print("3. Thoát")

        choice = input("Chọn chức năng (1-3): ")  

        match choice:
            case "1":
                print("--- KHỞI TẠO MA KIẾM SĨ SPELLBLADE ---")
                hp = int(input("Nhập lượng máu cơ bản (HP): "))
                strength = int(input("Nhập chỉ số sức mạnh (Strength): "))

                current_hero = Spellblade(hp, strength)
                print("[Thành công]: Khởi tạo nhân vật Spellblade thành công!")
                print("[MRO Architecture]: Spellblade → Warrior → BaseCharacter → MagicalStance → object")

                total_hp = current_hero + current_hero
                print("[Overloading __add__]: Tổng HP tích lũy khi gộp đội hình:", total_hp)

            case "2":
                if current_hero == None:
                    print("[Thông báo]: Vui lòng khởi tạo nhân vật trước!")
                else:
                    print("--- THI THIẾT KẾ GIAO TRANH & DUCK TYPING ---")
                    total_dmg = current_hero.attack_enemy()
                    print("[Đa hình] Spellblade vung kiếm ma thuật gây tổng sát thương:", total_dmg, "DMG")

                    volcano_env = VolcanoZone()
                    apply_battleground_effect(volcano_env, current_hero)

            case '3':
                print("Thoát")
                break
            case _:
                print("Nhập sai, vui lòng chọn lại.")

if __name__ == "__main__":
    main()
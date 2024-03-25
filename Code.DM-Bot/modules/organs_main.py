import os

from medical.medical_enums import BreastSizeEnum, GenderEnum
from medical.organs.brain import Brain
from medical.organs.breast import Breast
from medical.organs.genitalia import Genitalia
from medical.organs.heart import Heart
from medical.organs.kidney import Kidney
from medical.organs.liver import Liver
from medical.organs.lung import Lung
from medical.organs.organs_system import OrgansSystem
from medical.organs.stomach import Stomach
from prototype_system.organ import OrganPrototypeLoader


def clear_consol():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_consol():
    input("Нажмите Enter для продолжения...")

def show_organ_main(osys: OrgansSystem):
    print("Состояние основных органов:")
    print(f"{'Орган':<15} | {'Здоровье':<10}")
    print("-" * 25)
    print(f"{osys.brain.name:<15} | {osys.brain.health:<10}")
    print(f"{osys.heart.name:<15} | {osys.heart.health:<10}")
    print(f"{osys.liver.name:<15} | {osys.liver.health:<10}")
    print(f"{osys.kidney.name:<15} | {osys.kidney.health:<10}")
    print(f"{osys.lung.name:<15} | {osys.lung.health:<10}")
    print(f"{osys.stomach.name:<15} | {osys.stomach.health:<10}")
    print(f"{osys.genitalia.name:<15} | {osys.genitalia.health:<10}")
    print(f"{osys.breast.name:<15} | {osys.breast.health:<10}")

def show_menu():
    while True:
        clear_consol()
        print("Меню выбора:")
        print("1. Показать систему органов")
        print("2. Добавить органы (WIP)")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0", "1", "2"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")
            pause_consol()

def organs_main():
    proto = OrganPrototypeLoader("for_tests")
    organ_list = proto.get_prototype()

    r_l = []
    r_l.append(organ_list["brain"])
    r_l.append(organ_list["heart"])
    r_l.append(organ_list["liver"])
    r_l.append(organ_list["kidney"])
    r_l.append(organ_list["lung"])
    r_l.append(organ_list["stomach"])
    r_l.append(organ_list["genitalia"])
    r_l.append(organ_list["breast"])
    osys = OrgansSystem(*r_l)

    while (True):
        clear_consol()
        
        menu = show_menu()
        
        if menu == 1:
            show_organ_main(osys)
            pause_consol()
            continue
        
        if menu == 2: # TODO
            pass
        
        if menu == 0:
            return

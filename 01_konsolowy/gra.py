import random # Importujemy bibliotekę do losowania
import time   # Importujemy bibliotekę do obsługi czasu (przydatne do opóźnień)

def zagraj_w_gre():
    """
    To jest główna funkcja obsługująca pojedynczy mecz. 
    Dzięki zamknięciu kodu w funkcji, możemy go łatwo wywoływać wielokrotnie.
    """
    print("=======================================")
    print("Witaj w grze Kamień, Papier, Nożyce! ✊ ✋ ✌️")
    print("Gramy do 5 wygranych!")
    print("=======================================")

    # Inicjalizacja liczników punktów. Zaczynamy od zera.
    punkty_gracza = 0
    punkty_komputera = 0
    
    # Lista 'opcje' przechowuje możliwe ruchy w grze.
    opcje = ["kamien", "papier", "nozyce"]
    
    # Główna pętla meczu: trwa dopóki nikt nie zdobędzie 5 punktów.
    while punkty_gracza < 5 and punkty_komputera < 5:
        print(f"\n--- WYNIK --- Gracz: {punkty_gracza} | Komputer: {punkty_komputera} ---")
        
        # 1. POBIERANIE DANYCH OD UŻYTKOWNIKA
        # .lower() zamienia wpisany tekst na małe litery, aby uniknąć błędów przy "Kamień" vs "kamien"
        wybor_gracza = input("Wybierz (kamien, papier, nozyce): ").lower()
        
        # Walidacja: sprawdzamy, czy to co wpisał gracz znajduje się na naszej liście opcji.
        if wybor_gracza not in opcje:
            print("❌ Niepoprawny wybór! Wpisz dokładnie: kamien, papier lub nozyce.")
            continue # Przeskakujemy resztę pętli i wracamy do początku (nowe pytanie)
            
        print(f"Twój wybór to: {wybor_gracza.upper()}")
        
        # 2. RUCH KOMPUTERA
        # Korzystamy z funkcji random.choice, która wybiera losowy element z listy.
        print("🤖 Komputer myśli...")
        time.sleep(1) # Robimy 1 sekundę przerwy dla lepszego efektu "gry"
        
        wybor_komputera = random.choice(opcje)
        print(f"Wybór komputera to: {wybor_komputera.upper()}\n")
        
        # 3. LOGIKA SPRAWDZANIA WYNIKU (Warunki IF / ELIF)
        if wybor_gracza == wybor_komputera:
            print("Remis! Obaj wybraliście to samo. 🤝")
            
        # Sprawdzamy wszystkie przypadki, w których gracz wygrywa
        elif (wybor_gracza == "kamien" and wybor_komputera == "nozyce") or \
             (wybor_gracza == "papier" and wybor_komputera == "kamien") or \
             (wybor_gracza == "nozyce" and wybor_komputera == "papier"):
            print("Punkt dla Ciebie! 🎉")
            punkty_gracza += 1 # Zwiększamy punkty gracza o 1
            
        else:
            # Jeśli nie ma remisu i gracz nie wygrał, oznacza to zwycięstwo komputera.
            print("Punkt dla komputera! 💻")
            punkty_komputera += 1 # Zwiększamy punkty komputera o 1

    # PODSUMOWANIE MECZU
    print("\n=======================================")
    if punkty_gracza == 5:
        print("🎊 GRATULACJE! Pokonałeś maszynę i wygrałeś mecz! 🎊")
    else:
        print("💀 Komputer wygrał tym razem. Musisz poćwiczyć! 💀")
    print("=======================================")

# START PROGRAMU
# Ta pętla pozwala grać wiele meczów bez konieczności restartowania skryptu.
while True:
    zagraj_w_gre()
    jeszcze_raz = input("\nCzy chcesz zagrać kolejny mecz? (tak/nie): ").lower()
    if jeszcze_raz != "tak":
        print("Dziękuję za wspólną zabawę! Do widzenia!")
        break # Kończymy działanie programu

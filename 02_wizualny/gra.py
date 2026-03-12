import pygame
import random
import sys
import os

# =======================================================
# 1. INICJALIZACJA (PRZYGOTOWANIE)
# =======================================================
# Każdy program w Pygame musi zacząć od tej komendy. 
# Włącza ona wszystkie moduły biblioteki (grafika, dźwięk itp.)
pygame.init()

# Stałe wartości wymiarów okna gry
SZEROKOSC = 800
WYSOKOSC = 600
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Kamień, Papier, Nożyce - Poziom Graficzny")

# Kolory definiujemy w formacie RGB (Red, Green, Blue) — wartości od 0 do 255.
BIALY = (245, 245, 250)
CZARNY = (30, 30, 30)
SZARY = (150, 150, 150)
ZIELONY = (60, 200, 100)
CZERWONY = (220, 80, 80)
JASNO_SZARY = (200, 200, 200)

# Przygotowanie czcionek do wyświetlania tekstu.
# SysFont szuka czcionek zainstalowanych w Twoim systemie operacyjnym.
czcionka_tytul = pygame.font.SysFont("arial", 45, bold=True)
czcionka_zwykla = pygame.font.SysFont("arial", 35, bold=True)
czcionka_mala = pygame.font.SysFont("arial", 25)

# BASE_DIR to ścieżka do folderu, w którym znajduje się ten skrypt.
# Dzięki temu wczytywanie plików będzie działać na każdym komputerze.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def wczytaj_img(nazwa):
    """Pomocnicza funkcja do bezpiecznego wczytywania grafik."""
    sciezka = os.path.join(BASE_DIR, nazwa)
    if os.path.exists(sciezka):
        # convert_alpha() optymalizuje grafikę pod kątem szybkości rysowania (przezroczystość)
        return pygame.image.load(sciezka).convert_alpha()
    else:
        # Jeśli pliku brakuje, tworzymy zastępczy szary kwadrat, by program się nie zawiesił
        img = pygame.Surface((150, 150))
        img.fill(SZARY)
        return img

# Ładowanie Grafik — rock.png, paper.png, scissors.png muszą być w tym samym folderze!
grafiki = {}
male_grafiki = {}
# Tworzymy pętlę, żeby załadować obrazki dla każdej z trzech opcji
for opcja_plik in ["rock.png", "paper.png", "scissors.png"]:
    nazwa_klucz = "Kamień" if "rock" in opcja_plik else "Papier" if "paper" in opcja_plik else "Nożyce"
    original = wczytaj_img(opcja_plik)
    # Skalujemy obrazki do odpowiednich rozmiarów (transform.scale)
    grafiki[nazwa_klucz] = pygame.transform.scale(original, (150, 150))
    male_grafiki[nazwa_klucz] = pygame.transform.scale(original, (80, 80))

# =======================================================
# 2. LOGIKA GRY I FUNKCJE POMOCNICZE
# =======================================================
def sprawdz_wynik(gracz, komputer):
    """
    To jest mózg gry. Porównuje wybory i zwraca:
    - tekst wyniku
    - kolor tekstu
    - punkty dla gracza
    - punkty dla komputera
    """
    if gracz == komputer:
        return "REMIS!", SZARY, 0, 0
    elif (gracz == "Kamień" and komputer == "Nożyce") or \
         (gracz == "Papier" and komputer == "Kamień") or \
         (gracz == "Nożyce" and komputer == "Papier"):
        return "WYGRANA!", ZIELONY, 1, 0
    else:
        return "PRZEGRANA...", CZERWONY, 0, 1

def rysuj_przycisk(tekst, x, y, szer, wys, kolor):
    """
    Uniwersalna funkcja do rysowania prostokątnych przycisków.
    Zwraca True, jeśli użytkownik kliknął w przycisk myszką.
    """
    mysz = pygame.mouse.get_pos() # Pobieramy aktualną pozycję kursora (x, y)
    klik = pygame.mouse.get_pressed() # Pobieramy stan przycisków myszy (lewy, środkowy, prawy)
    rect = pygame.Rect(x, y, szer, wys) # Tworzymy obiekt prostokąta
    
    # EFEKT HOVER: Jeśli myszka jest nad przyciskiem, rozjaśniamy jego kolor
    kolor_final = (min(kolor[0]+30, 255), min(kolor[1]+30, 255), min(kolor[2]+30, 255)) if rect.collidepoint(mysz) else kolor
    
    # Rysujemy prostokąt na ekranie
    pygame.draw.rect(ekran, kolor_final, rect, border_radius=15)
    
    # Renderujemy tekst i umieszczamy go na środku przycisku
    t = czcionka_zwykla.render(tekst, True, BIALY)
    ekran.blit(t, t.get_rect(center=rect.center))
    
    # Sprawdzamy, czy nastąpiło kliknięcie (0 to lewy przycisk myszy)
    if rect.collidepoint(mysz) and klik[0]:
        pygame.time.delay(150) # Małe opóźnienie, by uniknąć wielokrotnego kliknięcia w ułamku sekundy
        return True
    return False

# Zmienne przechowujące aktualny stan meczu
opcje_gry = ["Kamień", "Papier", "Nożyce"]
wybor_gracza = wybor_komputera = None
wynik_tekst = ""
kolor_wyniku = CZARNY
punkty_gracza = punkty_komputera = 0
koniec_mecz = False

# =======================================================
# 3. GŁÓWNA PĘTLA GRY (GAME LOOP)
# =======================================================
# Heartbeat programu: Kod w pętli while działa w kółko, dopóki gracz nie zamknie okna.
dziala = True
zegar = pygame.time.Clock() # Zegar służy do kontrolowania liczby klatek na sekundę (FPS)

while dziala:
    # A. ZDARZENIA (Events) — Sprawdzamy, czy użytkownik coś zrobił (klawiatura, mysz)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Użytkownik kliknął X na oknie
            dziala = False

    # B. RYSOWANIE (Drawing) — Najpierw czyścimy ekran tłem, potem rysujemy elementy
    ekran.fill(BIALY)

    # Wyświetlamy aktualny wynik meczu na górze ekranu
    napis_pkt = czcionka_zwykla.render(f"TY: {punkty_gracza} | KOMP: {punkty_komputera}", True, CZARNY)
    ekran.blit(napis_pkt, (SZEROKOSC//2 - napis_pkt.get_width()//2, 20))

    if not koniec_mecz:
        # FAZA WYBORU — mecz w toku
        label = czcionka_tytul.render("Wybierz swój ruch:", True, CZARNY)
        ekran.blit(label, (SZEROKOSC//2 - label.get_width()//2, 80))

        # OBSŁUGA WYBORU BRONI (Pętla po opcjach)
        pos_x = [100, 325, 550] # Pozycje X dla trzech obrazków
        for i, opcja in enumerate(opcje_gry):
            rect_img = pygame.Rect(pos_x[i], 160, 150, 150)
            
            # Jeśli myszka najeżdża na obrazek, rysujemy pod nim szary kafel (podświetlenie)
            if rect_img.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(ekran, JASNO_SZARY, rect_img, border_radius=10)
            
            # Rysujemy główny obrazek broni (blit = draw)
            ekran.blit(grafiki[opcja], (pos_x[i], 160))
            
            # Jeśli użytkownik kliknął w dany obrazek:
            if rect_img.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                wybor_gracza = opcja
                wybor_komputera = random.choice(opcje_gry) # Losowanie komputera
                
                # Przetwarzamy wynik rundy
                wynik_tekst, kolor_wyniku, pg, pk = sprawdz_wynik(wybor_gracza, wybor_komputera)
                punkty_gracza += pg
                punkty_komputera += pk
                pygame.time.delay(200)

        # WYŚWIETLANIE WYNIKU RUNDY (jeśli już jakiś wybór nastąpił)
        if wybor_gracza:
            # Rysujemy mniejsze ikonki podsumowujące ostatnie starcie
            ekran.blit(male_grafiki[wybor_gracza], (150, 350))
            ekran.blit(male_grafiki[wybor_komputera], (SZEROKOSC - 230, 350))
            
            # Wypisujemy wynik (WYGRANA / REMIS / PRZEGRANA)
            txt = czcionka_tytul.render(wynik_tekst, True, kolor_wyniku)
            ekran.blit(txt, (SZEROKOSC//2 - txt.get_width()//2, 360))

        # Sprawdzamy, czy ktoś osiągnął 5 punktów (limit meczu)
        if punkty_gracza >= 5 or punkty_komputera >= 5:
            koniec_mecz = True
    else:
        # EKRAN KOŃCOWY — ktoś wygrał cały mecz!
        komunikat = "👑 WYGRAŁEŚ CAŁY MECZ! 👑" if punkty_gracza >= 5 else "💀 PRZEGRAŁEŚ MECZ... 💀"
        klr = ZIELONY if punkty_gracza >= 5 else CZERWONY
        napis_koniec = czcionka_tytul.render(komunikat, True, klr)
        ekran.blit(napis_koniec, (SZEROKOSC//2 - napis_koniec.get_width()//2, 220))
        
        # Przycisk restartu — czyści punkty i wybory, zaczynamy od nowa
        if rysuj_przycisk("Zagraj ponownie!", SZEROKOSC//2 - 150, 350, 300, 70, ZIELONY):
            punkty_gracza = punkty_komputera = 0
            wybor_gracza = None
            koniec_mecz = False

    # C. ODKŚWIEŻANIE (Update) — Przesyłamy wszystko, co narysowaliśmy, do wyświetlenia na monitorze.
    pygame.display.flip()
    
    # Ograniczamy prędkość gry do 60 klatek na sekundę. 
    # Bez tego program zużywałby 100% procesora, działając zbyt szybko.
    zegar.tick(60)

# Kiedy pętla while przestanie działać (dziala = False), wyłączamy Pygame i kończymy skrypt.
pygame.quit()
sys.exit()

import pygame
import random
import sys
import os
import asyncio # Wymagane dla przeglądarki

# =======================================================
# WERSJA PRZEGLĄDARKOWA (02_wizualny) — main.py
# =======================================================

async def main():
    pygame.init()

    SZEROKOSC = 800
    WYSOKOSC = 600
    ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    pygame.display.set_caption("KPN: Poziom Graficzny (Web)")

    BIALY = (245, 245, 250)
    CZARNY = (30, 30, 30)
    SZARY = (150, 150, 150)
    ZIELONY = (60, 200, 100)
    CZERWONY = (220, 80, 80)
    JASNO_SZARY = (200, 200, 200)

    czcionka_tytul = pygame.font.SysFont("arial", 45, bold=True)
    czcionka_zwykla = pygame.font.SysFont("arial", 35, bold=True)
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def wczytaj_img(nazwa):
        sciezka = os.path.join(BASE_DIR, nazwa)
        if os.path.exists(sciezka):
            return pygame.image.load(sciezka).convert_alpha()
        img = pygame.Surface((150, 150)); img.fill(SZARY); return img

    grafiki = {}
    male_grafiki = {}
    for opcja in ["rock.png", "paper.png", "scissors.png"]:
        nazwa_klucz = "Kamień" if "rock" in opcja else "Papier" if "paper" in opcja else "Nożyce"
        original = wczytaj_img(opcja)
        grafiki[nazwa_klucz] = pygame.transform.scale(original, (150, 150))
        male_grafiki[nazwa_klucz] = pygame.transform.scale(original, (80, 80))

    def sprawdz_wynik(gracz, komputer):
        if gracz == komputer: return "REMIS!", SZARY, 0, 0
        elif (gracz == "Kamień" and komputer == "Nożyce") or \
             (gracz == "Papier" and komputer == "Kamień") or \
             (gracz == "Nożyce" and komputer == "Papier"):
            return "WYGRANA!", ZIELONY, 1, 0
        else: return "PRZEGRANA...", CZERWONY, 0, 1

    def rysuj_przycisk(tekst, x, y, szer, wys, kolor):
        mysz, klik = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, szer, wys)
        h = rect.collidepoint(mysz)
        k_f = (min(kolor[0]+30, 255), min(kolor[1]+30, 255), min(kolor[2]+30, 255)) if h else kolor
        pygame.draw.rect(ekran, k_f, rect, border_radius=15)
        t = czcionka_zwykla.render(tekst, True, BIALY)
        ekran.blit(t, t.get_rect(center=rect.center))
        if h and klik[0]:
            pygame.time.delay(100); return True
        return False

    opcje_gry = ["Kamień", "Papier", "Nożyce"]
    wybor_gracza = wybor_komputera = None
    wynik_tekst = ""
    kolor_wyniku = CZARNY
    punkty_gracza = punkty_komputera = 0
    koniec_mecz = False
    zegar = pygame.time.Clock()

    # --- PĘTLA GŁÓWNA ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

        ekran.fill(BIALY)
        napis_pkt = czcionka_zwykla.render(f"TY: {punkty_gracza} | KOMP: {punkty_komputera}", True, CZARNY)
        ekran.blit(napis_pkt, (SZEROKOSC//2 - napis_pkt.get_width()//2, 20))

        if not koniec_mecz:
            label = czcionka_tytul.render("Wybierz swój ruch:", True, CZARNY)
            ekran.blit(label, (SZEROKOSC//2 - label.get_width()//2, 80))

            pos_x = [100, 325, 550]
            for i, opcja in enumerate(opcje_gry):
                rect_img = pygame.Rect(pos_x[i], 160, 150, 150)
                if rect_img.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(ekran, JASNO_SZARY, rect_img, border_radius=10)
                ekran.blit(grafiki[opcja], (pos_x[i], 160))
                if rect_img.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    wybor_gracza, wybor_komputera = opcja, random.choice(opcje_gry)
                    wynik_tekst, kolor_wyniku, pg, pk = sprawdz_wynik(wybor_gracza, wybor_komputera)
                    punkty_gracza += pg; punkty_komputera += pk; pygame.time.delay(150)

            if wybor_gracza:
                ekran.blit(male_grafiki[wybor_gracza], (150, 350))
                ekran.blit(male_grafiki[wybor_komputera], (SZEROKOSC - 230, 350))
                txt = czcionka_tytul.render(wynik_tekst, True, kolor_wyniku)
                ekran.blit(txt, (SZEROKOSC//2 - txt.get_width()//2, 360))

            if punkty_gracza >= 5 or punkty_komputera >= 5: koniec_mecz = True
        else:
            msg = "👑 WYGRAŁEŚ CAŁY MECZ! 👑" if punkty_gracza >= 5 else "💀 PRZEGRAŁEŚ MECZ... 💀"
            klr = ZIELONY if punkty_gracza >= 5 else CZERWONY
            napis_koniec = czcionka_tytul.render(msg, True, klr)
            ekran.blit(napis_koniec, (SZEROKOSC//2 - napis_koniec.get_width()//2, 220))
            if rysuj_przycisk("Zagraj ponownie!", SZEROKOSC//2 - 150, 350, 300, 70, ZIELONY):
                punkty_gracza = punkty_komputera = 0; wybor_gracza = None; koniec_mecz = False

        pygame.display.flip()
        await asyncio.sleep(0) # Wymagane dla płynności w przeglądarce
        zegar.tick(60)

asyncio.run(main())

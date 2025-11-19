# Diagnostika problému s detekcí převaděčů

## Problém
Program nenachází 2m převaděče v CHIRP image souboru, i když tam určitě jsou.

## Příčina
Existují **DVA různé formáty** pro Yaesu image soubory:

1. **FT-817 formát** - 26 bajtů na kanál
   - Frekvence: bajty 10-13
   - Offset: bajty 14-17
   - Jméno: bajty 18-25

2. **FT-857/897 formát** - 28 bajtů na kanál
   - Frekvence: bajty 12-15
   - Offset: bajty 16-19
   - Jméno: bajty 20-27

**CHIRP může uložit data v kterémkoliv formátu!**

## Řešení - Diagnostický nástroj

Vytvořil jsem nástroj, který otestuje **OBA** formáty na vašem image souboru a ukáže, který funguje správně.

### Jak použít (Windows):

1. **Jednoduchý způsob**: Přetáhněte váš `.dat` soubor na `dump_image.bat`

2. **Ruční způsob**:
   ```
   dump_image.bat "C:\cesta\k\vasemu\ft897.dat"
   ```

### Výstup:

Nástroj vytvoří textový soubor (např. `ft897_dump.txt`) který obsahuje:

- Prvních 10 kanálů v detailu
- **OBA** formáty otestované na každém kanálu
- Přesné bajty v hexadecimálním formátu
- Dekódované frekvence a offsety
- Logiku detekce převaděčů

### Co dělat dál:

1. Spusťte `dump_image.bat` na váš CHIRP image soubor
2. Otevře se Notepad s výsledky
3. **Pošlete mi tento soubor** (můžete zkopírovat text do zprávy)
4. Podle výsledků **opravím program** aby používal správný formát

## Příklad výstupu:

```
CHANNEL 0
======================================================================

Raw bytes (0-27):
  Bytes  0- 7: 05 c0 00 00 10 00 1a 1a
  Bytes  8-15: 00 00 a0 86 01 00 c0 c5 09 00
  Bytes 16-23: 4f 4b 37 44 4d 4f 00 ff
  Bytes 24-27: ff ff ff ff

──────────────────────────────────────────────────────────────────────
TESTING FT-817 FORMAT (26 bytes):
──────────────────────────────────────────────────────────────────────

Bytes 10-13 (frequency in FT-817 format):
  Raw bytes: a0 86 01 00
  → Raw value: 99488
  → Frequency: 994880 Hz = 0.9949 MHz
  → In 2m band? False

──────────────────────────────────────────────────────────────────────
TESTING FT-857/897 FORMAT (28 bytes):
──────────────────────────────────────────────────────────────────────

Bytes 12-15 (frequency in FT-857/897 format):
  Raw bytes: 01 00 c0 c5
  → Raw value: 3319644161
  → Frequency: 33196441610 Hz = 33196.4416 MHz
  → In 2m band? False
```

Podle těchto dat budu schopný určit, který formát váš CHIRP používá!

## Po diagnostice

Jakmile dostanu výstup, opravím:
- `ft897_memory.py` - základní knihovnu
- `ft897_gui.py` - PyQt GUI
- `ft897_gui_tkinter.py` - Tkinter GUI
- Všechny ostatní nástroje

Aby všechny používaly **SPRÁVNÝ** formát pro váš image soubor.

---

**Důležité**: Tento diagnostický nástroj **POUZE ČTE** váš image soubor. Nic nemodifikuje, takže je 100% bezpečný!

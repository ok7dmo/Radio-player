# FT-897 Packet Converter

Jednoduchá Python aplikace pro úpravu image souboru z radiostanice **Yaesu FT-897**, která automaticky nastaví všechny **dvoumetrové převaděče** (repeatery) do módu **PKT (Packet)**.

## 🎯 Co program dělá

1. Načte image soubor z FT-897 (záloha paměti rádia)
2. Projde všechny paměťové kanály
3. Najde kanály na 2m pásmu (144-146 MHz), které mají nastaven repeater offset
4. Změní jejich pracovní mód na **PKT (Packet)**
5. Uloží upravený image do nového souboru

## 📋 Požadavky

- **Python 3.6 nebo novější**
- Žádné další knihovny (používá pouze standardní Python moduly)

## 🚀 Použití

### Základní použití

```bash
python3 ft897_packet_converter.py vstupni_soubor.dat vystupni_soubor.dat
```

### Příklad

```bash
python3 ft897_packet_converter.py ft897_backup.dat ft897_modified.dat
```

### Krok za krokem

1. **Zálohujte paměť rádia** pomocí některého z těchto programů:
   - FT897 SuperControl
   - RT Systems ADMS-4B
   - FTBasicMMO
   - CHIRP

2. **Spusťte konvertor:**
   ```bash
   python3 ft897_packet_converter.py moje_zaloba.dat moje_zaloba_packet.dat
   ```

3. **Nahrajte upravený soubor zpět do rádia** pomocí stejného programu

4. **Vyzkoušejte nové nastavení** - ověřte, že 2m repeatery fungují správně

## 📊 Výstup programu

Program zobrazuje informace o zpracování:

```
======================================================================
FT-897 Image Converter - 2m Repeater to Packet Mode
======================================================================

Input file:  ft897_backup.dat
Output file: ft897_modified.dat

Processing...
----------------------------------------------------------------------

✓ Found 2m repeater: Ch005: 145.6250 MHz FM    [+]  offset=  600.0kHz  'R5'
  Changing mode: FM → PKT

✓ Found 2m repeater: Ch012: 145.7750 MHz FM    [-]  offset=  600.0kHz  'R12'
  Changing mode: FM → PKT

✓ Saved modified image to: ft897_modified.dat

======================================================================
Summary:
  Total channels found: 45
  2m repeaters modified: 2
======================================================================

✓ Success! You can now upload the modified image to your FT-897.

⚠ IMPORTANT: Make sure to keep a backup of your original image!
  Test the modified image carefully before relying on it.
```

## 🔍 Jak program pozná 2m repeater?

Kanál je považován za **dvoumetrový převaděč**, pokud:

1. **Frekvence je v rozsahu 144.000 - 146.000 MHz** (2m pásmo)
2. **Je nastaven repeater offset** (duplex flag nebo nenulový offset)

## 📡 Podporované módy FT-897

Program rozpoznává následující módy:

| Kód  | Mód   | Popis                    |
|------|-------|--------------------------|
| 0x00 | LSB   | Lower Sideband           |
| 0x01 | USB   | Upper Sideband           |
| 0x02 | CW    | Morse Code               |
| 0x03 | CW-R  | CW Reverse               |
| 0x04 | AM    | Amplitude Modulation     |
| 0x06 | WFM   | Wide FM (broadcast)      |
| 0x08 | FM    | Narrowband FM            |
| 0x0A | DIG   | Digital Mode             |
| 0x0C | **PKT** | **Packet Mode** ⬅️    |

## ⚙️ Technické detaily

### Struktura paměťového kanálu

Každý paměťový kanál má **26 bytů** a obsahuje:

- **Byte 0**: Tagy a pracovní mód (3 bity)
- **Byte 1**: Duplex nastavení, šířka pásma
- **Byte 2**: Skip, IPO, ATT příznaky
- **Bytes 14-17**: Frekvence (32-bit, little-endian, v jednotkách 10 Hz)
- **Bytes 18-21**: Repeater offset (32-bit, little-endian, v jednotkách 10 Hz)

### Změna módu

Mód je uložen v **3 bitech** (bits 0-2) prvního bytu každého kanálu. Program:

1. Přečte aktuální hodnotu bytu 0
2. Vynuluje bity 0-2 (mód)
3. Nastaví nový mód (0x0C pro PKT)
4. Zapíše upravený byte zpět

```python
# Příklad změny módu
byte0 = (byte0 & 0xF8) | 0x0C  # Set mode to PKT
```

## ⚠️ Důležitá upozornění

1. **Vždy si zálohujte originální image!** Před nahráním upravené konfigurace do rádia.

2. **Otestujte v bezpečném prostředí** - Ověřte, že upravená konfigurace funguje správně.

3. **Program byl vytvořen na základě reverse-engineeringu** formátu FT-897 image z:
   - CHIRP open-source projektu (ft857.py driver)
   - CAT command dokumentace
   - Community zdrojů

4. **Použití na vlastní riziko** - Autor neručí za případné problémy s rádiem.

## 🛠️ Řešení problémů

### Program nenajde žádné kanály

- Zkontrolujte, že vstupní soubor je opravdu FT-897 image
- Ověřte, že soubor není poškozen
- Ujistěte se, že máte v paměti rádia uložené nějaké 2m repeatery

### Rádio neakceptuje upravený image

- Ujistěte se, že používáte kompatibilní software pro nahrání
- Zkontrolujte, že image nebyl během přenosu poškozen
- Zkuste obnovit původní image a postup opakovat

### Python hlásí chyby

```bash
# Zkontrolujte verzi Pythonu (musí být 3.6+)
python3 --version

# Zkontrolujte, že máte práva ke čtení/zápisu souborů
ls -la vstupni_soubor.dat
```

## 📚 Zdroje a reference

- [Yaesu FT-897 Operating Manual](https://www.hamradio.co.uk/pub/media/wysiwyg/FT-897_OpMan.pdf)
- [CHIRP Radio Programming Software](https://chirpmyradio.com/)
- [FT-897 CAT Commands](https://www.qsl.net/sp9hzx/pdf/FT-897D_Yaesu-official_CAT-Commands.pdf)
- [KA7OEI FT-817 Memory Map](https://www.ka7oei.com/ft817_memmap.html)

## 📝 Licence

MIT License - Používejte a upravujte dle potřeby.

## 🤝 Přispívání

Pokud najdete chybu nebo máte nápad na vylepšení, neváhejte vytvořit issue nebo pull request.

## ✉️ Autor

Vytvořeno pomocí **Claude AI** na základě veřejně dostupné dokumentace a reverse-engineering informací z CHIRP projektu.

---

**UPOZORNĚNÍ**: Tento software byl vytvořen pro vzdělávací a experimentální účely. Autor není nijak spojen s Yaesu a produkt není oficiálně podporován výrobcem.

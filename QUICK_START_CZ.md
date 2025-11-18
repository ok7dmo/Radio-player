# 🚀 Rychlý start - FT-897 Packet Converter

## Co budete potřebovat

1. ✅ **Python 3.6 nebo novější**
2. ✅ **Zálohu paměti vašeho FT-897** (`.dat` soubor)
3. ✅ **Software pro nahrání konfigurace** (např. CHIRP, FTBasicMMO, RT Systems)

## Krok 1: Ověření instalace Pythonu

```bash
python3 --version
```

Měli byste vidět něco jako: `Python 3.8.10` nebo vyšší.

## Krok 2: Stažení zálohy z rádia

Použijte jeden z těchto programů pro vytvoření zálohy:

- **CHIRP** (zdarma, open-source): https://chirpmyradio.com/
- **FTBasicMMO** (zdarma): https://www.m0lxq.com/g4hfq/
- **RT Systems ADMS-4B** (placené)

Uložte zálohu například jako `ft897_original.dat`

## Krok 3: Analýza image (volitelné)

Nejdřív se podívejte, co je v image souboru:

```bash
python3 ft897_analyze.py ft897_original.dat
```

Uvidíte seznam všech kanálů, včetně 2m repeaterů, které budou převedeny.

## Krok 4: Konverze do Packet módu

```bash
python3 ft897_packet_converter.py ft897_original.dat ft897_packet.dat
```

Program najde všechny 2m repeatery a změní je na PKT mód.

## Krok 5: Nahrání zpět do rádia

1. Otevřete svůj programovací software (CHIRP, FTBasicMMO, atd.)
2. Nahrajte upravený soubor `ft897_packet.dat`
3. Odešlete do rádia

## Krok 6: Otestování

1. Vyberte nějaký 2m repeater z paměti
2. Zkontrolujte, že mód je nastaven na **PKT**
3. Vyzkoušejte spojení

---

## 📝 Kompletní příklad

```bash
# 1. Stáhnout zálohu z rádia (pomocí CHIRP nebo jiného SW)
#    → uložíte jako ft897_original.dat

# 2. Nejdřív analyzovat (volitelné)
python3 ft897_analyze.py ft897_original.dat

# 3. Konvertovat na PKT mód
python3 ft897_packet_converter.py ft897_original.dat ft897_packet.dat

# 4. Nahrát zpět do rádia (pomocí CHIRP nebo jiného SW)
#    → načtěte ft897_packet.dat a odešlete do rádia
```

---

## 🎯 Výstup analýzy

Po spuštění `ft897_analyze.py` uvidíte:

```
================================================================================
FT-897 Image Analyzer
================================================================================

File: ft897_original.dat
Size: 16384 bytes (16 KB)

--------------------------------------------------------------------------------
SUMMARY
--------------------------------------------------------------------------------
Total programmed channels: 45
Total repeaters: 8
2m band repeaters: 3

--------------------------------------------------------------------------------
2-METER BAND REPEATERS (Candidates for PKT mode conversion)
--------------------------------------------------------------------------------
Ch   Freq (MHz)   Mode   Duplex   Offset (kHz)  Name
--------------------------------------------------------------------------------
  5     145.6250 FM     + (Plus)          600.0  R5
 12     145.7750 FM     - (Minus)         600.0  R12
 23     145.5500 FM     + (Plus)          600.0  OK0EPP

Already in PKT mode: 0
Can be converted:    3

💡 TIP: Use ft897_packet_converter.py to convert these repeaters to PKT mode.
```

---

## 🎯 Výstup konverze

Po spuštění `ft897_packet_converter.py` uvidíte:

```
======================================================================
FT-897 Image Converter - 2m Repeater to Packet Mode
======================================================================

Input file:  ft897_original.dat
Output file: ft897_packet.dat

Processing...
----------------------------------------------------------------------

✓ Found 2m repeater: Ch005: 145.6250 MHz FM    [+]  offset=  600.0kHz  'R5'
  Changing mode: FM → PKT

✓ Found 2m repeater: Ch012: 145.7750 MHz FM    [-]  offset=  600.0kHz  'R12'
  Changing mode: FM → PKT

✓ Found 2m repeater: Ch023: 145.5500 MHz FM    [+]  offset=  600.0kHz  'OK0EPP'
  Changing mode: FM → PKT

✓ Saved modified image to: ft897_packet.dat

======================================================================
Summary:
  Total channels found: 45
  2m repeaters modified: 3
======================================================================

✓ Success! You can now upload the modified image to your FT-897.
```

---

## ⚠️ Důležité

1. **VŽDY SI ZÁLOHUJTE ORIGINÁL!** Než nahrajete novou konfiguraci.
2. **Nejdřív testujte** - Ověřte, že všechno funguje správně.
3. **Buďte opatrní** - Tento software není oficiálně podporován výrobcem.

---

## 🆘 Pomoc

### Program nenajde žádné repeatery

- Zkontrolujte, že máte v paměti opravdu nějaké 2m repeatery
- Použijte `ft897_analyze.py` pro kontrolu obsahu image

### Python není nainstalovaný

```bash
# Ubuntu/Debian
sudo apt-get install python3

# macOS (s Homebrew)
brew install python3

# Windows
# Stáhněte z https://www.python.org/downloads/
```

### Rádio neakceptuje upravený image

- Ujistěte se, že používáte správný software
- Zkontrolujte verzi rádia (FT-897 vs FT-897D)
- Obnovte originální zálohu a zkuste znovu

---

## 📚 Další informace

Podrobnou dokumentaci najdete v:
- **README_FT897_CONVERTER.md** - Kompletní dokumentace
- **ft897_packet_converter.py** - Zdrojový kód s komentáři

---

**Vytvořeno s láskou pro radioamatérskou komunitu 📻**

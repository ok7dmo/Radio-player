# FT-897 Memory Manager - GUI Application

Profesionální grafické rozhraní pro správu pamětí rádia **Yaesu FT-897** s kompletní podporou všech funkcí.

![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Funkce

### ✨ Hlavní funkce

- **📂 Načítání/ukládání FT-897 image souborů**
  - Podpora .dat a .img formátů
  - Automatické zálohy
  - Undo/Redo operace

- **📊 Tabulkový přehled všech kanálů**
  - Zobrazení všech používaných kanálů
  - Řazení podle sloupců
  - Barevné zvýraznění (2m repeatery, PKT mód)
  - Export do CSV

- **✏️ Editor kanálů**
  - Úprava frekvence (MHz + fine tune v kHz)
  - Změna módu (LSB, USB, CW, AM, FM, DIG, PKT)
  - Nastavení duplex (+, -, split)
  - Offset v kHz
  - Název kanálu (8 znaků)
  - Příznaky: Skip, IPO, ATT

- **🔄 Batch operace**
  - Konverze všech 2m repeaterů na PKT mód
  - Hromadné úpravy
  - Kopírování/mazání kanálů

- **📈 Statistiky a analýza**
  - Rozložení pásem
  - Rozložení módů
  - Počet repeaterů
  - Grafy a přehledy

## 📋 Požadavky

### Systémové požadavky

- **Python 3.7 nebo novější**
- **PyQt6** (grafická knihovna)
- Linux, macOS nebo Windows

### Instalace závislostí

```bash
# Instalace PyQt6
pip install PyQt6

# Nebo použít requirements.txt
pip install -r requirements.txt
```

## 🚀 Spuštění GUI aplikace

### Základní spuštění

```bash
python3 ft897_gui.py
```

### Alternativní způsoby

```bash
# Pokud je skript spustitelný
chmod +x ft897_gui.py
./ft897_gui.py
```

## 📖 Návod k použití

### 1. Načtení image souboru

**Menu:** `File → Load Image...` nebo **Ctrl+O**

1. Klikněte na tlačítko **"📂 Load Image"**
2. Vyberte .dat nebo .img soubor z vašeho rádia
3. Počkejte na načtení (zobrazí se všechny kanály)

### 2. Prohlížení kanálů

**Tabulka kanálů** zobrazuje:
- **Ch#** - Číslo kanálu
- **Frequency** - Frekvence v MHz
- **Mode** - Pracovní mód (zelená = PKT)
- **Duplex** - Simplex/+/-
- **Offset** - Repeater offset v kHz
- **Name** - Název kanálu
- **Band** - Pásmo (žlutá = 2m repeater)
- **Skip/IPO/ATT** - Příznaky

**Barevné zvýraznění:**
- 🟢 **Zelená** = Kanál v PKT módu
- 🟡 **Žlutá** = 2m repeater (kandidát na konverzi)

### 3. Úprava kanálu

**Způsob 1:** Dvojklik na řádek v tabulce

**Způsob 2:**
1. Vyberte kanál (kliknutím na řádek)
2. Klikněte **"✏️ Edit Selected Channel"**

**Editor kanálu umožňuje:**
- Změnit frekvenci (MHz a fine tune)
- Změnit mód
- Nastavit duplex a offset
- Upravit název
- Zapnout/vypnout příznaky

### 4. Konverze 2m repeaterů na PKT

**Menu:** `Tools → Convert 2m to PKT`

1. Klikněte **"🔄 Convert 2m Repeaters to PKT"**
2. Zobrazí se počet kanálů k převodu
3. Potvrďte operaci
4. Všechny 2m repeatery se změní na PKT mód

### 5. Statistiky

**Menu:** `Tools → Statistics`

1. Klikněte **"📊 Statistics"**
2. Zobrazí se:
   - Celkový počet kanálů
   - Počet 2m repeaterů
   - Rozložení pásem (graf)
   - Rozložení módů (graf)

### 6. Uložení změn

**Uložit do stejného souboru:**
- `File → Save` nebo **Ctrl+S**

**Uložit jako nový soubor:**
- `File → Save As...` nebo **Ctrl+Shift+S**

**Status bar** ukazuje:
- Název souboru
- [Modified] pokud jsou neuložené změny
- Počet kanálů
- Počet 2m repeaterů

## 🖥️ Ovládání klávesnicí

| Klávesa | Akce |
|---------|------|
| **Ctrl+O** | Načíst image |
| **Ctrl+S** | Uložit |
| **Ctrl+Shift+S** | Uložit jako... |
| **Ctrl+Q** | Ukončit aplikaci |
| **Enter** | Editovat vybraný kanál |
| **Delete** | Smazat vybraný kanál |

## 📸 Screenshoty

### Hlavní okno
```
┌─────────────────────────────────────────────────────────┐
│ File  Tools  Help                                       │
├─────────────────────────────────────────────────────────┤
│ [📂 Load] [💾 Save] [💾 Save As]      [📊 Statistics] │
├─────────────────────────────────────────────────────────┤
│ Batch Operations                                        │
│ [🔄 Convert 2m Repeaters to PKT]                       │
├─────────────────────────────────────────────────────────┤
│ Ch# │ Frequency │ Mode │ Duplex │ Offset │ Name │ Band │
├─────┼───────────┼──────┼────────┼────────┼──────┼──────┤
│  5  │ 145.6250  │ FM   │   +    │  600.0 │  R5  │  2m  │
│ 12  │ 145.7750  │ PKT  │   -    │  600.0 │  R12 │  2m  │
│ 23  │ 438.6250  │ FM   │   +    │ 7600.0 │  UHF │ 70cm │
└─────────────────────────────────────────────────────────┘
│ File: ft897_backup.dat | Channels: 45/200 | 2m: 3      │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Architektura

### Struktura projektu

```
Radio-player/
├── ft897_gui.py              # GUI aplikace (PyQt6)
├── ft897_memory.py            # Backend knihovna
├── ft897_packet_converter.py # CLI konvertor
├── ft897_analyze.py           # CLI analyzer
├── test_ft897_converter.py    # Testy
├── requirements.txt           # Závislosti
└── README_GUI.md             # Tato dokumentace
```

### Backend knihovna (ft897_memory.py)

**Třídy:**
- `FT897Channel` - Reprezentace jednoho kanálu
- `FT897Image` - Celý image soubor s operacemi

**Funkce:**
- Načítání/ukládání image
- Parsování 26-bytové struktury kanálu
- Úprava parametrů kanálů
- Batch operace
- Statistiky

### GUI aplikace (ft897_gui.py)

**Komponenty:**
- `FT897MainWindow` - Hlavní okno
- `ChannelEditorDialog` - Editor kanálu
- `StatisticsDialog` - Okno se statistikami

**Qt widgety:**
- `QTableWidget` - Tabulka kanálů
- `QSpinBox` - Číselné vstupy
- `QComboBox` - Výběr módu/duplex
- `QLineEdit` - Textové vstupy

## 🔧 Pokročilé použití

### Přidání vlastních operací

Můžete rozšířit `FT897Image` třídu o vlastní batch operace:

```python
from ft897_memory import FT897Image, MODE_USB

# Načíst image
image = FT897Image()
image.load_from_file("ft897_backup.dat")

# Vlastní operace - změnit všechny HF kanály na USB
for channel in image.channels:
    if channel.is_used() and 14_000_000 <= channel.frequency <= 30_000_000:
        channel.mode = MODE_USB
        channel._update_raw_data()

# Uložit
image.save_to_file("ft897_modified.dat")
```

### Export do CSV

```python
import csv

image = FT897Image()
image.load_from_file("ft897_backup.dat")

with open('channels.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Channel', 'Frequency', 'Mode', 'Name'])

    for ch in image.get_used_channels():
        info = ch.get_info_dict()
        writer.writerow([
            info['index'],
            f"{info['frequency_mhz']:.4f}",
            info['mode_name'],
            info['name']
        ])
```

## ⚠️ Důležitá upozornění

### Bezpečnost

1. **VŽDY SI ZÁLOHUJTE ORIGINÁLNÍ IMAGE!**
   - Před jakýmikoliv úpravami
   - Používejte "Save As..." pro nové verze

2. **Testujte v bezpečném prostředí**
   - Nejdřív načtěte do programovacího SW
   - Zkontrolujte náhled před odesláním do rádia

3. **Nemodifikujte systémové oblasti**
   - Nepřidávejte kanály mimo rozsah
   - Nedodržujte frekvenční limity

### Známá omezení

- **Formát image:** Podporován pouze standardní FT-897/857 formát (26 bytů/kanál)
- **Kapacita:** Max 200-500 kanálů (dle velikosti image)
- **Tone/CTCSS:** Základní podpora, pokročilé funkce v další verzi
- **Split frequency:** Zatím nepodporováno v editoru

## 🐛 Řešení problémů

### PyQt6 se nepodaří nainstalovat

```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6

# macOS
brew install pyqt6

# Windows
pip install --upgrade pip
pip install PyQt6
```

### Aplikace se nespustí

```bash
# Zkontrolujte Python verzi (min 3.7)
python3 --version

# Zkontrolujte PyQt6
python3 -c "from PyQt6.QtWidgets import QApplication; print('OK')"

# Pokud chyba, přeinstalujte
pip uninstall PyQt6
pip install PyQt6
```

### Tabulka je prázdná

- Zkontrolujte, že image obsahuje kanály (použijte ft897_analyze.py)
- Zkuste načíst jinou image
- Podívejte se do konzole na chybové hlášky

### Změny se neuloží do rádia

1. Ujistěte se, že jste uložili změny v GUI (**Save**)
2. Načtěte upravený soubor v programovacím SW
3. Odešlete do rádia přes CAT/clone
4. Zkontrolujte na rádiu, že změny jsou aplikovány

## 📚 Dodatečné zdroje

### Dokumentace

- [Yaesu FT-897 Operating Manual](https://www.hamradio.co.uk/pub/media/wysiwyg/FT-897_OpMan.pdf)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [CHIRP Project](https://chirpmyradio.com/)

### Související nástroje

- **CHIRP** - Open-source radio programming
- **RT Systems** - Komerční programovací SW
- **FTBasicMMO** - Free programming software

## 🤝 Přispívání

Máte nápad na vylepšení? Našli jste chybu?

1. Fork repository
2. Vytvořte feature branch
3. Commitněte změny
4. Vytvořte Pull Request

## 📄 Licence

MIT License - používejte a upravujte dle potřeby.

## ✉️ Autor

Vytvořeno pomocí **Claude AI** na základě:
- CHIRP ft857.py driver
- FT-897 CAT command dokumentace
- Reverse-engineering community

---

## 🎓 Pro vývojáře

### Struktura FT897Channel

```python
@dataclass
class FT897Channel:
    index: int              # Číslo kanálu
    frequency: int          # Frekvence v Hz
    mode: int               # Mód (0-7)
    duplex: int             # Duplex (0-3)
    offset: int             # Offset v Hz
    name: str               # Název (8 znaků)
    skip: bool              # Skip při scanu
    ipo: bool               # IPO flag
    att: bool               # Attenuator
    # ... další parametry
```

### API příklad

```python
from ft897_memory import FT897Image, MODE_PKT

# Načíst image
image = FT897Image()
image.load_from_file("backup.dat")

# Najít 2m repeatery
repeaters = image.get_2m_repeaters()
print(f"Found {len(repeaters)} 2m repeaters")

# Konvertovat na PKT
count = image.convert_2m_to_pkt()
print(f"Converted {count} channels")

# Uložit
image.save_to_file("modified.dat")

# Statistiky
stats = image.get_statistics()
print(f"Total: {stats['used_channels']} channels")
print(f"Bands: {stats['band_distribution']}")
```

---

**Vytvořeno s 💙 pro radioamatérskou komunitu 📻**

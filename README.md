# FT-897 Clone Manager

Qt aplikace v Pythonu pro správu paměťových kanálů vysílačky **Yaesu FT-897** přes klonovací režim.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Funkce

- ✅ Načítání paměťových kanálů z rádia přes sériový port (clone mode)
- ✅ Ukládání kanálů do rádia
- ✅ Načítání/ukládání clone dat do souborů
- ✅ Přehledná tabulka všech kanálů
- ✅ Zobrazení detailů kanálu (frekvence, režim, tóny, atd.)
- ⚠️ **Prototyp** - parsování dat je zjednodušené

## 📋 Požadavky

- Python 3.8 nebo novější
- PyQt6
- pyserial
- Yaesu FT-897 připojená přes sériový port (RS-232 nebo USB-to-Serial)

## 🚀 Instalace

1. Klonujte repozitář:
```bash
git clone <repository-url>
cd Radio-player
```

2. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

## 💻 Použití

### Spuštění aplikace

```bash
cd src
python main.py
```

### Načítání z rádia

1. **Připojte rádio** přes sériový port k počítači
2. **Vstupte do klonovacího režimu** na FT-897:
   - Vypněte rádio
   - Podržte obě **MODE** tlačítka (nad displejem)
   - Zapněte rádio (stále držte tlačítka)
   - Na displeji se objeví "CLONE MODE"
3. V aplikaci:
   - Vyberte správný sériový port
   - Klikněte na **"Připojit"**
   - Klikněte na **"📥 Načíst z rádia"**
   - Počkejte na dokončení (~10-30 sekund)

### Zápis do rádia

⚠️ **VAROVÁNÍ**: Toto přepíše všechna data v rádiu!

1. Načtěte nebo otevřete clone data
2. Vstupte do klonovacího režimu (viz výše)
3. Klikněte na **"📤 Zapsat do rádia"**

### Práce se soubory

- **Otevřít**: `Soubor > Otevřít...` (Ctrl+O)
- **Uložit**: `Soubor > Uložit` (Ctrl+S)
- **Uložit jako**: `Soubor > Uložit jako...` (Ctrl+Shift+S)

## 📁 Struktura projektu

```
Radio-player/
├── src/
│   ├── components/          # Qt GUI komponenty
│   │   ├── main_window.py   # Hlavní okno aplikace
│   │   └── channel_table.py # Tabulka kanálů
│   ├── services/            # Business logika
│   │   └── ft897_service.py # Komunikace s FT-897
│   ├── types/               # Datové typy
│   │   └── radio_types.py   # MemoryChannel, RadioMode, atd.
│   └── main.py              # Vstupní bod aplikace
├── tests/                   # Testy
├── requirements.txt         # Python závislosti
└── README.md               # Tento soubor
```

## 🔧 Technické detaily

### Klonovací protokol FT-897

- **Rychlost**: 9600 baud
- **Formát**: 8 datových bitů, 2 stop bity, bez parity
- **Velikost dat**: ~7898 bajtů
- **Kanály**: 1-999 paměťových kanálů

### Datová struktura MemoryChannel

```python
@dataclass
class MemoryChannel:
    channel_number: int          # 1-999
    receive_frequency: float     # v Hz
    transmit_offset: float       # v Hz
    mode: RadioMode             # LSB, USB, CW, AM, FM, atd.
    tone_mode: ToneMode         # OFF, TONE, T-SQL, DCS
    ctcss_tone: float           # Hz (88.5-254.1)
    dcs_code: int               # 23-754
    tag: str                    # Název kanálu (max 8 znaků)
    skip: bool                  # Přeskočit při skenování
    repeater_shift: str         # "SIMPLEX", "+", "-"
```

## ⚠️ Omezení (Prototyp)

Toto je **prototyp** s následujícími omezeními:

1. **Parsování dat je zjednodušené** - používá se ukázková struktura, ne skutečná FT-897 memory map
2. **Clone protokol není plně implementován** - příkazy jsou příklady
3. **Editace kanálů není implementována** - pouze zobrazení
4. **Chybí validace dat** - může selhat při neplatných datech
5. **Netestováno na skutečném hardware** - může vyžadovat úpravy

### Pro produkční použití by bylo potřeba:

- [ ] Implementovat skutečnou FT-897 memory map (detailní dokumentace)
- [ ] Přidat správné CAT příkazy pro clone mode
- [ ] Implementovat editaci kanálů
- [ ] Přidat undo/redo funkcionalitu
- [ ] Implementovat import/export do CSV
- [ ] Přidat podporu pro satelitní kanály
- [ ] Testování na skutečném hardware
- [ ] Přidat jednotkové testy
- [ ] Implementovat checksum validaci

## 📚 Reference

### Oficiální dokumentace

- [Yaesu FT-897D Operating Manual](http://www.yaesu.com/downloadFile.cfm?FileID=455&FileCatID=158&FileName=FT%2D897D%5FOM%5FENG%5F1108%2DD.pdf&FileContentType=application%2Fpdf)
- [FT-897 CAT Command Reference](http://www.ka7oei.com/ft817_meow.html)

### Software pro FT-897

- **CHIRP** - Open-source programovací software pro různá rádia
- **ADMS-4B** - Komerční software od RT Systems
- **SuperControl** - CAT control software

### Inspirace

- [CHIRP - FT-897 Support](https://chirp.danplanet.com/projects/chirp/wiki/Home)
- [FT-817/857/897 Memory Cloning](https://www.dxzone.com/dx12126/ft-817-ft-847-ft-857-ft-857d-ft-897-and-ft-897d-memory-cloning.html)

## 🐛 Známé problémy

1. **Parsování frekvencí** - Používá se jednoduchá konverze místo BCD dekódování
2. **Timeout na pomalém hardware** - Může být potřeba zvýšit timeout
3. **Port locking** - Na Linuxu může vyžadovat `sudo` nebo přidání uživatele do `dialout` skupiny

## 🤝 Přispívání

Příspěvky jsou vítány! Prosím:

1. Forkněte repozitář
2. Vytvořte feature branch (`git checkout -b feature/amazing-feature`)
3. Commitněte změny (`git commit -m 'Add amazing feature'`)
4. Pushněte do branch (`git push origin feature/amazing-feature`)
5. Otevřete Pull Request

## 📄 Licence

MIT License - viz [LICENSE](LICENSE) soubor

## 👤 Autor

Vytvořeno s pomocí Claude AI

## 🙏 Poděkování

- **Yaesu** za výrobu FT-897
- **CHIRP team** za inspiraci a dokumentaci
- Komunitě amatérského rádia za sdílení znalostí

---

**Poznámka**: Toto je prototyp/proof-of-concept. Pro produkční použití s reálným hardware doporučuji použít ověřený software jako CHIRP nebo ADMS-4B.

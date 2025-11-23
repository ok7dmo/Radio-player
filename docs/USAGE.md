# Návod k použití - FT-897 Clone Manager

## Obsah

1. [Vstup do klonovacího režimu](#vstup-do-klonovacího-režimu)
2. [Připojení rádia](#připojení-rádia)
3. [Načítání dat](#načítání-dat)
4. [Práce s kanály](#práce-s-kanály)
5. [Ukládání](#ukládání)
6. [Řešení problémů](#řešení-problémů)

## Vstup do klonovacího režimu

### FT-897

1. **Vypněte** rádio
2. **Podržte** obě tlačítka **MODE** (nachází se nad displejem)
3. **Zapněte** rádio (stále držte tlačítka MODE)
4. Na displeji se objeví text **"CLONE MODE"**
5. **Uvolněte** tlačítka

⚠️ **Důležité**: Rádio musí být v klonovacím režimu před každou operací čtení nebo zápisu!

### Výstup z klonovacího režimu

- Vypněte a znovu zapněte rádio normálně (bez držení tlačítek)

## Připojení rádia

### Hardware

Potřebujete:
- **FT-897** rádio
- **RS-232 kabel** (nebo USB-to-Serial adaptér)
- **CAT kabel** pro FT-897 (obvykle součástí příslušenství)

### Připojení v aplikaci

1. **Spusťte aplikaci**
2. V sekci "Připojení k rádiu":
   - Klikněte na **"🔄 Obnovit"** pro aktualizaci seznamu portů
   - **Vyberte správný sériový port** (např. COM3, /dev/ttyUSB0)
   - Klikněte na **"Připojit"**

3. Pokud je připojení úspěšné:
   - Tlačítko změní text na **"Odpojit"**
   - Aktivují se tlačítka pro načítání/zápis

### Výběr správného portu

#### Windows
- Obvykle `COM1`, `COM3`, `COM4`, atd.
- Zkontrolujte v **Správce zařízení** → **Porty (COM a LPT)**

#### Linux
- Obvykle `/dev/ttyUSB0`, `/dev/ttyS0`, atd.
- Seznam portů: `ls /dev/tty*`
- Může vyžadovat oprávnění: `sudo usermod -a -G dialout $USER`

#### macOS
- Obvykle `/dev/cu.usbserial-*`
- Seznam: `ls /dev/cu.*`

## Načítání dat

### Z rádia

1. **Vstupte do klonovacího režimu** (viz výše)
2. **Připojte se** k rádiu v aplikaci
3. Klikněte na **"📥 Načíst z rádia"**
4. Potvrďte dialog
5. **Počkejte** na dokončení (~10-30 sekund)
   - Uvidíte progress bar
   - Stavový řádek zobrazí průběh

6. Po dokončení:
   - Data se automaticky naparsují
   - Kanály se zobrazí v tabulce
   - Můžete **ukončit** klonovací režim na rádiu

### Ze souboru

1. **Menu: Soubor → Otevřít...** (nebo `Ctrl+O`)
2. Vyberte clone soubor (`.dat`, `.clone`)
3. Kanály se automaticky načtou

## Práce s kanály

### Zobrazení kanálů

- **Tabulka** zobrazuje všechny naprogramované kanály
- **Sloupce**:
  - Kanál: Číslo kanálu (1-999)
  - RX Frekvence: Příjmová frekvence v MHz
  - TX Frekvence: Vysílací frekvence v MHz
  - Režim: Provozní režim (FM, AM, USB, LSB, atd.)
  - Tón: CTCSS/DCS tón
  - Název: Tag/název kanálu
  - Přeskočit: Zda přeskočit při skenování

### Výběr kanálu

- Klikněte na **řádek** v tabulce
- Detailní informace se zobrazí v sekci **"Informace o kanálu"**

### Řazení

- Klikněte na **záhlaví sloupce** pro seřazení
- Další kliknutí obrátí pořadí

### Filtrování

⚠️ **Prototyp**: Filtrování zatím není implementováno

## Ukládání

### Do souboru

- **Uložit**: `Soubor → Uložit` (`Ctrl+S`)
  - Uloží do aktuálního souboru
- **Uložit jako**: `Soubor → Uložit jako...` (`Ctrl+Shift+S`)
  - Uloží do nového souboru

### Formát souboru

- Clone soubory jsou **binární**
- Obvykle přípona `.dat` nebo `.clone`
- Velikost: ~7898 bajtů
- **Kompatibilita**: Možná kompatibilní s CHIRP a ADMS-4B (netestováno)

## Zápis do rádia

⚠️ **VAROVÁNÍ**: Toto **přepíše všechna data** v rádiu!

### Postup

1. **Načtěte nebo otevřete** clone data
2. **Zkontrolujte** kanály v tabulce
3. **Vstupte do klonovacího režimu** na rádiu
4. **Připojte se** k rádiu
5. Klikněte na **"📤 Zapsat do rádia"**
6. **Potvrďte** varování
7. **Počkejte** na dokončení
8. **Ukončete** klonovací režim
9. **Zkontrolujte** kanály na rádiu

### Doporučení

- Před zápisem **zálohujte** aktuální data z rádia
- **Zkontrolujte** frekvence a nastavení
- **Otestujte** na prázdném kanálu nejprve

## Řešení problémů

### Aplikace nenajde sériový port

**Linux**:
```bash
# Přidejte uživatele do skupiny dialout
sudo usermod -a -G dialout $USER
# Odhlaste se a přihlaste znovu

# Nebo spusťte s sudo (nedoporučeno)
sudo python src/main.py
```

**Windows**:
- Zkontrolujte Správce zařízení
- Nainstalujte ovladače pro USB-to-Serial adaptér

### Timeout při čtení

- **Zkontrolujte** kabel a připojení
- **Ujistěte se**, že je rádio v klonovacím režimu
- **Zkuste nižší/vyšší rychlost** (vyžaduje úpravu kódu)
- **Restartujte** rádio a zkuste znovu

### Neplatná data

- **Ověřte** velikost souboru (~7898 bajtů)
- **Zkontrolujte** zdroj souboru
- **Zkuste** načíst přímo z rádia

### Chybné frekvence

⚠️ **Prototyp**: Parsování frekvencí je zjednodušené

- Pro správné parsování je potřeba implementovat **BCD dekódování**
- Použijte ověřený software (CHIRP) pro kritické operace

### Permission denied (Linux)

```bash
# Dočasné řešení
sudo chmod 666 /dev/ttyUSB0

# Trvalé řešení
sudo usermod -a -G dialout $USER
```

## Klávesové zkratky

- `Ctrl+O` - Otevřít soubor
- `Ctrl+S` - Uložit
- `Ctrl+Shift+S` - Uložit jako
- `Ctrl+Q` - Ukončit aplikaci

## Tipy a triky

### Záloha před experimentováním

```bash
# Vždy si zálohujte originální data
# Načtěte z rádia a uložte jako backup
```

### Práce s více rádiími

- Clone data jsou specifická pro rádio
- Označte soubory názvem rádia (např. `FT897_KA7OEI.dat`)

### Export do CSV (budoucí funkce)

⚠️ **Prototyp**: Export zatím není implementován

## Další čtení

- [README.md](../README.md) - Obecná dokumentace
- [CLAUDE.md](../CLAUDE.md) - Technická dokumentace
- [FT-897 Manual](http://www.yaesu.com) - Oficiální manuál

## Podpora

Pro hlášení chyb nebo otázky:
- Vytvořte issue na GitHubu
- Kontaktujte vývojáře

---

**Poznámka**: Toto je prototyp. Pro produkční použití doporučujeme ověřený software jako **CHIRP** nebo **ADMS-4B**.

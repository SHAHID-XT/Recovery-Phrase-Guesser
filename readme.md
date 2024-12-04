# Recovery Phrase Guesser

## Overview

The **Recovery Phrase Guesser** is a Python-based tool that demonstrates how brute-force techniques can be used to guess recovery phrases for accounts. It integrates browser automation and random phrase generation to test account access.

This project was developed as part of a challenge posed by a friend who claimed that it is impossible to hack or brute-force a cryptocurrency wallet. The goal of this project is to demonstrate that with sufficient resources and time, vulnerabilities in such systems can exist. This tool does **not** aim to promote illegal activities or harm; it is purely for educational and ethical purposes.

---

## Disclaimer

- **Use at Your Own Risk**: This tool is provided "as-is" for **educational purposes only**.
- **Legal Responsibility**: The author is **not responsible** for any misuse or legal consequences arising from using this tool.
- **Ethical Usage**: Only use this tool to test accounts that you **own** or have explicit permission to test.
- **No Malicious Intent**: The author does not condone or encourage illegal hacking, unauthorized access, or malicious activities.

By using this tool, you agree to take full responsibility for your actions and understand the potential risks involved.

---

## Features

1. **Phrase Generation**: Generates random recovery phrases from a predefined word list.
2. **Browser Automation**: Automates account recovery tests using Selenium-based drivers.
3. **Data Logging**:
   - Logs attempted recovery phrases in `recovery_phrases.json`.
   - Records valid accounts with potential balances in `balances.json`.
4. **Headless Browser Support**: Operates discreetly in headless mode.
5. **Customizable**: Allows phrase length and word list adjustments.

---

## Installation

1. **Install Dependencies**:
   Ensure you have Python 3.8+ installed, then install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Browser Driver**:
   - Ensure ChromeDriver is installed and properly configured in your system's PATH.
   - Place your extension files in the `panthom` directory.

---

## Usage

1. **Run the Script**:

   ```bash
   python main.py
   ```

2. **Outputs**:

   - **`recovery_phrases.json`**: Logs all tested recovery phrases.
   - **`balances.json`**: Logs valid recovery phrases linked to accounts with possible balances.

3. **Customization**:
   Modify the `word_list` or `phrase_length` in the script to fit your use case:
   ```python
   guesser = RecoveryPhraseGuesser(word_list=your_word_list, phrase_length=12)
   ```

---

## Purpose and Ethical Use

This project was created to prove a point: no system is entirely secure. It serves as a **proof of concept** to challenge the perception that cryptocurrency wallets are invulnerable to brute-force attacks.

However, this tool should **never** be used maliciously. Unauthorized access to someone else's account is a criminal offense. Use this tool solely for testing the security of your own accounts or with explicit permission.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Stay ethical, responsible, and mindful when using this tool.

---

##  Author: (Shahidxt)
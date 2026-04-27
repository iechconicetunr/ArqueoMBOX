# ArqueoMBOX - Historical Email Extractor and Sanitizer

*[Lea esta documentación en español](leerme.md)*

This repository contains **ArqueoMBOX**, a robust Python tool developed for the extraction, cleaning, and atomic fragmentation of historical email archives stored in `.mbox` and `.mbx` formats.

This tool is part of the Targeted Research Project (Investigación Orientada 2025) funded by the **Government of the Province of Santa Fe**, Argentina. The development was carried out by the **Digital Humanities Lab (LHD) of the IECH (UNR/CONICET)**, focused on integrating Artificial Intelligence into archival description for the processing of the Mario Levrero Digital Archive.

*Note: The creation and architectural design of this software were assisted by AI using Gemini Pro.*

## 📌 Key Features

Historical email formats present multiple challenges for processing via Large Language Models (LLMs) due to the high concentration of technical noise and obsolete encoding standards. This script solves these issues through:

* **Atomic Fragmentation:** Deconstructs large `.mbox` files into individual `.txt` files for each email, facilitating iterative processing.
* **Polyglot Decoding:** Integrates a translation fallback system that rescues Spanish characters (accents, 'ñ') by safely iterating through historical encodings (`latin-1`, `windows-1252`, `iso-8859-1`).
* **HTML Sanitization:** Uses regular expressions (`re`) to clean emails encapsulated in `<x-html>` tags, extracting exclusively the human-readable text.
* **Emergency Fallback (Forced Recovery):** Implements a contingency mechanism for emails with severely corrupted MIME structures (e.g., defective exports from legacy clients like *Qualcomm Eudora 5*). It extracts information at the raw text level while preserving invaluable forensic footprints.

## ⚙️ Requirements

The tool is designed to be lightweight and easy to deploy. It does not require the installation of third-party libraries via `pip`, as it strictly utilizes native Python modules:
* `Python 3.x`
* Native libraries used: `mailbox`, `os`, `email`, `re`.

## 🚀 Usage Instructions

1. **Clone the repository** or download the `arqueombox.py` file to your local machine.
2. **Prepare your files:** Place your `.mbox` or `.mbx` files in the same directory as the script.
3. **Execute the tool:** Open your terminal or command prompt, navigate to the project folder, and run:

   ```bash
   python3 arqueombox.py

4. **Interactive Menu:** The script will automatically detect compatible files in the directory and present a menu (in Spanish) allowing you to process a specific file or batch-process all found files.

5. **Results:** A new folder named corpus_limpio will be generated automatically in the same directory. Inside, you will find all extracted emails as clean, numbered .txt files, ready to be consumed by Artificial Intelligence models or relational databases.

👥 Team & Acknowledgments

**Development:** Digital Humanities Lab (LHD) - IECH (UNR/CONICET).

**Funding:** Targeted Research Program 2025 (IO 2025), Government of the Province of Santa Fe.

**AI Assistance:** Code generation assisted by Gemini Pro.

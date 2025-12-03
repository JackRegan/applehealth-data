# Apple Health A.I. Data Analyzer - MOD (V2)

This Python tool is originally developed by Krumjahn - https://github.com/krumjahn

All credit for the original code, setup, and documentation goes to Krumjahn. This V2 README preserves all original instructions and features, but documents additional capabilities added in this fork.

---

## 🆕 Additional Features in V2

- **Query CSV, GPX, and FIT files**: You can now analyze Apple Health data exported in CSV, GPX, or FIT formats, not just XML.
- **Flexible file support**: The tool automatically detects and summarizes all supported file types in your chosen directory.
- **LLM-powered analysis for all formats**: Use local Ollama or remote LLMs to analyze any supported file type, including running and cycling metrics from GPX/FIT files.
- **Improved error handling**: The tool skips empty or invalid files and warns you, instead of crashing.
- **Custom queries**: Pass your own analysis question to the LLM using the `--query` option.

## 📝 Credit to Original Author

This project is based on the work of Krumjahn. All setup, installation, and usage instructions below are from the original README and remain unchanged. Please give all credit to the original author for their work.

---

# Original Setup & Usage Instructions

<details>
<summary>Click to expand original README</summary>

```
# Apple Health A.I. Data Analyzer - MOD

This Python tool is origionally developed by Krumjahn - https://github.com/krumjahn 

In my testing I found that the Apple Health export doesnt contain the workout details of a run - eg cadence, pace details, splits, GPS etc.

I am experimenting with using this code as a base and using exported data from iOS / App HealthKit - which does seem to cointain a semblance more data.

ALL BELOW IS BLATANT PLAGURISM AND BASED ON THE ORGIONAL CODE.  IF YOU STUMBLE ACROSS THIS PLEASE GIVE ALL CREDIT TO ORIGINAL AUTHOR.

---

A Python tool that transforms Apple Health export data into insightful visualizations and analytics, with AI-powered analysis. Easily track your fitness journey with detailed analysis of steps, workouts, heart rate, sleep, and more. Features specialized support for WHOOP workout data and ChatGPT integration for personalized insights.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- 📊 Interactive data visualizations for all metrics
- 🤖 AI-powered analysis using ChatGPT
- 💪 Workout duration tracking and analysis
- ❤️ Heart rate patterns and trends
- 🏃‍♂️ Daily activity metrics (steps, distance)
- ⚖️ Weight tracking over time
- 😴 Sleep pattern analysis
- 🔄 WHOOP workout integration
- 🧠 **Local LLM Support** - Analyze data privately using Ollama models like Deepseek-R1
- 🌐 **External LLM Support** (New!) - Connect to remote Ollama instances for analysis

## 📺 Youtube tutorial

[Watch youtube tutorial here](https://youtu.be/5FCFRYbXHjg)

## ⚡ Quick Start

Local (recommended for interactive charts)

```bash
# 1) Clone and enter the repo
git clone https://github.com/krumjahn/applehealth.git
cd applehealth

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app (you'll be prompted for export.xml; outputs go to ./health_out)
python src/applehealth.py

# Optional: Advanced flags if you already know the paths
# python src/applehealth.py --export "/absolute/path/to/export.xml" --out "./health_out"
```

Docker (saves charts/CSVs to your host folder)

```bash
# 1) Build the image
docker build -t applehealth .

# 2) Run the container (quote paths with spaces)
```
... (full original README content continues)
```
</details>

---

## How to Use the New Features

### Querying CSV, GPX, and FIT Files

You can now run:

```bash
python src/applehealth_healthkit_llm_query.py --dir <your_data_dir> --query "Summarize my running and cycling activities in the past 14 days."
```
- The tool will automatically find and analyze all supported files in the directory.
- You can use any custom query for the LLM.

### Error Handling
- Empty or invalid files are skipped with a warning.
- Only valid health data files are processed.

---

## License & Attribution

This project remains under the MIT License. All original code and documentation are credited to Krumjahn. This fork only adds new file support and LLM features.

---

If you use this tool, please star the original repo and credit the author!

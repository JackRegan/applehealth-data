"""
Apple HealthKit LLM Query Script
--------------------------------

This script scans a directory for Apple HealthKit data files (.csv, .gpx, .fit), summarizes their contents, and sends a prompt to a local Ollama LLM for analysis and insights.

Usage:
    python applehealth_healthkit_llm_query.py --dir <directory> [--query "Your question"] [--model <ollama-model>]

Options:
    --dir   Directory to search for data files (default: current directory)
    --query Custom question or prompt for the LLM (optional)
    --model Ollama model to use (default: deepseek-r1)

Supported file types:
    - CSV (.csv): Tabular health data
    - GPX (.gpx): GPS track data (with optional heart rate, elevation, etc.)
    - FIT (.fit): Fitness device binary files (e.g., Garmin, Wahoo)

Example:
    python applehealth_healthkit_llm_query.py --dir healthdata --query "Summarize my running and cycling activities."

Requirements:
- pandas
- gpxpy
- fitparse
- ollama
- fitparse
- ollama
"""

import os
import sys
import argparse
import pandas as pd
import ollama
from datetime import datetime
import gpxpy
import fitparse

def summarize_csv(file_path):
    df = pd.read_csv(file_path)
    summary = {}
    summary['file'] = os.path.basename(file_path)
    summary['total_records'] = len(df)
    summary['columns'] = list(df.columns)
    if 'Date' in df.columns:
        summary['date_range'] = f"{df['Date'].min()} to {df['Date'].max()}"
    else:
        summary['date_range'] = 'N/A'
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        summary[col] = {
            'mean': df[col].mean(),
            'min': df[col].min(),
            'max': df[col].max()
        }
    summary['sample'] = df.head(10).to_dict(orient='records')
    return summary

def summarize_gpx(file_path):
    with open(file_path, 'r') as f:
        gpx = gpxpy.parse(f)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                pt = {
                    'time': point.time,
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation
                }
                if point.extensions:
                    for ext in point.extensions:
                        for child in ext:
                            if 'hr' in child.tag.lower():
                                pt['heart_rate'] = child.text
                points.append(pt)
    summary = {
        'file': os.path.basename(file_path),
        'type': 'gpx',
        'total_points': len(points),
        'start_time': str(points[0]['time']) if points else 'N/A',
        'end_time': str(points[-1]['time']) if points else 'N/A',
        'sample_points': points[:10]
    }
    return summary

def summarize_fit(file_path):
    fitfile = fitparse.FitFile(file_path)
    records = []
    for record in fitfile.get_messages('record'):
        rec = {}
        for d in record:
            rec[d.name] = d.value
        records.append(rec)
    summary = {
        'file': os.path.basename(file_path),
        'type': 'fit',
        'total_records': len(records),
        'fields': list(records[0].keys()) if records else [],
        'sample_records': records[:10]
    }
    return summary

def build_llm_prompt(summaries, user_query=None):
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"Today's date is {today}. Always use this as the current date.\n\nAnalyze this Apple Health CSV data and provide insights.\n\n"
    for summary in summaries:
        prompt += f"File: {summary['file']}\n"
        if summary.get('type') == 'gpx':
            prompt += f"Type: GPX\nTotal Points: {summary['total_points']}\nStart: {summary['start_time']}\nEnd: {summary['end_time']}\nSample Points: {summary['sample_points']}\n"
        elif summary.get('type') == 'fit':
            prompt += f"Type: FIT\nTotal Records: {summary['total_records']}\nFields: {summary['fields']}\nSample Records: {summary['sample_records']}\n"
        else:
            prompt += f"Total Records: {summary['total_records']}\n"
            prompt += f"Columns: {summary['columns']}\n"
            prompt += f"Date Range: {summary['date_range']}\n"
            for col in summary:
                if isinstance(summary[col], dict):
                    prompt += f"{col}: mean={summary[col]['mean']}, min={summary[col]['min']}, max={summary[col]['max']}\n"
            prompt += f"Sample Rows:\n{summary['sample']}\n"
        prompt += "\n" + "="*40 + "\n"
    if user_query:
        prompt += f"\nUser Query: {user_query}\n"
    else:
        prompt += "Please provide a comprehensive analysis including:\n1. Notable patterns or trends\n2. Unusual findings\n3. Actionable health insights\n4. Areas for improvement\n"
    return prompt

def query_ollama(prompt, model='deepseek-r1'):
    print("Contacting Ollama...")
    collected = []
    try:
        stream = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a health data analyst. Provide detailed analysis and actionable insights."},
                {"role": "user", "content": prompt}
            ],
            options={'temperature': 0.3, 'num_ctx': 6144},
            stream=True,
        )
        for chunk in stream:
            text = chunk.get('response') or (chunk.get('message') or {}).get('content') or ''
            if text:
                collected.append(text)
                print(text, end='', flush=True)
        print("\nDone.")
    except Exception as e:
        print(f"Error: {e}")
    return ''.join(collected)

def main():
    parser = argparse.ArgumentParser(description="Query Apple Health CSV/GPX/FIT data and send to Ollama LLM.")
    parser.add_argument('--dir', type=str, default='.', help='Directory to search for data files (default: current directory)')
    parser.add_argument('--model', default='deepseek-r1', help='Ollama model to use')
    parser.add_argument('--query', type=str, default=None, help='Custom query or question for the LLM')
    args = parser.parse_args()

    import glob
    search_dir = os.path.abspath(args.dir)
    file_patterns = [
        os.path.join(search_dir, '*.csv'),
        os.path.join(search_dir, '*.gpx'),
        os.path.join(search_dir, '*.fit'),
    ]
    data_files = []
    for pattern in file_patterns:
        data_files.extend(glob.glob(pattern))
    if not data_files:
        print(f"No .csv, .gpx, or .fit files found in {search_dir}.")
        sys.exit(1)

    summaries = []
    for f in data_files:
        ext = os.path.splitext(f)[1].lower()
        if ext == '.csv':
            summaries.append(summarize_csv(f))
        elif ext == '.gpx':
            summaries.append(summarize_gpx(f))
        elif ext == '.fit':
            summaries.append(summarize_fit(f))
        else:
            print(f"Unsupported file type: {f}")
    if not summaries:
        print("No supported files to summarize.")
        sys.exit(1)
    prompt = build_llm_prompt(summaries, user_query=args.query)
    query_ollama(prompt, model=args.model)

if __name__ == '__main__':
    main()
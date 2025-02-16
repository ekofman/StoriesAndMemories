#!/usr/bin/env python3
import re

# === CONFIGURATION and FILE PATHS ===
# (Update these paths if necessary.)
spanish_transcript_file = "transcripts/RositaInterview4_29_20-11_17_23.txt"
english_transcript_file = "transcripts/RositaInterview4_29_20-11_17_23_English.txt"
audio_file = "audio/RositaInterview4_29_20-11_17_23.mp3"
output_file = "RositaInterview.html"

# === REGEX for TIMESTAMP LINES ===
# We assume a timestamp line is exactly in the format "H:MM:SS" (for example: "0:00:00")
timestamp_re = re.compile(r"^(\d+):(\d+):(\d+)$")

def timestamp_to_seconds(ts_str):
    """Convert a timestamp string (H:MM:SS) to total seconds."""
    parts = ts_str.strip().split(":")
    if len(parts) != 3:
        return None
    try:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return None

def extract_main_points(lines):
    """
    From the Spanish transcript lines, extract every line that exactly matches
    a timestamp. For each timestamp found, create a dictionary with:
      - id: a generated section id (like "section-1")
      - title: a generated title (e.g. "Section 1"). (You can modify this logic.)
      - start_time: the timestamp in seconds.
      - display_time: the original timestamp text.
    Returns a list of main point dictionaries.
    """
    points = []
    for line in lines:
        stripped = line.strip()
        if timestamp_re.match(stripped):
            seconds = timestamp_to_seconds(stripped)
            point = {
                "id": f"section-{len(points)+1}",
                "title": f"Section {len(points)+1}",
                "start_time": seconds,
                "display_time": stripped
            }
            points.append(point)
    return points

def partition_transcript(lines, main_points):
    """
    Partition transcript lines into sections defined by main_points.
    Returns a dictionary mapping each section id to the accumulated text.
    The function uses the timestamp lines (in the transcript) to decide when to switch
    from one section to the next.
    """
    sections = {mp["id"]: "" for mp in main_points}
    current_index = 0
    current_section_id = main_points[current_index]["id"]

    for line in lines:
        stripped = line.strip()
        # If this line is exactly a timestamp line, then check whether to advance.
        if timestamp_re.match(stripped):
            current_time = timestamp_to_seconds(stripped)
            # Advance the section if the current timestamp is equal to or later than
            # the next main point's start time.
            while (current_index + 1 < len(main_points) and
                   current_time is not None and
                   current_time >= main_points[current_index + 1]["start_time"]):
                current_index += 1
                current_section_id = main_points[current_index]["id"]
        sections[current_section_id] += line
    return sections

# === READ TRANSCRIPT FILES ===
with open(spanish_transcript_file, "r", encoding="utf-8") as f:
    spanish_lines = f.readlines()

with open(english_transcript_file, "r", encoding="utf-8") as f:
    english_lines = f.readlines()

# === EXTRACT MAIN POINTS FROM THE SPANISH TRANSCRIPT ===
main_points = extract_main_points(spanish_lines)
if not main_points:
    print("No timestamp lines found in the Spanish transcript. Exiting.")
    exit(1)

# === PARTITION BOTH TRANSCRIPTS USING THE SAME MAIN POINTS ===
spanish_sections = partition_transcript(spanish_lines, main_points)
english_sections = partition_transcript(english_lines, main_points)

# === BUILD THE HTML CONTENT ===
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rosita Interview - Bilingual Transcript</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        /* Audio player and TOC styling */
        #toc {{
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 20px;
        }}
        #toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        #toc li {{
            margin-bottom: 8px;
        }}
        /* Fixed-height transcript container with scrolling */
        #transcript-container {{
            border: 1px solid #ccc;
            height: 600px;
            overflow-y: auto;
            padding: 10px;
            margin-top: 20px;
        }}
        /* Ensure that section anchors are not hidden (extra top padding) */
        .section-anchor {{
            padding-top: 60px;
            margin-top: -60px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .lang-title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        pre {{
            white-space: pre-wrap;
            background-color: #f3f3f3;
            padding: 10px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <h1>Rosita Interview - Bilingual Transcript</h1>

    <!-- Audio Player -->
    <audio id="audioPlayer" controls>
        <source src="{audio_file}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>

    <!-- Table of Contents -->
    <div id="toc">
        <h2>Table of Contents</h2>
        <ul>
"""

# Build TOC links using the extracted main points.
for mp in main_points:
    html_content += f'            <li><a href="#{mp["id"]}" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n'

html_content += """        </ul>
    </div>

    <!-- Transcript Container (scrollable) -->
    <div id="transcript-container">
"""

# For each main point, output a section that includes both English and Spanish parts.
for mp in main_points:
    sid = mp["id"]
    html_content += f'        <div id="{sid}" class="section-anchor section">\n'
    html_content += f'            <h3>{mp["title"]} ({mp["display_time"]})</h3>\n'
    html_content += '            <div class="lang-section english-section">\n'
    html_content += '                <div class="lang-title">English:</div>\n'
    html_content += f'                <pre>{english_sections.get(sid, "").strip()}</pre>\n'
    html_content += '            </div>\n'
    html_content += '            <div class="lang-section spanish-section">\n'
    html_content += '                <div class="lang-title">Español:</div>\n'
    html_content += f'                <pre>{spanish_sections.get(sid, "").strip()}</pre>\n'
    html_content += '            </div>\n'
    html_content += '        </div>\n\n'

html_content += """    </div>

    <script>
        // Function to jump the audio player to a specified time (in seconds)
        function jumpToTime(seconds) {
            var audio = document.getElementById("audioPlayer");
            audio.currentTime = seconds;
            audio.play();
        }
        // Function to jump both the audio and scroll the transcript container to the designated section.
        function jumpToSection(sectionId, seconds) {
            jumpToTime(seconds);
            var container = document.getElementById("transcript-container");
            var target = document.getElementById(sectionId);
            if (target) {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }
    </script>
</body>
</html>
"""

# === WRITE THE OUTPUT HTML FILE ===
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file generated: {output_file}")

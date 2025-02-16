#!/usr/bin/env python3
import re

# === CONFIGURATION: File Locations ===
transcript_file = "transcripts/RositaInterview4_29_20-11_17_23_English.txt"
audio_file = "audio/RositaInterview4_29_20-11_17_23.mp3"
output_file = "RositaInterview.html"

# === Define the Main Points (Granular Sections) with Detailed Descriptions ===
# The start_time is in seconds (converted from H:MM:SS) and display_time is the original timestamp string.
# Adjust these values as needed.
main_points = [
    {
        "id": "section-1",
        "title": "WWII Outbreak and Early Reflections on the War",
        "start_time": 0,          # 0:00:00
        "display_time": "0:00:00"
    },
    {
        "id": "section-2",
        "title": "Mina and Brana's Journey from Orhei/Orgeyev to Lisbon",
        "start_time": 19,         # 0:00:19
        "display_time": "0:00:19"
    },
    {
        "id": "section-3",
        "title": "A Childhood Memory: The Unusual Bathing Incident",
        "start_time": 122,        # 0:02:02
        "display_time": "0:02:02"
    },
    {
        "id": "section-4",
        "title": "Family Background: León’s Parents and the Vicuña Mackenna Building",
        "start_time": 253,        # 0:04:13
        "display_time": "0:04:13"
    },
    {
        "id": "section-5",
        "title": "Religious Practices and Abram’s Devotion in the Family",
        "start_time": 370,        # ~0:06:10
        "display_time": "0:06:10"
    },
    {
        "id": "section-7",
        "title": "Ester's Second Marriage",
        "start_time": 464,        # ~0:07:44
        "display_time": "0:07:44"
    },
    {
        "id": "section-8",
        "title": "Descriptions of Ester's Personality",
        "start_time": 531,        # ~0:08:51
        "display_time": "0:08:51"
    },
    {
        "id": "section-9",
        "title": "The Importance of Education in Ester's Family",
        "start_time": 675,        # ~0:11:15
        "display_time": "0:11:15"
    },
    {
        "id": "section-10",
        "title": "International Connections and Memories of David Braylovsky",
        "start_time": 961,        # ~0:16:01 — adjust as needed
        "display_time": "0:16:01"
    },
    {
        "id": "section-11",
        "title": "Rosita's Memories of Her Father",
        "start_time": 1265,       # ~0:21:05
        "display_time": "0:21:05"
    },
    {
        "id": "section-12",
        "title": "The Marble House, Earthquake, and Family Tragedy",
        "start_time": 1341,       # ~0:22:21
        "display_time": "0:22:21"
    },
    {
        "id": "section-13",
        "title": "School Memories and Early Friendships in Concepción",
        "start_time": 1500,       # ~0:25:00
        "display_time": "0:25:00"
    },
    {
        "id": "section-14",
        "title": "Language Challenges and Pursuing Further Education",
        "start_time": 1578,       # ~0:26:18
        "display_time": "0:26:18"
    },
    {
        "id": "section-15",
        "title": "Natalio Berman, Communist Congressman and Friend of José's",
        "start_time": 1635,       # ~0:27:15
        "display_time": "0:27:15"
    },
    {
        "id": "section-16",
        "title": "Observations on the Early Pandemic",
        "start_time": 1860,       # ~0:31:00
        "display_time": "0:31:00"
    }
]

# === Regular Expression for Timestamp Lines ===
timestamp_re = re.compile(r"^\d+:\d{2}:\d{2}$")

def timestamp_to_seconds(ts_str):
    """Convert a timestamp string in H:MM:SS format to total seconds."""
    parts = ts_str.strip().split(":")
    if len(parts) != 3:
        return None
    try:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return None

# === Process the Transcript ===
output_lines = []
mp_index = 0  # pointer into the main_points list

with open(transcript_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    stripped = line.strip()
    if timestamp_re.match(stripped) and mp_index < len(main_points):
        current_time = timestamp_to_seconds(stripped)
        # Insert anchor div(s) while the current timestamp meets or exceeds the next section's start_time.
        while mp_index < len(main_points) and current_time is not None and current_time >= main_points[mp_index]["start_time"]:
            anchor_html = f'<div id="{main_points[mp_index]["id"]}" class="section-anchor"></div>\n'
            output_lines.append(anchor_html)
            mp_index += 1
    output_lines.append(line)

while mp_index < len(main_points):
    anchor_html = f'<div id="{main_points[mp_index]["id"]}" class="section-anchor"></div>\n'
    output_lines.append(anchor_html)
    mp_index += 1

processed_transcript = "".join(output_lines)

# === Format Speaker Names and Convert Timestamps to Clickable Links ===
# Wrap speaker names ("Rosita" and "Eric") in span tags.
processed_transcript = re.sub(r"^(Rosita)", r'<span class="speaker-rosita">\1</span>', processed_transcript, flags=re.MULTILINE)
processed_transcript = re.sub(r"^(Eric)", r'<span class="speaker-eric">\1</span>', processed_transcript, flags=re.MULTILINE)

# Replace lines that are exactly a timestamp with a clickable link.
def timestamp_link(match):
    ts = match.group(1)
    seconds = timestamp_to_seconds(ts)
    return f'<a href="#" class="timestamp" onclick="jumpToTime({seconds}); return false;">{ts}</a>'

processed_transcript = re.sub(r"^(\d+:\d{2}:\d{2})$", timestamp_link, processed_transcript, flags=re.MULTILINE)

# === Build the HTML Content ===
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rosita Interview - Transcript</title>
    <style>
        body {{
            font-family: Arial, sans-serif;	
	    font-size: 10.2pt;
            margin: 20px;
        }}
        /* Flex container for side-by-side layout */
        #container {{
            display: flex;
            gap: 20px;
        }}
        /* Table of Contents styling */
        #toc {{
            flex: 1; /* approx 1/3 of container width */
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 30px;
        }}
        #toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        #toc li {{
            margin-bottom: 8px;
        }}
        #toc a {{
            text-decoration: none;
            color: #333333;
        }}
        #toc a:hover {{
            text-decoration: underline;
        }}
        /* Transcript container styling */
        #transcript-container {{
            flex: 2; /* approx 2/3 of container width */
            border: 1px solid #ccc;
            height: 70vh;
            overflow-y: auto;
            padding: 30px;
        }}
        /* Title above Transcript */
        #transcript-title {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        /* Anchor div styling: extra top padding so that the header is not hidden */
        .section-anchor {{
            padding-top: 60px;
            margin-top: -60px;
        }}
        pre {{
            white-space: pre-wrap;
        }}
        /* Speaker name styling */
        .speaker-rosita {{
            color: darkblue;
            font-weight: bold;
        }}
        .speaker-eric {{
            color: darkgreen;
            font-weight: bold;
        }}
        /* Timestamp styling using Roboto and bold */
        .timestamp {{
            font-family: 'Roboto', sans-serif;
            font-weight: bold;
            color: black;
        }}
    </style>
    <!-- Import Roboto from Google Fonts -->
    <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">
</head>
<body>
    <h1>Rosita Interview - Transcript</h1>
    <!-- Audio Player -->
    <audio id="audioPlayer" controls>
        <source src="{audio_file}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <!-- Flex Container for TOC and Transcript -->
    <div id="container">
        <!-- Table of Contents -->
        <div id="toc">
            <h2>Table of Contents</h2>
            <ul>
"""
for mp in main_points:
    html_content += f'                <li><a href="#{mp["id"]}" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n'
html_content += """            </ul>
        </div>
        <!-- Transcript Container -->
        <div id="transcript-container">
            <pre>
"""
html_content += processed_transcript
html_content += """            </pre>
        </div>
    </div>
    <script>
        // Function to jump the audio player to a specified time (in seconds)
        function jumpToTime(seconds) {
            var audio = document.getElementById("audioPlayer");
            audio.currentTime = seconds;
            audio.play();
        }
        // Function to jump both the audio and scroll the transcript container to the specified section
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

# === Write the HTML Content to the Output File ===
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file generated: {output_file}")

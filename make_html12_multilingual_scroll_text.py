#!/usr/bin/env python3
import re
import sys
import json
import os

# --- Load JSON Data from External Files ---
with open("config.json", "r", encoding="utf-8") as f:
    config_dict = json.load(f)

# Load main points from separate JSON files in the main_points folder.
main_points_dict = {}
for key, conf in config_dict.items():
    main_points_path = os.path.join("main_points", conf["page_id"] + ".json")
    try:
        with open(main_points_path, "r", encoding="utf-8") as f:
            main_points_dict[conf["page_id"]] = json.load(f)
    except FileNotFoundError:
        main_points_dict[conf["page_id"]] = []

with open("images.json", "r", encoding="utf-8") as f:
    image_dict = json.load(f)

# --- Regular Expression for Timestamp Lines ---
timestamp_re = re.compile(r"^\d+:\d{2}:\d{2}$")

def timestamp_to_seconds(ts_str):
    parts = ts_str.strip().split(":")
    if len(parts) != 3:
        return None
    try:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return None

# === Function to Process a Transcript File (inserts anchors and formats timestamps) ===
def process_transcript(file_path, main_points_list):
    output_lines = []
    mp_index = 0
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        stripped = line.strip()
        if timestamp_re.match(stripped) and mp_index < len(main_points_list):
            current_time = timestamp_to_seconds(stripped)
            while mp_index < len(main_points_list) and current_time is not None and current_time >= main_points_list[mp_index]["start_time"]:
                anchor_html = f'<div id="{main_points_list[mp_index]["id"]}" class="section-anchor"></div>\n'
                output_lines.append(anchor_html)
                mp_index += 1
        output_lines.append(line)
    while mp_index < len(main_points_list):
        anchor_html = f'<div id="{main_points_list[mp_index]["id"]}" class="section-anchor"></div>\n'
        output_lines.append(anchor_html)
        mp_index += 1
    processed = "".join(output_lines)
    # Wrap speaker names
    processed = re.sub(r"^(Rosita)", r'<span class="speaker-rosita">\1</span>', processed, flags=re.MULTILINE)
    processed = re.sub(r"^(Eric)", r'<span class="speaker-eric">\1</span>', processed, flags=re.MULTILINE)
    # Make timestamp-only lines clickable
    def timestamp_link(match):
        ts = match.group(1)
        seconds = timestamp_to_seconds(ts)
        return f'<a href="#" class="timestamp" onclick="jumpToTime({seconds}); return false;">{ts}</a>'
    processed = re.sub(r"^(\d+:\d{2}:\d{2})$", timestamp_link, processed, flags=re.MULTILINE)
    return processed

# === Function to Generate a Single HTML Page with Navigation, Image, TOC, and Transcript Toggle ===
def generate_page_with_nav(config, main_points_list, all_configs):
    # Process transcripts.
    # Default to Spanish transcript if available.
    if "spanish_transcript_file" in config:
        processed_sp = process_transcript(config["spanish_transcript_file"], main_points_list)
    else:
        processed_sp = ""
    if "transcript_file" in config:
        processed_en = process_transcript(config["transcript_file"], main_points_list)
    else:
        processed_en = ""
    
    # Build the navigation block (as a flat, table-like nav bar).
    nav_links = []
    for key, conf in all_configs.items():
        if conf["page_id"] == config["page_id"]:
            nav_links.append(f'<a href="{conf["output_file"]}" class="nav-link selected">{conf["page_title"]}</a>')
        else:
            nav_links.append(f'<a href="{conf["output_file"]}" class="nav-link">{conf["page_title"]}</a>')
    nav_block = "".join(nav_links)
    
    # Build a JavaScript JSON string for the image dictionary.
    section_images_json = json.dumps(image_dict)
    
    # Build the HTML content.
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{config["page_title"]}</title>
    <style>
/* Global Styles */
body {{
  font-family: 'Roboto', sans-serif;
  margin: 20px;
  background-color: #f0f2f5;
  color: #333;
}}

/* Navigation Bar styled as flat buttons */
#nav {{
  display: flex;
  justify-content: center;
  gap: 0;
  margin-bottom: 5px;
  border-bottom: 1px solid #e0e0e0;
}}
.nav-link {{
  flex: 1;
  padding: 5px 5px;
  text-align: center;
  font-size: 0.85em;
  text-decoration: none;
  color: #555;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  transition: background-color 0.3s, color 0.3s;
}}
.nav-link:last-child {{
  border-right: none;
}}
.nav-link:hover {{
  background-color: #e9eff5;
  color: #222;
}}
.nav-link.selected {{
  background-color: #007acc;
  color: #ffffff;
  pointer-events: none;
}}

/* Audio Player */
audio {{
  width: 100%;
  margin-bottom: 10px;
  max-height: 20px;
}}

/* Main Container for Two Vertical Columns */
#main-container {{
  display: flex;
  gap: 20px;
  height: calc(100vh - 140px);
}}

/* Left Column: Image and TOC */
#left-column {{
  width: 50%;
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #ffffff;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}}
/* Image Container (upper 55%) */
#image-container {{
  height: 55%;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
}}
#image-container img {{
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}}
#buttons {{
  text-align: center;
  margin-bottom: 2px;
}}
#buttons button {{
  display: inline-block;
  background-color: rgba(255, 255, 255, 0.8);
  border: none;
  cursor: pointer;
  font-size: 1.2em;
  color: #007acc;
  padding: 2px 5px;
  transition: background-color 0.3s, color 0.3s;
  margin: 0 2px;
}}
#buttons button:hover {{
  background-color: rgba(150, 150, 150, 0.8);
  color: gray;
}}
#buttons button:active {{
  background-color: rgba(100, 100, 100, 0.8);
  color: darkgray;
}}
#image-subtitle {{
  margin-top: 10px;
  font-size: 0.7em;
  color: #555;
  text-align: center;
}}

/* TOC Container (lower 45%) */
#toc-container {{
  height: 45%;
  overflow-y: auto;
  background-color: #fafafa;
  border-top: 1px solid #e0e0e0;
  padding: 10px;
}}
#toc-container h2 {{
  margin: 0 0 10px 0;
  font-size: 1.2em;
  color: #007acc;
}}
#toc-container ul {{
  list-style: none;
  padding: 0;
  margin: 0;
}}
#toc-container li {{
  margin-bottom: 8px;
}}
#toc-container a {{
  text-decoration: none;
  color: #555;
  transition: color 0.3s;
}}
#toc-container a:hover {{
  color: #007acc;
}}

/* Right Column: Transcript with Toggle */
#right-column {{
  width: 50%;
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow-y: auto;
  padding: 15px;
}}
#transcript-toggle {{
  text-align: center;
  margin-bottom: 10px;
}}
#transcript-toggle button {{
  margin: 0 5px;
  padding: 8px 15px;
  background-color: #007acc;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}}
#transcript-toggle button:hover {{
  background-color: #005fa3;
}}
#transcript-content pre {{
  white-space: pre-wrap;
  font-size: 1em;
  line-height: 1.6;
}}

/* Anchor Div Styling */
.section-anchor {{
  padding-top: 60px;
  margin-top: -60px;
}}

/* Speaker Name Styling */
.speaker-rosita {{
  color: #007acc;
  font-weight: bold;
}}
.speaker-eric {{
  color: #228b22;
  font-weight: bold;
}}

/* Timestamp Styling */
.timestamp {{
  font-family: 'Roboto', sans-serif;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  transition: color 0.3s;
}}
.timestamp:hover {{
  color: #007acc;
}}
    </style>
    <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">
</head>
<body>
    <h1>{config["page_title"]}</h1>
    <!-- Navigation Block -->
    <div id="nav">{nav_block}</div>
    <!-- Audio Player -->
    <audio id="audioPlayer" controls>
        <source src="{config["audio_file"]}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <!-- Main Container with Two Columns -->
    <div id="main-container">
        <!-- Left Column: Buttons, Image Subtitle, Image, and TOC -->
        <div id="left-column">
            <div id="buttons">
                <button id="prev-image" onclick="prevImage()">&#9664;</button>
                <button id="next-image" onclick="nextImage()">&#9654;</button>
            </div>
            <div id="image-subtitle"></div>
            <div id="image-container">
                <img id="current-image" src="" alt="Image">
            </div>
            <div id="toc-title">
                <h2>Table of Contents</h2>
            </div>
            <div id="toc-container">
                <div id="toc">
                    <ul>
"""
    for mp in main_points_list:
        html_content += f'                        <li><a href="#{mp["id"]}" id="link-{mp["id"]}" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n'
    html_content += """                    </ul>
                </div>
            </div>
        </div>
        <!-- Right Column: Transcript with Toggle -->
        <div id="right-column">
            <div id="transcript-toggle">
                <button onclick="showTranscript('spanish')">Spanish</button>
                <button onclick="showTranscript('english')">English</button>
            </div>
            <div id="transcript-content">
                <pre id="transcript-pre">
"""
    if processed_sp:
        html_content += processed_sp
    else:
        html_content += processed_en
    html_content += """                </pre>
            </div>
        </div>
    </div>
    <script>
    // Global array of section images from image_dict.
    var sectionImages = """ + section_images_json + """;
    // mainPoints is already defined from the JSON dump of your main_points_list.
    var mainPoints = """ + json.dumps(main_points_list) + """;

    // Function to update the TOC styles based on the current section.
function updateToc() {
    var tocContainer = document.getElementById("toc-container");
    for (var i = 0; i < mainPoints.length; i++) {
        var section_id = mainPoints[i].id;
        var tocEntry = document.getElementById("link-" + section_id);
        if (section_id === currentSectionId) {
            tocEntry.style.color = "black";
            // Check if the tocEntry is fully visible within its container.
            var containerRect = tocContainer.getBoundingClientRect();
            var entryRect = tocEntry.getBoundingClientRect();
            if (entryRect.top < containerRect.top || entryRect.bottom > containerRect.bottom) {
                tocEntry.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
        } else {
            tocEntry.style.color = "gray";
        }
    }
}

    // Helper function to update the image based on the section that is in view.
    function updateImageForSection(sectionId) {
        // Find the main point with this section ID.
        var point = mainPoints.find(function(pt) {
            return pt.id === sectionId;
        });
        // Only update the image if the point has an "image" property and that key exists.
        if (point && point.hasOwnProperty("image") && sectionImages.hasOwnProperty(point.image)) {
            document.getElementById("current-image").src = sectionImages[point.image].src;
           document.getElementById("image-subtitle").textContent = sectionImages[point.image].textContent;
        }
        // Otherwise, leave the current image and subtitle as they are.
     }

    // Functions for manual image navigation.
    function prevImage() {
        // Loop through mainPoints backwards to find the previous section with an image.
        for (var i = mainPoints.length - 1; i >= 0; i--) {
            if (mainPoints[i].hasOwnProperty("image")) {
                if (mainPoints[i].id < currentSectionId) { // simplistic check; you may need a better comparison
                    currentSectionId = mainPoints[i].id;
                    updateImageForSection(currentSectionId);
                    updateToc();
                    return;
                }
            }
        }
    }

    function nextImage() {
        // Loop through mainPoints forwards to find the next section with an image.
        for (var i = 0; i < mainPoints.length; i++) {
            if (mainPoints[i].hasOwnProperty("image")) {
                if (mainPoints[i].id > currentSectionId) { // simplistic check; adjust as needed
                    currentSectionId = mainPoints[i].id;
                    updateImageForSection(currentSectionId);
                    updateToc();
                    return;
                }
            }
        }
    }

    // Initially set the current section.
    var currentSectionId = "section-1";
    // Initially update TOC and image.
    updateToc();
    updateImageForSection(currentSectionId);

    // Transcript toggle logic.
    var transcriptPre = document.getElementById("transcript-pre");
    var transcriptEnglish = """ + json.dumps(processed_en) + """;
    var transcriptSpanish = """ + json.dumps(processed_sp) + """;
    function showTranscript(lang) {
        if (lang === "english") {
            transcriptPre.innerHTML = transcriptEnglish;
        } else {
            transcriptPre.innerHTML = transcriptSpanish;
        }
    }
    showTranscript("spanish");

    // Function to jump the audio player to a specified time.
    function jumpToTime(seconds) {
        var audio = document.getElementById("audioPlayer");
        audio.currentTime = seconds;
        audio.play();
    }

    // Function to jump to a section: scroll that section into view, update TOC and image.
    function jumpToSection(sectionId, seconds) {
        jumpToTime(seconds);
        var anchor = document.getElementById(sectionId);
        if (anchor) {
            anchor.scrollIntoView({ behavior: "smooth", block: "start" });
        }
        currentSectionId = sectionId;
        updateToc();
        updateImageForSection(currentSectionId);
    }

    // Attach a scroll event listener to the transcript (right column) to update the TOC
    // based on the section whose anchor is closest to the top.
    var scrollDiv = document.getElementById("right-column");
    if (scrollDiv) {
        scrollDiv.addEventListener("scroll", function() {
            var containerRect = scrollDiv.getBoundingClientRect();
            var closestSectionId = "";
            var minDiff = Infinity;
            mainPoints.forEach(function(point) {
                var anchor = document.getElementById(point.id);
                if (anchor) {
                    var diff = Math.abs(anchor.getBoundingClientRect().top - containerRect.top);
                    if (diff < minDiff) {
                        minDiff = diff;
                        closestSectionId = point.id;
                    }
                }
            });
            if (closestSectionId && closestSectionId !== currentSectionId) {
                currentSectionId = closestSectionId;
                updateToc();
                updateImageForSection(currentSectionId);
            }
        });
    }
    </script>
</body>
</html>
"""
    with open(config["output_file"], "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML file generated: {config['output_file']}")

# === Generate Pages for All Interviews ===
for key, conf in config_dict.items():
    generate_page_with_nav(conf, main_points_dict[conf["page_id"]], config_dict)

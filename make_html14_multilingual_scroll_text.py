#!/usr/bin/env python3
import re
import sys
import json
import os

# --- Load JSON Data from External Files ---
with open("config.json", "r", encoding="utf-8") as f:
    config_dict = json.load(f)

# Load main points (English) from separate JSON files in the main_points folder.
# We will also attempt to load a Spanish version (suffix "_es.json") for each page.
main_points_dict = {}
main_points_es_dict = {}
for key, conf in config_dict.items():
    page_id = conf["page_id"]

    # English main points
    main_points_path = os.path.join("main_points", page_id + ".json")
    try:
        with open(main_points_path, "r", encoding="utf-8") as f:
            main_points_dict[page_id] = json.load(f)
    except FileNotFoundError:
        main_points_dict[page_id] = []

    # Spanish main points (suffix "_es.json")
    main_points_es_path = os.path.join("main_points", page_id + "_es.json")
    try:
        with open(main_points_es_path, "r", encoding="utf-8") as f:
            main_points_es_dict[page_id] = json.load(f)
    except FileNotFoundError:
        main_points_es_dict[page_id] = []

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
            while (
                mp_index < len(main_points_list)
                and current_time is not None
                and current_time >= main_points_list[mp_index]["start_time"]
            ):
                anchor_html = f'<div id="{main_points_list[mp_index]["id"]}" class="section-anchor"></div>\n'
                output_lines.append(anchor_html)
                mp_index += 1
        output_lines.append(line)
    # If there are any anchors left (points with no matching timestamps in text), append them at the end
    while mp_index < len(main_points_list):
        anchor_html = f'<div id="{main_points_list[mp_index]["id"]}" class="section-anchor"></div>\n'
        output_lines.append(anchor_html)
        mp_index += 1

    processed = "".join(output_lines)

    # Wrap speaker names (for styling)
    processed = re.sub(
        r"^(Rosita)", r'<span class="speaker-rosita">\1</span>',
        processed, flags=re.MULTILINE
    )
    processed = re.sub(
        r"^(Lali)", r'<span class="speaker-lali">\1</span>',
        processed, flags=re.MULTILINE
    )
    processed = re.sub(
        r"^(Ruby)", r'<span class="speaker-ruby">\1</span>',
        processed, flags=re.MULTILINE
    )
    processed = re.sub(
        r"^(Jaime)", r'<span class="speaker-jaime">\1</span>',
        processed, flags=re.MULTILINE
    )
    processed = re.sub(
        r"^(Marita)", r'<span class="speaker-marita">\1</span>',
        processed, flags=re.MULTILINE
    )
    processed = re.sub(
        r"^(Eric)", r'<span class="speaker-eric">\1</span>',
        processed, flags=re.MULTILINE
    )

    # Make timestamp-only lines clickable
    def timestamp_link(match):
        ts = match.group(1)
        seconds = timestamp_to_seconds(ts)
        return (
            f'<a href="#" class="timestamp" '
            f'onclick="jumpToTime({seconds}); return false;">{ts}</a>'
        )

    processed = re.sub(
        r"^(\d+:\d{2}:\d{2})$",
        timestamp_link,
        processed,
        flags=re.MULTILINE
    )

    return processed

# === Function to Generate a Single HTML Page with Navigation, Image, TOC, Transcript Toggle, and a Floating Gallery ===
def generate_page_with_nav(config, main_points_list_en, main_points_list_es, all_configs):
    page_id = config["page_id"]

    # === Process transcripts (English and Spanish) ===
    if "spanish_transcript_file" in config:
        processed_sp = process_transcript(
            config["spanish_transcript_file"], main_points_list_es
        )
    else:
        processed_sp = ""

    if "transcript_file" in config:
        processed_en = process_transcript(
            config["transcript_file"], main_points_list_en
        )
    else:
        processed_en = ""

    # Only show the transcript-toggle buttons if both English and Spanish exist
    has_en = bool(processed_en.strip())
    has_sp = bool(processed_sp.strip())
    show_transcript_toggle = has_en and has_sp

    # === Build the navigation bar ===
    nav_links = []
    for key, conf in all_configs.items():
        if conf["page_id"] == config["page_id"]:
            nav_links.append(
                f'<a href="{conf["output_file"]}" class="nav-link selected">'
                f'{conf["page_title"]}</a>'
            )
        else:
            nav_links.append(
                f'<a href="{conf["output_file"]}" class="nav-link">'
                f'{conf["page_title"]}</a>'
            )
    nav_block = "".join(nav_links)

    # === JSON for images, TOC, and transcript ===
    section_images_json = json.dumps(image_dict)
    main_en_json = json.dumps(main_points_list_en)
    main_es_json = json.dumps(main_points_list_es)
    transcript_en_json = json.dumps(processed_en)
    transcript_sp_json = json.dumps(processed_sp)

    # === Build HTML content using only f-strings ===
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
  gap: 12px;
  height: calc(90vh - 130px);
}}

/* Left Column: Buttons, Image Subtitle, Image, TOC, and TOC Toggle */
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
#buttons {{
  text-align: center;
  margin: 2px 0;
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
#image-container {{
  height: 55%;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  padding-bottom: 2px;
}}
#image-container img {{
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}}

/* TOC Toggle Buttons */
#toc-toggle {{
  text-align: center;
  margin: 5px 0;
}}
#toc-toggle button {{
  margin: 0 5px;
  padding: 6px 12px;
  background-color: #007acc;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}}
#toc-toggle button:hover {{
  background-color: #005fa3;
}}

/* TOC Containers */
#toc-title {{
  font-size: 0.7em;
  text-align: center;
  border-top: 1px solid #e0e0e0;
}}
.toc-container {{
  height: 34%;
  overflow-y: auto;
  background-color: #fafafa;
  border-top: 1px solid #e0e0e0;
  padding: 10px;
}}
.toc-container h2 {{
  margin: 0 0 10px 0;
  font-size: 1.2em;
  color: #007acc;
}}
.toc-container ul {{
  list-style: none;
  padding: 0;
  margin: 0;
}}
.toc-container li {{
  margin-bottom: 8px;
}}
.toc-container a {{
  text-decoration: none;
  color: #555;
  transition: color 0.3s;
}}
.toc-container a:hover {{
  color: #007acc;
}}

/* Right Column: Transcript (toggle shown conditionally) */
#right-column {{
  font-family: 'Roboto';
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
.speaker-jaime {{
  color: #ff7a00;
  font-weight: bold;
}}
.speaker-marita {{
  color: #0077ab;
  font-weight: bold;
}}
.speaker-rosita {{
  color: #007acc;
  font-weight: bold;
}}
.speaker-eric {{
  color: #228b22;
  font-weight: bold;
}}
.speaker-ruby {{
  color: #998b88;
  font-weight: bold;
}}
.speaker-lali {{
  color: #ff0000;
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

/* Floating Gallery Popup */
#gallery-popup {{
  display: none;
  position: fixed;
  top: 10%;
  left: 10%;
  width: 80%;
  height: 80%;
  background-color: #fff;
  border: 2px solid #007acc;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  padding: 10px;
  overflow: hidden;
}}
#gallery-close {{
  position: absolute;
  top: 5px;
  right: 10px;
  font-size: 1.5em;
  cursor: pointer;
  color: #007acc;
}}
#gallery-close:hover {{
  color: darkgray;
}}
#gallery-content {{
  display: flex;
  height: 100%;
}}
#gallery-full-pane {{
  flex: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #e0e0e0;
  padding: 10px;
}}
#gallery-full-pane img {{
  max-width: 100%;
  max-height: 70%;
  object-fit: contain;
}}
#gallery-full-pane #gallery-full-title {{
  margin-top: 5px;
  font-size: 1.2em;
  font-weight: bold;
}}
#gallery-full-pane #gallery-full-subtitle {{
  margin-top: 3px;
  font-size: 0.9em;
  color: #555;
}}
#gallery-thumbs-pane {{
  flex: 1;
  overflow-y: auto;
  padding: 5px;
}}
#gallery-thumbs-pane img {{
  width: 80px;
  height: 60px;
  object-fit: cover;
  margin: 3px 0;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border 0.3s;
}}
#gallery-thumbs-pane img.selected {{
  border: 2px solid #007acc;
}}
#acknowledgements {{
  font-size: 0.6em;
  padding-bottom: 2px;
}}
    </style>
    <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">
</head>
<body>
    <span style="font-size: 12pt;"><u><b>Recuerdos y Cuentos de la Familia:</b> <span>{config["page_title"]}</span></u></span>
    
    <div style="font-size: 0.8em; padding-top: 0px;"><i>
<div style="font-size: 10pt;"><b>Navégue los entrevistas a través de clicks en "Resumen de Secciones" o en las indicaciones de tiempo en la sección con las transcripciónes. Haga click en "Galeria" para ver todas las fotos.</b>
<div id="acknowledgements">
<div>* Muchas gracias a todos los participantes, entre cuales algunos ya no están con nosotros. Espero que las grabaciones sirvan como bonitos recuerdos, preservando a personalidades y cuentos únicos. </div>

<div>** He agregado musica en ciertas partes de acuerdo a los deseos de los entrevistados, o para cubrir problemas técnicos. </i></div>
<div>*** Por favor mandenme fotos, me encantaria poder agregar mas información y imágenes a esto sito.</div>
</div>
</div>
    <!-- Navigation Block -->
    <div id="nav">{nav_block}</div>
    <!-- Audio Player -->
    <audio id="audioPlayer" controls>
        <source src="{config["audio_file"]}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <!-- Main Container with Two Columns -->
    <div id="main-container">
        <!-- Left Column: Image Controls, Image, TOC Toggle, TOC, and Gallery Link -->
        <div id="left-column">
            <div id="image-subtitle">Ester. Ester as a young woman (1926?)</div>
            <div id="image-container">
                <img id="current-image" src="images/ester_as_young_woman.jpg" alt="Image">
            </div>
            <div id="gallery-link" style="text-align:center; margin:5px;">
                <button onclick="openGallery()">Galeria</button>
            </div>

            <!-- TOC Toggle Buttons -->
            <div id="toc-title" style="padding: 2px;">
                <span id="toc-toggle"><button style="margin: 5px;" onclick="showToc('spanish')">Español</button></span> 
		<span style="font-size: 12px; padding-top: 0px;"><b>Resumen de Secciones</b></span>
                <span id="toc-toggle"><button style="margin: 5px;" onclick="showToc('english')">English</button></span>
            </div>

            <!-- Spanish TOC (visible by default) -->
            <div id="toc-es" class="toc-container">
                <ul>
{"".join(f'                    <li><a href="#{mp["id"]}" id="link-{mp["id"]}-es" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n' for mp in main_points_list_es)}
                </ul>
            </div>

            <!-- English TOC (hidden by default) -->
            <div id="toc-en" class="toc-container" style="display:none;">
                <ul>
{"".join(f'                    <li><a href="#{mp["id"]}" id="link-{mp["id"]}-en" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n' for mp in main_points_list_en)}
                </ul>
            </div>
        </div>

        <!-- Right Column: Transcript (toggle shown only if both languages exist) -->
        <div id="right-column">
            {f"""<div id="transcript-toggle">
                <button onclick="showTranscript('spanish')">Español</button>
                <button onclick="showTranscript('english')">English</button>
            </div>""" if show_transcript_toggle else ""}
            <div id="transcript-content">
                <pre id="transcript-pre">
{processed_sp or processed_en}
                </pre>
            </div>
        </div>
    </div>

    <!-- Floating Gallery Popup -->
    <div id="gallery-popup">
        <span id="gallery-close" onclick="closeGallery()">×</span>
        <div id="gallery-content">
            <div id="gallery-full-pane">
                <img id="gallery-full" src="" alt="Full Image">
                <div id="gallery-full-title"></div>
                <div id="gallery-full-subtitle"></div>
            </div>
            <div id="gallery-thumbs-pane">
            </div>
        </div>
    </div>

    <script>
        // Global arrays/objects
        var sectionImages = {section_images_json};
        var mainPointsEn = {main_en_json};
        var mainPointsEs = {main_es_json};

        // Update TOC: highlight current section in whichever TOC is visible
        function updateToc() {{
            var currentLang = document.getElementById("toc-es").style.display === "none" ? "en" : "es";
            var points = (currentLang === "en") ? mainPointsEn : mainPointsEs;
            var prefix = (currentLang === "en") ? "-en" : "-es";
            var containerId = (currentLang === "en") ? "toc-en" : "toc-es";
            var tocContainer = document.getElementById(containerId);

            points.forEach(function(pt) {{
                var entry = document.getElementById("link-" + pt.id + prefix);
                if (entry) {{
                    if (pt.id === currentSectionId) {{
                        entry.style.color = "black";
                        var containerRect = tocContainer.getBoundingClientRect();
                        var entryRect = entry.getBoundingClientRect();
                        if (entryRect.top < containerRect.top || entryRect.bottom > containerRect.bottom) {{
                            entry.scrollIntoView({{ behavior: "smooth", block: "nearest" }});
                        }}
                    }} else {{
                        entry.style.color = "gray";
                    }}
                }}
            }});
        }}

        // Helper: update the gallery-full image
        function updateGalleryImage(sectionId) {{
            var pointEs = mainPointsEs.find(function(pt) {{ return pt.id === sectionId; }});
            var pointEn = mainPointsEn.find(function(pt) {{ return pt.id === sectionId; }});
            var point = pointEs || pointEn;
            if (point && point.hasOwnProperty("image") && sectionImages.hasOwnProperty(point.image)) {{
                document.getElementById("gallery-full").src = sectionImages[point.image].src;
                var fullText = sectionImages[point.image].textContent;
                var titleText = fullText.split(".")[0];
                document.getElementById("gallery-full-title").textContent = titleText;
                document.getElementById("gallery-full-subtitle").textContent = fullText;
            }}
        }}

        // Next/Prev image on main page
        function prevImage() {{
            var combined = mainPointsEn.concat(mainPointsEs);
            var seen = new Set();
            var merged = [];
            combined.forEach(function(pt) {{
                if (!seen.has(pt.id)) {{
                    seen.add(pt.id);
                    merged.push(pt);
                }}
            }});
            for (var i = merged.length - 1; i >= 0; i--) {{
                if (merged[i].hasOwnProperty("image") && merged[i].id < currentSectionId) {{
                    currentSectionId = merged[i].id;
                    updateImageForSection(currentSectionId);
                    updateToc();
                    return;
                }}
            }}
        }}

        function nextImage() {{
            var combined = mainPointsEn.concat(mainPointsEs);
            var seen = new Set();
            var merged = [];
            combined.forEach(function(pt) {{
                if (!seen.has(pt.id)) {{
                    seen.add(pt.id);
                    merged.push(pt);
                }}
            }});
            for (var i = 0; i < merged.length; i++) {{
                if (merged[i].hasOwnProperty("image") && merged[i].id > currentSectionId) {{
                    currentSectionId = merged[i].id;
                    updateImageForSection(currentSectionId);
                    updateToc();
                    return;
                }}
            }}
        }}

        function updateImageForSection(sectionId) {{
            var pointEs = mainPointsEs.find(function(pt) {{ return pt.id === sectionId; }});
            var pointEn = mainPointsEn.find(function(pt) {{ return pt.id === sectionId; }});
            var point = pointEs || pointEn;
            if (point && point.hasOwnProperty("image") && sectionImages.hasOwnProperty(point.image)) {{
                document.getElementById("current-image").src = sectionImages[point.image].src;
                document.getElementById("image-subtitle").textContent = sectionImages[point.image].textContent;
            }}
        }}

        // TOC toggle logic
        function showToc(lang) {{
            if (lang === "english") {{
                document.getElementById("toc-en").style.display = "block";
                document.getElementById("toc-es").style.display = "none";
            }} else {{
                document.getElementById("toc-en").style.display = "none";
                document.getElementById("toc-es").style.display = "block";
            }}
            updateToc();
        }}

        // Transcript toggle logic (only if both exist)
        var transcriptPre = document.getElementById("transcript-pre");
        var transcriptEnglish = {transcript_en_json};
        var transcriptSpanish = {transcript_sp_json};
        function showTranscript(lang) {{
            transcriptPre.innerHTML = (lang === "english") ? transcriptEnglish : transcriptSpanish;
        }}
        {"/* Initialize with Spanish transcript */ showTranscript('spanish');" if show_transcript_toggle else ""}

        // Audio jump function
        function jumpToTime(seconds) {{
            var audio = document.getElementById("audioPlayer");
            audio.currentTime = seconds;
            audio.play();
        }}

        // Function to jump to a section
        function jumpToSection(sectionId, seconds) {{
            jumpToTime(seconds);
            var anchor = document.getElementById(sectionId);
            if (anchor) {{
                anchor.scrollIntoView({{ behavior: "smooth", block: "start" }});
            }}
            currentSectionId = sectionId;
            updateToc();
            updateImageForSection(currentSectionId);
        }}

        // Update TOC & image based on scroll position in transcript
        var scrollDiv = document.getElementById("right-column");
        if (scrollDiv) {{
            scrollDiv.addEventListener("scroll", function() {{
                var containerRect = scrollDiv.getBoundingClientRect();
                var combined = mainPointsEn.concat(mainPointsEs);
                var closestSectionId = "";
                var minDiff = Infinity;
                combined.forEach(function(point) {{
                    var anchor = document.getElementById(point.id);
                    if (anchor) {{
                        var diff = Math.abs(anchor.getBoundingClientRect().top - containerRect.top);
                        if (diff < minDiff) {{
                            minDiff = diff;
                            closestSectionId = point.id;
                        }}
                    }}
                }});
                if (closestSectionId && closestSectionId !== currentSectionId) {{
                    currentSectionId = closestSectionId;
                    updateToc();
                    updateImageForSection(currentSectionId);
                }}
            }});
        }}

        // Current section starts at the first Spanish section if available, otherwise English
        var currentSectionId = (mainPointsEs.length > 0) ? mainPointsEs[0].id
                                : (mainPointsEn.length > 0) ? mainPointsEn[0].id
                                : "";
        // Initialize TOC & image
        showToc("spanish");
        updateImageForSection(currentSectionId);

        // Open gallery popup
        function openGallery() {{
            document.getElementById("gallery-popup").style.display = "block";
            updateGalleryImage(currentSectionId);
            populateGalleryThumbnails();
        }}

        // Close gallery popup
        function closeGallery() {{
            document.getElementById("gallery-popup").style.display = "none";
        }}

        // Populate gallery thumbnails
        function populateGalleryThumbnails() {{
            var thumbsPane = document.getElementById("gallery-thumbs-pane");
            thumbsPane.innerHTML = "";
            Object.keys(sectionImages).forEach(function(key) {{
                var imgObj = sectionImages[key];
                var thumb = document.createElement("img");
                thumb.src = imgObj.src;
                thumb.onclick = function() {{
                    document.getElementById("gallery-full").src = imgObj.src;
                    document.getElementById("gallery-full-title").textContent = imgObj.textContent.split(".")[0];
                    document.getElementById("gallery-full-subtitle").textContent = imgObj.textContent;
                    var allThumbs = thumbsPane.getElementsByTagName("img");
                    for (var i = 0; i < allThumbs.length; i++) {{
                        allThumbs[i].classList.remove("selected");
                    }}
                    thumb.classList.add("selected");
                }};
                var currentPoint = mainPointsEs.find(function(pt) {{
                    return pt.hasOwnProperty("image") && pt.image === key;
                }}) || mainPointsEn.find(function(pt) {{
                    return pt.hasOwnProperty("image") && pt.image === key;
                }});
                if (currentPoint && currentPoint.id === currentSectionId) {{
                    thumb.classList.add("selected");
                }}
                thumbsPane.appendChild(thumb);
            }});
        }}
    </script>
</body>
</html>
"""

    with open(config["output_file"], "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file generated: {config['output_file']}")


# === Generate Pages for All Interviews ===
for key, conf in config_dict.items():
    pid = conf["page_id"]
    generate_page_with_nav(
        conf,
        main_points_dict.get(pid, []),
        main_points_es_dict.get(pid, []),
        config_dict
    )

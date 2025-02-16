#!/usr/bin/env python3
import re
import sys
import json

# === Image dict ===
image_dict = {
    "young_ester": {
        "src": "images/ester_as_young_woman.png",
        "subtitle": "Ester as a young woman"
    },
    "boarding_lisbon": {
        "src": "images/boarding_in_lisbon.png",
        "subtitle": "Waiting to board in Lisbon"
    }
}

# === Configuration Dictionary for All Interviews ===
# Each key is a unique page ID. The inner dictionary contains:
#   - page_id: identifier (should match the key)
#   - transcript_file: path to the English transcript file
#   - spanish_transcript_file (optional): path to the Spanish transcript file (if available)
#   - audio_file: path to the audio file
#   - output_file: name for the generated HTML file
#   - page_title: title for the page (used in the navigation menu)
config_dict = {
    "RositaInterview4_29_20-11_17_23": {
        "page_id": "RositaInterview4_29_20-11_17_23",
        "transcript_file": "transcripts/RositaInterview4_29_20-11_17_23_English.txt",
        "spanish_transcript_file": "transcripts/RositaInterview4_29_20-11_17_23.txt",
        "audio_file": "audio/RositaInterview4_29_20-11_17_23.mp3",
        "output_file": "RositaInterview4_29_20-11_17_23.html",
        "page_title": "Rosita Interview - 4/29/20 (Interview 1)"
    },
    "RositaInterview4_11_20-4_11_20": {
        "page_id": "RositaInterview4_11_20-4_11_20",
        "transcript_file": "transcripts/RositaInterview4_11_20-4_11_20_English.txt",
        "spanish_transcript_file": "transcripts/RositaInterview4_11_20-4_11_20.txt",
        "audio_file": "audio/RositaInterview4_11_20-4_11_20.mp3",
        "output_file": "RositaInterview4_11_20-4_11_20.html",
        "page_title": "Rosita Interview - 4/11/20 (Interview 2)"
    },
    "MaritaInterview5_4_20": {
        "page_id": "MaritaInterview5_4_20",
        "transcript_file": "transcripts/MaritaInterview5_4_20_English.txt",
        "spanish_transcript_file": "transcripts/MaritaInterview5_4_20.txt",
        "audio_file": "audio/MaritaInterview5_4_20.mp3",
        "output_file": "MaritaInterview5_4_20.html",
        "page_title": "Marita Interview - 5/4/20 (first 30 min)"
    }
}

# === Define the Main Points for Each Interview ===
# main_points_dict maps a page_id to a list of section dictionaries.
# Each section dict contains:
#   - id: a unique anchor identifier
#   - title: a detailed descriptive title for that section
#   - subtitle: an optional subtitle or quotation from that section (for added detail)
#   - start_time: approximate start time (in seconds)
#   - display_time: the timestamp string for display
#   - image (optional): a key referring to an entry in image_dict
main_points_dict = {
    "MaritaInterview5_4_20": [
        {
            "id": "section-1",
            "title": "Start",
            "start_time": 0,
            "display_time": "0:00:00",
            "image": "young_ester"
        }
        # Add additional sections as needed…
    ],
    "RositaInterview4_29_20-11_17_23": [
        {
            "id": "section-1",
            "title": "WWII Outbreak and Early Reflections on the War",
            "start_time": 0,
            "display_time": "0:00:00",
            "image": "young_ester"

        },
        {
            "id": "section-2",
            "title": "Mina and Brana's Journey from Orhei/Orgeyev to Lisbon",
            "start_time": 19,
            "display_time": "0:00:19",
            "image": "boarding_lisbon"
        },
        {
            "id": "section-3",
            "title": "A Childhood Memory: The Unusual Bathing Incident",
            "start_time": 122,
            "display_time": "0:02:02"
        },
        {
            "id": "section-4",
            "title": "Family Background: León’s Parents and the Vicuña Mackenna Building",
            "start_time": 253,
            "display_time": "0:04:13"
        },
        {
            "id": "section-5",
            "title": "Religious Practices and Abram’s Devotion in the Family",
            "start_time": 370,
            "display_time": "0:06:10"
        },
        {
            "id": "section-7",
            "title": "Ester's Second Marriage",
            "start_time": 464,
            "display_time": "0:07:44"
        },
        {
            "id": "section-8",
            "title": "Descriptions of Ester's Personality",
            "start_time": 531,
            "display_time": "0:08:51"
        },
        {
            "id": "section-9",
            "title": "The Importance of Education in Ester's Family",
            "start_time": 675,
            "display_time": "0:11:15"
        },
        {
            "id": "section-10",
            "title": "International Connections and Memories of David Braylovsky",
            "start_time": 961,
            "display_time": "0:16:01"
        },
        {
            "id": "section-11",
            "title": "Rosita's Memories of Her Father",
            "start_time": 1265,
            "display_time": "0:21:05"
        },
        {
            "id": "section-12",
            "title": "The Marble House, Earthquake, and Family Tragedy",
            "start_time": 1341,
            "display_time": "0:22:21"
        },
        {
            "id": "section-13",
            "title": "School Memories and Early Friendships in Concepción",
            "start_time": 1500,
            "display_time": "0:25:00"
        },
        {
            "id": "section-14",
            "title": "Language Challenges and Pursuing Further Education",
            "start_time": 1578,
            "display_time": "0:26:18"
        },
        {
            "id": "section-15",
            "title": "Natalio Berman, Communist Congressman and Friend of José's",
            "start_time": 1635,
            "display_time": "0:27:15"
        },
        {
            "id": "section-16",
            "title": "Observations on the Early Pandemic",
            "start_time": 1860,
            "display_time": "0:31:00"
        }
    ],
    "RositaInterview4_11_20-4_11_20": [
        {
            "id": "section-1",
            "title": "Arrival in Santiago and Initial Impressions",
            "subtitle": "We arrived in Santiago, my mother, my brother and I, in January of 1939.",
            "start_time": 0,
            "display_time": "0:00:00"
        },
        {
            "id": "section-2",
            "title": "Immediate Post‐Earthquake Reaction",
            "subtitle": "Eric asks, 'Right after the earthquake?' and Rosita replies, 'After the earthquake.'",
            "start_time": 9,
            "display_time": "0:00:09"
        },
        {
            "id": "section-3",
            "title": "Ship Arrival and Family Reunion",
            "subtitle": "Rosita explains that the ship arrived carrying her mother's two sisters, her uncle Fabel, and Chelis’s family.",
            "start_time": 13,
            "display_time": "0:00:13"
        },
        {
            "id": "section-4",
            "title": "Family Gatherings and Economic Conditions",
            "subtitle": "Family meetings were frequent and everyone was poorer (no cars).",
            "start_time": 52,
            "display_time": "0:00:52"
        },
        {
            "id": "section-5",
            "title": "Neighborhood Living in Santiago",
            "subtitle": "Everyone lived 6–8 blocks apart; no family had a car.",
            "start_time": 85,
            "display_time": "0:01:25"
        },
        {
            "id": "section-6",
            "title": "Traumatic Transfer from Concepción to Santiago",
            "subtitle": "Rosita mentions the traumatic transfer from Concepción to Santiago following the earthquake.",
            "start_time": 125,
            "display_time": "0:02:05"
        },
        {
            "id": "section-7",
            "title": "Family Details: The VINE and Jaime Motlis",
            "subtitle": "She refers to a cousin (son of 'the VINE') and to Jaime Motlis, a government doctor.",
            "start_time": 155,
            "display_time": "0:02:35"
        },
        {
            "id": "section-8",
            "title": "Train Transportation Across Chile",
            "subtitle": "Travel was mostly by train due to few cars and paved roads.",
            "start_time": 209,
            "display_time": "0:03:29"
        },
        {
            "id": "section-9",
            "title": "Living Arrangements: Big Houses and Mixed Emotions",
            "subtitle": "Rosita recounts living in large houses with extended family, with mixed feelings.",
            "start_time": 246,
            "display_time": "0:04:06"
        },
        {
            "id": "section-10",
            "title": "Newcomers (‘Grines’) and Community Impressions",
            "subtitle": "She explains that the 'grines' (gringos) fresh off the boat became a local talking point.",
            "start_time": 330,
            "display_time": "0:05:30"
        },
        {
            "id": "section-11",
            "title": "Long-Term Childhood Memories",
            "subtitle": "Rosita recalls Aunt Feige and that she saw these people frequently until her marriage.",
            "start_time": 406,
            "display_time": "0:06:46"
        },
        {
            "id": "section-12",
            "title": "Earthquake Memories and the Pool House ‘Penco’",
            "subtitle": "She remembers the January earthquake and sleeping in tents at a pool house called 'Penco.'",
            "start_time": 440,
            "display_time": "0:07:20"
        },
        {
            "id": "section-13",
            "title": "Reconstruction and Adobe Collapse",
            "subtitle": "Rosita describes cracks, ditches, and wonders about a tsunami in Pucon; she references the 1939 earthquake.",
            "start_time": 501,
            "display_time": "0:08:21"
        },
        {
            "id": "section-14",
            "title": "First House in Santiago on Agustinas",
            "subtitle": "She recalls the first house on Agustinas (which is still standing).",
            "start_time": 588,
            "display_time": "0:09:48"
        },
        {
            "id": "section-15",
            "title": "Central Santiago: Plaza Italia and Neighborhood Streets",
            "subtitle": "A discussion about central Santiago (Plaza Italia, Ahumada, Plaza de Armas) and the walkability of the area.",
            "start_time": 630,
            "display_time": "0:10:30"
        },
        {
            "id": "section-16",
            "title": "Cultural Landmarks: Synagogue and Rosh Hashanah",
            "subtitle": "She mentions a synagogue that was sold and installed in a church and recalls a Rosh Hashanah ceremony.",
            "start_time": 728,
            "display_time": "0:12:08"
        },
        {
            "id": "section-17",
            "title": "Mother’s Dramatic Early Life and Arrival in Chile",
            "subtitle": "Rosita recounts her mother's dramatic life, arriving in Chile in 1928 and being born in 1929.",
            "start_time": 783,
            "display_time": "0:13:03"
        },
        {
            "id": "section-18",
            "title": "Mother’s Journey to Puerto Montt and Meeting on the Boat",
            "subtitle": "She recounts how her mother left for Puerto Montt (with help from Uncle Aarón) and met Jose Greider on the boat.",
            "start_time": 865,
            "display_time": "0:14:25"
        },
        {
            "id": "section-19",
            "title": "Factory Work and Early Relocation in Concepción",
            "subtitle": "Rosita describes working in a factory in Concepción, living behind it, and later moving to a nicer house.",
            "start_time": 906,
            "display_time": "0:15:06"
        },
        {
            "id": "section-20",
            "title": "Family Economic Progress and Real Estate Investments",
            "subtitle": "She explains how the family moved from Plaza Italia and invested in real estate (mentioning 'Lockshins').",
            "start_time": 964,
            "display_time": "0:16:04"
        },
        {
            "id": "section-21",
            "title": "Mother’s Business, Divorce, and Restarted Ventures",
            "subtitle": "After being widowed, her mother set up a new fabric factory and later tried to restart a workshop after divorce.",
            "start_time": 1034,
            "display_time": "0:17:14"
        },
        {
            "id": "section-22",
            "title": "Real Estate and Investment Challenges",
            "subtitle": "More details on investments, low property sale values, and financial challenges.",
            "start_time": 1123,
            "display_time": "0:18:43"
        },
        {
            "id": "section-23",
            "title": "Mother’s Marriage to Poniatyk and Polish Connection",
            "subtitle": "Rosita recounts her mother's marriage to a Polish man named Poniatyk.",
            "start_time": 1179,
            "display_time": "0:19:39"
        },
        {
            "id": "section-24",
            "title": "Factory Sale and Financial Legacy",
            "subtitle": "She explains how her mother sold her factory to help her husband and the resulting financial impact.",
            "start_time": 1336,
            "display_time": "0:22:16"
        },
        {
            "id": "section-25",
            "title": "Investments, the Dollar Crisis, and ‘Lockshins’",
            "subtitle": "Discussion of skyrocketing dollars, property investments, and the term 'Loxxion' for dollars.",
            "start_time": 1380,
            "display_time": "0:23:49"
        },
        {
            "id": "section-26",
            "title": "Mother’s Independence and Business Legacy",
            "subtitle": "Reflections on how her mother managed to start a business on her own despite challenges.",
            "start_time": 1576,
            "display_time": "0:26:16"
        },
        {
            "id": "section-27",
            "title": "Language and Cultural Skills",
            "subtitle": "Rosita discusses her mother's struggles with Spanish and her abilities in Russian, Yiddish, and German.",
            "start_time": 1637,
            "display_time": "0:27:17"
        },
        {
            "id": "section-28",
            "title": "Clothing Business and Family Connections",
            "subtitle": "Details about the clothing business, mentioning Uli Chas and the Lithuanian background of Goyo’s father.",
            "start_time": 1691,
            "display_time": "0:28:11"
        },
        {
            "id": "section-29",
            "title": "Family Reunion and Ongoing Reminiscences",
            "subtitle": "Brief recollections of continuing family interactions and memories.",
            "start_time": 1751,
            "display_time": "0:29:11"
        },
        {
            "id": "section-30",
            "title": "Discussion on Divorce and Financial Decisions",
            "subtitle": "A narrative regarding her mother’s divorce, the sale of the factory, and financial decisions.",
            "start_time": 1774,
            "display_time": "0:29:34"
        },
        {
            "id": "section-31",
            "title": "Economic Crisis: Skyrocketing Dollar and Property Sales",
            "subtitle": "Explanation of how the dollar skyrocketed and properties were sold for very little.",
            "start_time": 1860,
            "display_time": "0:31:00"
        },
        {
            "id": "section-32",
            "title": "Revisiting the Family Business and Investment Legacy",
            "subtitle": "Continued discussion on family business and investments.",
            "start_time": 1896,
            "display_time": "0:31:36"
        },
        {
            "id": "section-33",
            "title": "Adoption and Extended Family Dynamics",
            "subtitle": "Talk about adopted children and various cousin relationships within the family.",
            "start_time": 1985,
            "display_time": "0:33:05"
        },
        {
            "id": "section-34",
            "title": "Immigration History and European Roots",
            "subtitle": "Discussion of her mother's origins, life in Russia, and the immigrant background.",
            "start_time": 2042,
            "display_time": "0:34:02"
        },
        {
            "id": "section-35",
            "title": "Later Reflections and Future Research on Family History",
            "subtitle": "Final remarks on writing a book about immigration to South America and further research.",
            "start_time": 2156,
            "display_time": "0:35:56"
        }
    ]
}

# === Regular Expression for Timestamp Lines ===
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

# === Function to Generate a Single HTML Page with Navigation, Transcripts, and an Image Container ===
def generate_page_with_nav(config, main_points_list, all_configs):
    # Process transcripts. Use English transcript if available; otherwise default to Spanish.
    if "transcript_file" in config:
        processed_en = process_transcript(config["transcript_file"], main_points_list)
    elif "spanish_transcript_file" in config:
        processed_en = process_transcript(config["spanish_transcript_file"], main_points_list)
    else:
        processed_en = ""
    processed_es = ""
    if "spanish_transcript_file" in config:
        processed_es = process_transcript(config["spanish_transcript_file"], main_points_list)
    
    # Build navigation links for other pages.
    nav_links = []
    for key, conf in all_configs.items():
        if conf["page_id"] != config["page_id"]:
            nav_links.append(f'<a href="{conf["output_file"]}" style="font-size:1.2em; color:darkblue; text-decoration:none;">{conf["page_title"]}</a>')
    nav_block = " | ".join(nav_links)
    
    # Build a JSON string from image_dict.
    section_images_json = json.dumps(image_dict)
    
    # Build the HTML content.
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{config["page_title"]}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        /* Navigation styling */
        #nav {{
            margin-bottom: 20px;
        }}
        /* Left Column: Contains Image and TOC */
        #left-col {{
            display: flex;
            flex-direction: column;
            height: calc(100vh - 100px);
            flex: 1;
        }}
        /* Image Container: Upper half of left-col */
        #image-container {{
            position: relative;
            height: 50%;
            text-align: center;
            border: 1px solid #ccc;
            padding: 10px;
            overflow: hidden;
        }}
        #image-container img {{
            max-height: 100%;
            max-width: 100%;
            object-fit: contain;
        }}
        /* Arrow button styling */
        #prev-image, #next-image {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0);
            border: none;
            font-size: 2em;
            cursor: pointer;
            z-index: 10;
            padding: 5px;
        }}
        #prev-image {{
            left: 10px;
        }}

        #next-image {{
            right: 10px;
        }}

	/* When the user hovers over the arrow, change the arrow color to gray */
	#prev-image:hover, #next-image:hover {{
 	   color: gray;
	}}

	/* When the arrow is actively clicked, change it to dark gray */
	#prev-image:active, #next-image:active {{
	    color: darkgray;
	}}
	
        /* Table of Contents: Lower half of left-col */
        #toc {{
            height: 50%;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 10px;
            overflow-y: auto;
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
            color: darkgray;
        }}
        #toc a:hover {{
            text-decoration: underline;
        }}
        /* Transcripts wrapper styling (Right Column) */
        #transcripts-wrapper {{
            flex: 2;
            display: flex;
            gap: 20px;
            border: 1px solid #ccc;
            height: calc(100vh - 100px);
            overflow: hidden;
            padding: 10px;
        }}
        /* Individual transcript containers */
        .transcript-column {{
            flex: 1;
            overflow-y: auto;
        }}
        #transcript-title-en, #transcript-title-es {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        /* Anchor div styling */
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
        /* Timestamp styling */
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
    <h1>{config["page_title"]}</h1>
    <!-- Navigation Block -->
    <div id="nav">
        {nav_block}
    </div>
    <!-- Audio Player -->
    <audio id="audioPlayer" controls>
        <source src="{config["audio_file"]}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <!-- Left Column: Image Container and TOC -->
    <div id="container" style="display: flex; gap: 20px;">
        <div id="left-col">
            <!-- Image Container (upper half) -->
            <div id="image-container">
                <button id="prev-image" onclick="prevImage()">&#9664;</button>
                <img id="current-image" src="" alt="Image">
                <button id="next-image" onclick="nextImage()">&#9654;</button>
                <div id="image-subtitle"></div>
            </div>
            <!-- Table of Contents (lower half) -->
            <div id="toc">
                <h2>Table of Contents</h2>
                <ul>
"""
    # Add TOC entries.
    for mp in main_points_list:
        html_content += f'                    <li><a href="#{mp["id"]}" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n'
    html_content += """                </ul>
            </div>
        </div>
        <!-- Transcripts Wrapper (English and Spanish) -->
        <div id="transcripts-wrapper">
            <!-- English Transcript -->
            <div id="transcript-en" class="transcript-column">
                <div id="transcript-title-en">Transcript (English)</div>
                <pre>
"""
    html_content += processed_en
    html_content += """                </pre>
            </div>
"""
    if processed_es:
        html_content += """            <!-- Spanish Transcript -->
            <div id="transcript-es" class="transcript-column">
                <div id="transcript-title-es">Transcript (Spanish)</div>
                <pre>
"""
        html_content += processed_es
        html_content += """                </pre>
            </div>
"""
    html_content += """        </div>
    </div>
    <script>
        // Global array of section images (populated from Python)
        var sectionImages = """ + section_images_json + """;
        // Build an array of image keys from the main points that specify an "image" attribute.
        var imageSections = [];
        var mainPoints = """ + json.dumps(main_points_list) + """;
        for (var i = 0; i < mainPoints.length; i++) {
            if (mainPoints[i].hasOwnProperty("image")) {
                imageSections.push({section_id: mainPoints[i].id, image_key: mainPoints[i].image});
            }
        }
        var currentImageIndex = 0;
        // Build a mapping from index to image info
        var indices_to_image = {};
        for (var i = 0; i < imageSections.length; i++) {
            var key = imageSections[i].image_key;
            indices_to_image[i] = {section_id: imageSections[i].section_id, info: sectionImages[key]};
        }
        function updateImage() {
            if (Object.keys(indices_to_image).length > 0) {
                // Get the image info for the current index.
                var imgObj = indices_to_image[currentImageIndex];
                document.getElementById("current-image").src = imgObj.info.src;
                document.getElementById("image-subtitle").textContent = imgObj.info.subtitle;
            }
        }
        function prevImage() {
            if (Object.keys(indices_to_image).length > 0) {
                currentImageIndex = (currentImageIndex - 1 + Object.keys(indices_to_image).length) % Object.keys(indices_to_image).length;
                updateImage();
            }
        }
        function nextImage() {
            if (Object.keys(indices_to_image).length > 0) {
                currentImageIndex = (currentImageIndex + 1) % Object.keys(indices_to_image).length;
                updateImage();
            }
        }
        // Initially update the image (if any).
        updateImage();
        
        // Function to jump the audio player to a specified time (in seconds)
        function jumpToTime(seconds) {
            var audio = document.getElementById("audioPlayer");
            audio.currentTime = seconds;
            audio.play();
        }
        // Function to jump to a section: scroll the English transcript to the corresponding anchor,
        // update the image if that section has an associated image, and sync Spanish transcript scroll.
        function jumpToSection(sectionId, seconds) {
            jumpToTime(seconds);
            var enAnchor = document.getElementById(sectionId);
            var enContainer = document.getElementById("transcript-en");
            if (enAnchor && enContainer) {
                enAnchor.scrollIntoView({ behavior: "smooth", block: "start" });
            }
            // Check if this section has an associated image and update the image container.
            for (var i = 0; i < imageSections.length; i++) {
                if (imageSections[i].section_id === sectionId) {
                    currentImageIndex = i;
                    updateImage();
                    break;
                }
            }
            // Also attempt to sync Spanish transcript scroll if present.
            var esAnchor = document.querySelector("#transcript-es #" + sectionId);
            var esContainer = document.getElementById("transcript-es");
            if (esAnchor && esContainer) {
                var enRect = enAnchor.getBoundingClientRect();
                var enContainerRect = enContainer.getBoundingClientRect();
                var relativeEnTop = enRect.top - enContainerRect.top;
                var esRect = esAnchor.getBoundingClientRect();
                var esContainerRect = esContainer.getBoundingClientRect();
                var relativeEsTop = esRect.top - esContainerRect.top;
                var delta = relativeEnTop - relativeEsTop;
                esContainer.scrollBy({ top: delta, behavior: "smooth" });
            }
        }
        // Optionally, continuously sync scrolling between English and Spanish transcript columns.
        var enDiv = document.getElementById("transcript-en");
        var esDiv = document.getElementById("transcript-es");
        if (enDiv && esDiv) {
            enDiv.addEventListener("scroll", function() {
                esDiv.scrollTop = enDiv.scrollTop;
                // Additionally, check for the closest section with an image.
                var newIndex = currentImageIndex;
                imageSections.forEach(function(imgObj, index) {
                    var anchor = document.getElementById(imgObj.section_id);
                    if (anchor) {
                        var rect = anchor.getBoundingClientRect();
                        var containerRect = enDiv.getBoundingClientRect();
                        if (rect.top >= containerRect.top && rect.top < containerRect.top + 100) {
                            newIndex = index;
                        }
                    }
                });
                if (newIndex !== currentImageIndex) {
                    currentImageIndex = newIndex;
                    updateImage();
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

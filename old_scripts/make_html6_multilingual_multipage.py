#!/usr/bin/env python3
import re

# === Configuration Dictionary for All Interviews ===
config_dict = {
    "RositaInterview4_29_20-11_17_23": {
        "page_id": "RositaInterview4_29_20-11_17_23",
        "transcript_file": "transcripts/RositaInterview4_29_20-11_17_23_English.txt",
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
    }
}

# === Define the Main Points for Each Interview ===
main_points_dict = {
    "RositaInterview4_29_20-11_17_23": [
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

# === Function to Generate a Single HTML Page with Navigation and Two Transcripts ===
def generate_page_with_nav(config, main_points_list, all_configs):
    # Process the English transcript.
    processed_en = process_transcript(config["transcript_file"], main_points_list)
    # If a Spanish transcript is provided, process it; otherwise, leave it empty.
    processed_es = ""
    if "spanish_transcript_file" in config:
        processed_es = process_transcript(config["spanish_transcript_file"], main_points_list)
    
    # Build the navigation block linking to all other pages.
    nav_links = []
    for key, conf in all_configs.items():
        if conf["page_id"] != config["page_id"]:
            nav_links.append(f'<a href="{conf["output_file"]}" style="font-size:1.2em; color:darkblue; text-decoration:none;">Switch to {conf["page_title"]}</a>')
    nav_block = " | ".join(nav_links)
    
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
        /* Flex container for side-by-side layout */
        #container {{
            display: flex;
            gap: 20px;
        }}
        /* Table of Contents styling */
        #toc {{
            flex: 1;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 10px;
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
        /* Transcripts wrapper styling */
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
    <div id="nav" style="margin-bottom:20px;">
        {nav_block}
    </div>
    <!-- Audio Player -->
    <audio id="audioPlayer" controls>
        <source src="{config["audio_file"]}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <!-- Container for TOC and Transcripts -->
    <div id="container">
        <!-- Table of Contents -->
        <div id="toc">
            <h2>Table of Contents</h2>
            <ul>
"""
    # Add TOC entries.
    for mp in main_points_list:
        html_content += f'                <li><a href="#{mp["id"]}" onclick="jumpToSection(\'{mp["id"]}\', {mp["start_time"]}); return false;">{mp["title"]} ({mp["display_time"]})</a></li>\n'
    html_content += """            </ul>
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
    # If a Spanish transcript exists, add its column.
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
        // Function to jump the audio player to a specified time (in seconds)
        function jumpToTime(seconds) {
            var audio = document.getElementById("audioPlayer");
            audio.currentTime = seconds;
            audio.play();
        }
        // Function to jump both the audio and scroll the English transcript container to the specified section
        function jumpToSection(sectionId, seconds) {
            jumpToTime(seconds);
            var target = document.getElementById(sectionId);
            if (target) {
                // Scroll the English transcript container
                document.getElementById("transcript-en").scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }
        // Sync scrolling between English and Spanish transcript columns
        var enDiv = document.getElementById("transcript-en");
        var esDiv = document.getElementById("transcript-es");
        if (enDiv && esDiv) {
            enDiv.addEventListener("scroll", function() {
                esDiv.scrollTop = enDiv.scrollTop;
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

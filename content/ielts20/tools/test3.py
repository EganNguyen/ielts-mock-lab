"""IELTS 20 Academic — Test 3."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts20-test3",
        "title": "IELTS 20 · Academic Test 3",
        "module": "Academic",
        "version": "ielts20.1",
        "listening": build_listening(keys, transcripts),
        "reading": build_reading(passages, keys),
        "writing": build_writing(),
        "speaking": build_speaking(),
        "publishedAt": "2026-11-12T00:00:00Z",
        "scoring": {
            "listeningVersion": "ielts-academic-2026",
            "readingVersion": "ielts-academic-2026",
            "rubricVersion": "apex-local-rubric-v1",
        },
    }


def build_listening(keys, transcripts):
    parts = []

    # Part 1 -----------------------------------------------------------------
    g1 = group(
        "l1-g1", "Questions 1–10",
        "Complete the table below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 11)), layout="form", body=[
            "# Furniture rental companies",
            "• Peak Rentals — prices range from $105 to ${{1}} per room per month — the furniture is very {{2}} — delivers in 1–2 days — free {{3}} with every living room set",
            "• {{4}} and Oliver — mid-range prices — 12% monthly fee for {{5}} — also offers a cleaning service",
            "• Larch Furniture — offers the cheapest prices for renting furniture and {{6}} items — must have own {{7}} — minimum contract length: six months",
            "• {{8}} Rentals — see the {{9}} for the most up-to-date prices — {{10}} are allowed within 7 days of delivery",
        ])
    qs = [
        question(1, "l1-g1", "Top price per room per month at Peak Rentals"),
        question(2, "l1-g1", "What the furniture at Peak Rentals is like"),
        question(3, "l1-g1", "Free item with every living room set"),
        question(4, "l1-g1", "Second company name"),
        question(5, "l1-g1", "What the 12% monthly fee is for"),
        question(6, "l1-g1", "Type of items Larch Furniture also rents"),
        question(7, "l1-g1", "What Larch customers must have"),
        question(8, "l1-g1", "Fourth company name"),
        question(9, "l1-g1", "Where to see the most up-to-date prices"),
        question(10, "l1-g1", "What is allowed within 7 days of delivery"),
    ]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Furniture rental companies",
        "context": "A woman compares three furniture rental companies.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    g2 = group(
        "l2-g1", "Questions 11–16", "Choose the correct letter, A, B or C.",
        list(range(11, 17)),
    )
    mcq = [
        (11, "Who was responsible for starting the community project?",
         ["the castle owners", "a national charity", "the local council"]),
        (12, "How was the gold coin found?",
         ["Heavy rain had removed some of the soil.", "The ground was dug up by wild rabbits.",
          "A person with a metal detector searched the area."]),
        (13, "What led the archaeologists to believe there was an ancient village on this site?",
         ["the lucky discovery of old records", "the bases of several structures visible in the grass",
          "the unusual stones found near the castle"]),
        (14, "What are the team still hoping to find?",
         ["everyday pottery", "animal bones", "pieces of jewellery"]),
        (15, "What was found on the other side of the river to the castle?",
         ["the remains of a large palace", "the outline of fields", "a number of small huts"]),
        (16, "What do the team plan to do after work ends this summer?",
         ["prepare a display for a museum", "take part in a television programme",
          "start to organise school visits"]),
    ]
    qs2 = [question(n, "l2-g1", prompt, "mcq", options) for n, prompt, options in mcq]
    g3 = group(
        "l2-g2", "Questions 17–20",
        "Label the map below. Drag the correct letter, A–G, next to Questions 17–20.",
        list(range(17, 21)), layout="map",
        figure="/media/figures/ielts20/test3-listening-map.jpg",
        figureAlt="Plan of the Bidcaster Archaeological Dig, with locations A to G around the castle walls and river.",
    )
    qs2 += [
        question(17, "l2-g2", "bridge foundations", "map"),
        question(18, "l2-g2", "rubbish pit", "map"),
        question(19, "l2-g2", "meeting hall", "map"),
        question(20, "l2-g2", "fish pond", "map"),
    ]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "The Bidcaster archaeological dig",
        "context": "An archaeologist describes the community excavation at Bidcaster.",
        "groups": [g2, g3], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    g4 = group(
        "l3-g1", "Questions 21–26", "Choose the correct letter, A, B or C.",
        list(range(21, 27)),
    )
    mcq3 = [
        (21, "Finn was pleased to discover that their topic",
         ["was not familiar to their module leader.", "had not been chosen by other students.",
          "did not prove to be difficult to research."]),
        (22, "Maya says a mistaken belief about theatre programmes is that",
         ["theatres pay companies to produce them.", "few theatre-goers buy them nowadays.",
          "they contain far more adverts than previously."]),
        (23, "Finn was surprised that, in early British theatre, programmes",
         ["were difficult for audiences to obtain.", "were given out free of charge.",
          "were seen as a kind of contract."]),
        (24, "Maya feels their project should include an explanation of why companies of actors",
         ["promoted their own plays.", "performed plays outdoors.", "had to tour with their plays."]),
        (25, "Finn and Maya both think that, compared to nineteenth-century programmes, those from the eighteenth century",
         ["were more original.", "were more colourful.", "were more informative."]),
        (26, "Maya doesn't fully understand why, in the twentieth century,",
         ["very few theatre programmes were printed in the USA.",
          "British theatre programmes failed to develop for so long.",
          "theatre programmes in Britain copied fashions from the USA."]),
    ]
    qs3 = [question(n, "l3-g1", prompt, "mcq", options) for n, prompt, options in mcq3]
    comments = [
        "A Its origin is somewhat controversial.",
        "B It is historically significant for a country.",
        "C It was effective at attracting audiences.",
        "D It is included in a recent project.",
        "E It contains insights into the show.",
        "F It resembles an artwork.",
    ]
    g5 = group(
        "l3-g2", "Questions 27–30",
        "What comment is made about the programme for each of the following shows? Choose FOUR answers from the box and write the correct letter, A–F.",
        list(range(27, 31)), layout="match", shared=comments,
    )
    qs3 += [question(n, "l3-g2", show, "match") for n, show in [
        (27, "Ruy Blas"), (28, "Man of La Mancha"),
        (29, "The Tragedy of Jane Shore"), (30, "The Sailors' Festival"),
    ]]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "A project on theatre programmes",
        "context": "Two students discuss their research project on the history of theatre programmes.",
        "groups": [g4, g5], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g6 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Inclusive design",
            "## Definition",
            "• Designing products that can be accessed by a diverse range of people without the need for any {{31}}.",
            "• Not the same as universal design: that is design for everyone, including catering for people with {{32}} problems.",
            "## Examples of inclusive design",
            "• {{33}} which are adjustable, avoiding back or neck problems",
            "• {{34}} in public toilets which are easier to use",
            "• To assist the elderly: designers avoid using {{35}} in interfaces; people can make commands using a mouse, keyboard or their {{36}}.",
            "## Impact of non-inclusive designs",
            "• Access: loss of independence for disabled people.",
            "• Safety: seatbelts are especially problematic for {{37}} women; PPE jackets are often unsuitable because of the size of women's {{38}}; PPE for female {{39}} officers dealing with emergencies is the worst.",
            "• Comfort in the workplace: the {{40}} in offices is often too low for women.",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "What inclusive design avoids the need for"),
        (32, "Type of problems universal design caters for"),
        (33, "Adjustable workplace items that prevent back or neck problems"),
        (34, "Public toilet items that are easier to use"),
        (35, "Colour avoided in interfaces for the elderly"),
        (36, "What people can use to make commands besides a mouse or keyboard"),
        (37, "Seatbelts are especially problematic for this group of women"),
        (38, "Body measurement that makes PPE jackets unsuitable"),
        (39, "Female officers whose PPE is the worst"),
        (40, "Workplace factor that is often too low for women"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Inclusive design",
        "context": "A lecture about inclusive design and the problems caused by non-inclusive products.",
        "groups": [g6], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 --------------------------------------------------------------
    r1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–7",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(1, 8)), layout="notes", body=[
            "# The history of frozen food",
            "## 2,000 years ago, South America",
            "People conserved the nutritional value of {{1}}, using a method of freezing then drying.",
            "## 1851, USA",
            "• {{2}} was kept cool by ice during transportation in specially adapted trains.",
            "## 1880, Australia",
            "• Two kinds of {{3}} were the first frozen food shipped to England.",
            "## 1917 onwards, USA",
            "Clarence Birdseye introduced innovations including:",
            "• quick-freezing methods, so that {{4}} did not spoil the food.",
            "• packaging products with {{5}}, so the product was visible.",
            "## Early 1940s, USA",
            "• Frozen food became popular because of a shortage of {{6}}.",
            "## 1950s, USA",
            "• A large number of homes now had a {{7}}.",
        ])
    qs = [question(n, "r1-g1", f"Frozen food notes {n}") for n in range(1, 8)]
    g2 = group(
        "r1-g2", "Questions 8–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(8, 14)),
    )
    qs += [
        question(8, "r1-g2", "The ice transportation business made some Boston ship owners very wealthy in the early 1800s.", "tfng"),
        question(9, "r1-g2", "A disadvantage of the freezing process invented in Australia was that it affected the taste of food.", "tfng"),
        question(10, "r1-g2", "Clarence Birdseye travelled to Labrador in order to learn how the Inuit people froze fish.", "tfng"),
        question(11, "r1-g2", "Swanson Foods invested a great deal of money in the promotion of the TV Dinner.", "tfng"),
        question(12, "r1-g2", "Swanson Foods developed a new style of container for the launch of the TV Dinner.", "tfng"),
        question(13, "r1-g2", "The US frozen food industry is currently the largest in the world.", "tfng"),
    ]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 --------------------------------------------------------------
    r2 = passage(2, passages["2"])
    headings = [
        "i   Tried and tested solutions",
        "ii   Cooperation beneath the waves",
        "iii   Working to lessen the problems",
        "iv   Disagreement about the accuracy of a certain phrase",
        "v   Two clear educational goals",
        "vi   Promoting hope",
        "vii   A warning of further trouble ahead",
    ]
    g3 = group(
        "r2-g1", "Questions 14–19",
        "Reading Passage 2 has six sections, A–F. Choose the correct heading for each section from the list of headings below.",
        list(range(14, 20)), shared=headings,
        note="There are more headings than sections, so you will not use all of them.",
    )
    qs2 = [question(n, "r2-g1", f"Section {label}", "heading")
           for n, label in zip(range(14, 20), "ABCDEF")]

    damage = [
        "a rising number of extreme storms", "the removal of too many fish from the sea",
        "the contamination of the sea from waste", "increased disease among marine species",
        "alterations in the usual flow of water in the seas",
    ]
    g4 = group(
        "r2-g2", "Questions 20 and 21",
        "Choose TWO letters, A–E. Which TWO of these causes of damage to coral reefs are mentioned by the writer of the text?",
        [20, 21],
    )
    qs2 += [
        question(20, "r2-g2", "First cause of damage to coral reefs", "mcq", damage),
        question(21, "r2-g2", "Second cause of damage to coral reefs", "mcq", damage),
    ]
    zoo = [
        "They are hoping to expand the numbers of different corals being bred in laboratories.",
        "They want to identify corals that can cope well with the changed sea conditions.",
        "They are looking at ways of creating artificial reefs that corals could grow on.",
        "They are trying out methods that would speed up reproduction in some corals.",
        "They are investigating materials that might protect reefs from higher temperatures.",
    ]
    g5 = group(
        "r2-g3", "Questions 22 and 23",
        "Choose TWO letters, A–E. Which TWO of the following statements are true of the researchers at London Zoo?",
        [22, 23],
    )
    qs2 += [
        question(22, "r2-g3", "First statement true of the London Zoo researchers", "mcq", zoo),
        question(23, "r2-g3", "Second statement true of the London Zoo researchers", "mcq", zoo),
    ]
    g6 = group(
        "r2-g4", "Questions 24–26",
        "Complete the sentences below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(24, 27)), layout="summary", body=[
            "Corals have a number of {{24}} which they use to collect their food.",
            "Algae gain {{25}} from being inside the coral.",
            "Increases in the warmth of the sea water can remove the {{26}} from coral.",
        ])
    qs2 += [question(n, "r2-g4", f"Coral sentence {n}") for n in range(24, 27)]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5, g6]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 --------------------------------------------------------------
    r3 = passage(3, passages["3"])
    experts = ["A Martin Rees", "B Daniel Wolpert", "C Kathleen Richardson"]
    g7 = group(
        "r3-g1", "Questions 27–33",
        "Look at the following statements and the list of experts below. Match each statement with the correct expert, A, B or C. NB You may use any letter more than once.",
        list(range(27, 34)), layout="match", shared=experts,
    )
    statements = [
        (27, "For our own safety, humans will need to restrict the abilities of robots."),
        (28, "The risk of robots harming us is less serious than humans believe it to be."),
        (29, "It will take many decades for robot intelligence to be as imaginative as human intelligence."),
        (30, "We may have to start considering whether we are treating robots fairly."),
        (31, "Robots are probably of more help to us on Earth than in space."),
        (32, "The ideas in high-quality science fiction may prove to be just as accurate as those found in the work of mediocre scientists."),
        (33, "There are those who look forward to robots developing greater intelligence."),
    ]
    qs3 = [question(n, "r3-g1", text, "match") for n, text in statements]
    endings = [
        "A robots to explore outer space.",
        "B advances made in machine intelligence so far.",
        "C changes made to other planets for our own benefit.",
        "D the harm already done by artificial intelligence.",
    ]
    g8 = group(
        "r3-g2", "Questions 34–36",
        "Complete each sentence with the correct ending, A–D, below.",
        list(range(34, 37)), layout="select", shared=endings,
    )
    qs3 += [
        question(34, "r3-g2", "Richardson and Rees express similar views regarding the ethical aspect of", "select"),
        question(35, "r3-g2", "Rees and Wolpert share an opinion about the extent of", "select"),
        question(36, "r3-g2", "Wolpert disagrees with Richardson on the question of", "select"),
    ]
    g9 = group(
        "r3-g3", "Questions 37–40", "Choose the correct letter, A, B, C or D.",
        list(range(37, 41)),
    )
    mcq = [
        (37, "What point does Richardson make about fear of machines?",
         ["It has grown alongside the development of ever more advanced robots.",
          "It is the result of our inclination to attribute human characteristics to non-human entities.",
          "It has its origins in basic misunderstandings about how inanimate objects function.",
          "It demonstrates a key difference between human intelligence and machine intelligence."]),
        (38, "What potential advance does Rees see as a cause for concern?",
         ["robots outnumbering people", "robots having abilities which humans do not",
          "artificial intelligence developing independent thought",
          "artificial intelligence taking over every aspect of our lives"]),
        (39, "What does Wolpert emphasise in his response to the question about science fiction?",
         ["how science fiction influences our attitudes to robots",
          "how fundamental robots are to the science fiction genre",
          "how the image of robots in science fiction has changed over time",
          "how reactions to similar portrayals of robots in science fiction may vary"]),
        (40, "What is Richardson doing in her comment about reality and fantasy?",
         ["warning people not to confuse one with the other",
          "outlining ways in which one has impacted on the other",
          "recommending a change of approach in how people view them",
          "explaining why scientists have a different perspective on them from other people"]),
    ]
    qs3 += [question(n, "r3-g3", prompt, "mcq", options) for n, prompt, options in mcq]
    apply_keys(qs3, keys["reading"], "r3")
    r3["groups"] = [g7, g8, g9]
    r3["questions"] = qs3
    reading.append(r3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The charts below give information about a public library in a town called Little Chalfont.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts20/test3-writing-task1.jpg",
            "figureAlt": "Pie chart of library members by age, a table of loans by category and a bar chart of total loans from 2007 to 2016.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "Some people have decided to reduce the number of times they fly every year or to stop flying altogether.\n\nDo you think the environmental benefits of this development outweigh the disadvantages for individuals and businesses?",
            "instructions": [
                "Give reasons for your answer and include any relevant examples from your own knowledge or experience.",
                "Write at least 250 words.", "You should spend about 40 minutes on this task.",
            ],
            "minimumWords": 250, "suggestedMinutes": 40,
        },
    ]


def build_speaking():
    return [
        {
            "id": "speaking-1", "number": 1, "title": "Part 1 · Interview",
            "description": "The examiner asks you about museums.",
            "questions": [
                {"id": "s1", "text": "Did you enjoy going to museums when you were a child?"},
                {"id": "s2", "text": "Are there any interesting museums near where you live now?"},
                {"id": "s3", "text": "Do you think it is best to go to museums by yourself or with friends?"},
                {"id": "s4", "text": "When you visit another city or country, do you think it's important to go to a museum there?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a piece of work you did for your job or your studies that you felt very satisfied with.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a piece of work you did for your job or your studies that you felt very satisfied with.",
                "bullets": ["what this piece of work was", "why you did this piece of work",
                            "who or what helped you to do this work"],
                "rounding": "and explain why you felt so satisfied with this piece of work.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: satisfaction in life and at work.",
            "questions": [
                {"id": "s5", "text": "What are some aspects of people's lives that they can often be dissatisfied with?"},
                {"id": "s6", "text": "Would you say that having ambitions in life is always a positive thing?"},
                {"id": "s7", "text": "What do you believe the most important components are of a satisfying life?"},
                {"id": "s8", "text": "What makes a job more satisfying: a high salary or having good colleagues?"},
                {"id": "s9", "text": "Do you think people need to change jobs regularly if they want to stay satisfied at work?"},
                {"id": "s10", "text": "Is it possible to find job satisfaction in all types of work?"},
            ],
        },
    ]

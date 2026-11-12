"""IELTS 20 Academic — Test 1."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts20-test1",
        "title": "IELTS 20 · Academic Test 1",
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
            "# Restaurant recommendations",
            "• The Junction — Greyson Street, near the station — especially good for people who are keen on {{1}} — quite expensive — the {{2}} is a good place for a drink",
            "• Paloma — in Bow Street, next to the cinema — {{3}} food, good for sharing — staff very friendly — £50 deposit — a limited selection of {{4}} food on the menu",
            "• The {{5}} — at the top of a {{6}} — a famous chef — all the {{7}} are very good — only uses {{8}} ingredients — set lunch costs £{{9}} per person — portions of {{10}} size",
        ])
    qs = [
        question(1, "l1-g1", "What The Junction is especially good for"),
        question(2, "l1-g1", "Good place for a drink at The Junction"),
        question(3, "l1-g1", "Type of food at Paloma"),
        question(4, "l1-g1", "Limited selection on Paloma's menu"),
        question(5, "l1-g1", "Name of the third restaurant"),
        question(6, "l1-g1", "Building the third restaurant is at the top of"),
        question(7, "l1-g1", "What is very good at the third restaurant"),
        question(8, "l1-g1", "Type of ingredients the third restaurant uses"),
        question(9, "l1-g1", "Cost of the set lunch per person"),
        question(10, "l1-g1", "Size of the portions"),
    ]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Choosing a restaurant",
        "context": "A woman asks a friend for advice about restaurants for a family celebration.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    g2 = group(
        "l2-g1", "Questions 11–16", "Choose the correct letter, A, B or C.",
        list(range(11, 17)),
    )
    mcq = [
        (11, "Heather says pottery differs from other art forms because",
         ["it lasts longer in the ground.", "it is practised by more people.",
          "it can be repaired more easily."]),
        (12, "Archaeologists sometimes identify the use of ancient pottery from",
         ["the clay it was made with.", "the marks that are on it.", "the basic shape of it."]),
        (13, "Some people join Heather's pottery class because they want to",
         ["create an item that looks very old.", "find something that they are good at.",
          "make something that will outlive them."]),
        (14, "What does Heather value most about being a potter?",
         ["its calming effect", "its messy nature", "its physical benefits"]),
        (15, "Most of the visitors to Edelman Pottery",
         ["bring friends to join courses.", "have never made a pot before.",
          "try to learn techniques too quickly."]),
        (16, "Heather reminds her visitors that they should",
         ["put on their aprons.", "change their clothes.", "take off their jewellery."]),
    ]
    qs2 = [question(n, "l2-g1", prompt, "mcq", options) for n, prompt, options in mcq]

    kilns = [
        "what their function is", "when they were invented",
        "ways of keeping them safe", "where to put one in your home",
        "what some people use instead of one",
    ]
    g3 = group(
        "l2-g2", "Questions 17 and 18",
        "Choose TWO letters, A–E. Which TWO things does Heather explain about kilns?",
        [17, 18],
    )
    qs2 += [
        question(17, "l2-g2", "First thing Heather explains about kilns", "mcq", kilns),
        question(18, "l2-g2", "Second thing Heather explains about kilns", "mcq", kilns),
    ]

    tools = [
        "Some are hard to hold.", "Some are worth buying.", "Some are essential items.",
        "Some have memorable names.", "Some are available for use by participants.",
    ]
    g4 = group(
        "l2-g3", "Questions 19 and 20",
        "Choose TWO letters, A–E. Which TWO points does Heather make about a potter's tools?",
        [19, 20],
    )
    qs2 += [
        question(19, "l2-g3", "First point about a potter's tools", "mcq", tools),
        question(20, "l2-g3", "Second point about a potter's tools", "mcq", tools),
    ]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "A visit to a pottery",
        "context": "A potter talks to a group of visitors about her craft and the equipment she uses.",
        "groups": [g2, g3, g4], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    causes = ["social media", "smaller nuclear families", "urban design",
              "longer lifespans", "a mobile workforce"]
    g5 = group(
        "l3-g1", "Questions 21 and 22",
        "Choose TWO letters, A–E. Which TWO things do the students both believe are responsible for the increase in loneliness?",
        [21, 22],
    )
    qs3 = [
        question(21, "l3-g1", "First cause of the increase in loneliness", "mcq", causes),
        question(22, "l3-g1", "Second cause of the increase in loneliness", "mcq", causes),
    ]

    risks = ["a weakened immune system", "dementia", "cancer", "obesity",
             "cardiovascular disease"]
    g6 = group(
        "l3-g2", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO health risks associated with loneliness do the students agree are based on solid evidence?",
        [23, 24],
    )
    qs3 += [
        question(23, "l3-g2", "First health risk based on solid evidence", "mcq", risks),
        question(24, "l3-g2", "Second health risk based on solid evidence", "mcq", risks),
    ]

    opinions = [
        "It has little practical relevance.", "It needs further investigation.",
        "It is misleading.", "It should be more widely accepted.",
        "It is difficult to understand.",
    ]
    g7 = group(
        "l3-g3", "Questions 25 and 26",
        "Choose TWO letters, A–E. Which TWO opinions do both the students express about the evolutionary theory of loneliness?",
        [25, 26],
    )
    qs3 += [
        question(25, "l3-g3", "First opinion about the evolutionary theory", "mcq", opinions),
        question(26, "l3-g3", "Second opinion about the evolutionary theory", "mcq", opinions),
    ]

    g8 = group(
        "l3-g4", "Questions 27–30", "Choose the correct letter, A, B or C.",
        list(range(27, 31)),
    )
    mcq3 = [
        (27, "When comparing loneliness to depression, the students",
         ["doubt that there will ever be a medical cure for loneliness.",
          "claim that the link between loneliness and mental health is overstated.",
          "express frustration that loneliness is not taken more seriously."]),
        (28, "Why do the students decide to start their presentation with an example from their own experience?",
         ["to explain how difficult loneliness can be",
          "to highlight a situation that most students will recognise",
          "to emphasise that feeling lonely is more common for men than women"]),
        (29, "The students agree that talking to strangers is a good strategy for dealing with loneliness because",
         ["it creates a sense of belonging.", "it builds self-confidence.",
          "it makes people feel more positive."]),
        (30, "The students find it difficult to understand why solitude is considered to be",
         ["similar to loneliness.", "necessary for mental health.",
          "an enjoyable experience."]),
    ]
    qs3 += [question(n, "l3-g4", prompt, "mcq", options) for n, prompt, options in mcq3]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "A presentation on loneliness",
        "context": "Two students discuss their presentation on loneliness and mental health.",
        "groups": [g5, g6, g7, g8], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g9 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Reclaiming urban rivers",
            "## Historical background",
            "• Nearly all major cities were built on a river.",
            "• Rivers were used for transport, fishing and recreation.",
            "• Industrial development and rising populations led to more sewage and pollution from {{31}} on the river bank.",
            "• In 1957, the River Thames was declared biologically {{32}}.",
            "## Recent improvements",
            "• Seals and even a {{33}} have been seen in the River Thames.",
            "• Riverside warehouses are converted into restaurants and {{34}}.",
            "• In Los Angeles, plans include a riverside {{35}} and displays of {{36}} projects.",
            "• In Paris, {{37}} are created on the sides of the river every summer.",
            "## Transport possibilities",
            "• Over 2 billion passengers already travel by {{38}} in cities around the world.",
            "• Goods could travel by freight barges and electric {{39}}, or in future by {{40}}.",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "Source of pollution on the river bank"),
        (32, "What the River Thames was declared biologically in 1957"),
        (33, "Large sea animal seen in the River Thames"),
        (34, "Buildings riverside warehouses are converted into, besides restaurants"),
        (35, "Riverside facility planned in Los Angeles"),
        (36, "Type of projects to be displayed in Los Angeles"),
        (37, "What is created on the sides of the river in Paris every summer"),
        (38, "Form of transport already used by over 2 billion passengers"),
        (39, "Electric vehicles that could transport goods"),
        (40, "Future method of transporting goods"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Reclaiming urban rivers",
        "context": "A lecture about how cities are bringing their rivers back into public use.",
        "groups": [g9], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 --------------------------------------------------------------
    r1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–6",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(1, 7)),
    )
    qs = [
        question(1, "r1-g1", "There are other parrots that share the kākāpō's inability to fly.", "tfng"),
        question(2, "r1-g1", "Adult kākāpō produce chicks every year.", "tfng"),
        question(3, "r1-g1", "Adult male kākāpō bring food back to nesting females.", "tfng"),
        question(4, "r1-g1", "The Polynesian rat was a greater threat to the kākāpō than Polynesian settlers.", "tfng"),
        question(5, "r1-g1", "Kākāpō were transferred from Rakiura Island to other locations because they were at risk from feral cats.", "tfng"),
        question(6, "r1-g1", "One Recovery Plan initiative that helped increase the kākāpō population size was caring for struggling young birds.", "tfng"),
    ]
    g2 = group(
        "r1-g2", "Questions 7–13",
        "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        list(range(7, 14)), layout="notes", body=[
            "# New Zealand's kākāpō",
            "## A type of parrot",
            "• diet consists of fern fronds, various parts of a tree and {{7}}",
            "• nests are created in {{8}}, where eggs are laid",
            "## Arrival of Polynesian settlers",
            "• the {{9}} of the kākāpō were used to make clothes",
            "## Arrival of European colonisers",
            "• {{10}} were an animal they introduced that ate the kākāpō's food sources",
            "## Protecting kākāpō",
            "• Richard Henry, a conservationist, tried to protect the kākāpō",
            "• a definite sighting of female kākāpō on Rakiura Island was reported in the year {{11}}",
            "• the Recovery Plan included an increase in {{12}}",
            "• a current goal of the Recovery Plan is to maintain the involvement of {{13}} in kākāpō protection",
        ])
    qs += [question(n, "r1-g2", f"Kākāpō notes {n}") for n in range(7, 14)]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 --------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–18",
        "Reading Passage 2 has seven sections, A–G. Which section contains the following information? Write the correct letter, A–G. NB You may use any letter more than once.",
        list(range(14, 19)), layout="match", shared=list("ABCDEFG"),
    )
    qs2 = [
        question(14, "r2-g1", "reference to the research problems that arise from there being only a few surviving large elms", "match"),
        question(15, "r2-g1", "details of a difference of opinion about the value of reintroducing elms to Britain", "match"),
        question(16, "r2-g1", "reference to how Dutch elm disease was brought into Britain", "match"),
        question(17, "r2-g1", "a description of the conditions that have enabled a location in Britain to escape Dutch elm disease", "match"),
        question(18, "r2-g1", "reference to the stage at which young elms become vulnerable to Dutch elm disease", "match"),
    ]
    people = ["A Matt Elliot", "B Karen Russell", "C Peter Bourne"]
    g4 = group(
        "r2-g2", "Questions 19–23",
        "Look at the following statements and the list of people below. Match each statement with the correct person, A, B or C. NB You may use any letter more than once.",
        list(range(19, 24)), layout="match", shared=people,
    )
    qs2 += [
        question(19, "r2-g2", "If a tree gets infected with Dutch elm disease, the damage rapidly becomes visible.", "match"),
        question(20, "r2-g2", "It may be better to wait and see if the mature elms that have survived continue to flourish.", "match"),
        question(21, "r2-g2", "There must be an explanation for the survival of some mature elms.", "match"),
        question(22, "r2-g2", "We need to be aware that insects carrying Dutch elm disease are not very far away.", "match"),
        question(23, "r2-g2", "You understand the effect Dutch elm disease has had when you see evidence of how prominent the tree once was.", "match"),
    ]
    g5 = group(
        "r2-g3", "Questions 24–26",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(24, 27)), layout="summary", body=[
            "# Uses of a popular tree",
            "For hundreds of years, the only tree that was more popular in Britain than elm was {{24}}. Starting in the Bronze Age, many tools were made from elm and people also used it to make weapons. In the 18th century, it was grown to provide wood for boxes and {{25}}. Due to its strength, elm was often used for mining equipment and the Cutty Sark's {{26}} was also constructed from elm.",
        ])
    qs2 += [question(n, "r2-g3", f"Uses of elm {n}") for n in range(24, 27)]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 --------------------------------------------------------------
    r3 = passage(3, passages["3"])
    g6 = group(
        "r3-g1", "Questions 27–30", "Choose the correct letter, A, B, C or D.",
        list(range(27, 31)),
    )
    mcq = [
        (27, "In the first paragraph, the writer introduces the topic of the text by",
         ["defining some commonly used terms.", "questioning a widely held assumption.",
          "mentioning a challenge faced by everyone.", "specifying a situation which makes us most anxious."]),
        (28, "What point does the writer make about firefighters in the second paragraph?",
         ["The regular changes of stress levels in their working lives make them ideal study subjects.",
          "The strategies they use to handle stress are of particular interest to researchers.",
          "The stressful nature of their job is typical of many public service professions.",
          "Their personalities make them especially well-suited to working under stress."]),
        (29, "What is the writer doing in the fourth paragraph?",
         ["explaining their findings", "justifying their approach",
          "setting out their objectives", "describing their methodology"]),
        (30, "In the seventh paragraph, the writer describes a mechanism in the brain which",
         ["enables people to respond more quickly to stressful situations.",
          "results in increased ability to control our levels of anxiety.",
          "produces heightened sensitivity to indications of external threats.",
          "is activated when there is a need to communicate a sense of danger."]),
    ]
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in mcq]

    endings = [
        "A made them feel optimistic.",
        "B took relatively little notice of bad news.",
        "C responded to negative and positive information in the same way.",
        "D were feeling under stress.",
        "E put them in a stressful situation.",
        "F behaved in a similar manner, regardless of the circumstances.",
        "G thought it more likely that they would experience something bad.",
    ]
    g7 = group(
        "r3-g2", "Questions 31–35",
        "Complete each sentence with the correct ending, A–G, below.",
        list(range(31, 36)), layout="select", shared=endings,
    )
    starts = [
        (31, "At times when they were relaxed, the firefighters usually"),
        (32, "The researchers noted that when the firefighters were stressed, they"),
        (33, "When the firefighters were told good news, they always"),
        (34, "The students' cortisol levels and heart rates were affected when the researchers"),
        (35, "In both experiments, negative information was processed better when the subjects"),
    ]
    qs3 += [question(n, "r3-g2", prompt, "select") for n, prompt in starts]
    g8 = group(
        "r3-g3", "Questions 36–40",
        "Do the following statements agree with the claims of the writer in Reading Passage 3? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(36, 41)),
    )
    qs3 += [
        question(36, "r3-g3", "The tone of the content we post on social media tends to reflect the nature of the posts in our feeds.", "ynng"),
        question(37, "r3-g3", "Phones have a greater impact on our stress levels than other electronic media devices.", "ynng"),
        question(38, "r3-g3", "The more we read about a stressful public event on social media, the less able we are to take the information in.", "ynng"),
        question(39, "r3-g3", "Stress created by social media posts can lead us to take unnecessary precautions.", "ynng"),
        question(40, "r3-g3", "Our tendency to be affected by other people's moods can be used in a positive way.", "ynng"),
    ]
    apply_keys(qs3, keys["reading"], "r3")
    r3["groups"] = [g6, g7, g8]
    r3["questions"] = qs3
    reading.append(r3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The first table below shows changes in the total population of New York City from 1800 to 2000. The second and third tables show changes in the population of the five districts of the city (Manhattan, Brooklyn, Bronx, Queens, Staten Island) over the same period.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts20/test1-writing-task1.jpg",
            "figureAlt": "Three tables showing the population of New York City and the share living in Manhattan and the other four districts in 1800, 1900 and 2000.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "Access to clean water is a basic human right. Therefore, every home should have a water supply that is provided free of charge.\n\nDo you agree or disagree?",
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
            "description": "The examiner asks you about walking and walking holidays.",
            "questions": [
                {"id": "s1", "text": "How much walking do you do in your daily life?"},
                {"id": "s2", "text": "Did you walk more when you were at school than now?"},
                {"id": "s3", "text": "What places are there to go for a walk near where you live?"},
                {"id": "s4", "text": "Would you ever like to go on a walking holiday?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a play or a film you have seen that you would like to see again with friends.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a play or a film you have seen that you would like to see again with friends.",
                "bullets": [
                    "what play or film you'd like to go to see again",
                    "who you would go with",
                    "what other people have said about this play or film",
                ],
                "rounding": "and explain why you would like to see this play or film again with friends.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: theatre audiences and working as an actor.",
            "questions": [
                {"id": "s5", "text": "What are the most popular kinds of plays or shows at theatres in your country?"},
                {"id": "s6", "text": "How easy is it to get tickets to the theatre?"},
                {"id": "s7", "text": "Do you think theatres need to do more to attract younger audiences?"},
                {"id": "s8", "text": "What do you think attracts people to working as an actor?"},
                {"id": "s9", "text": "What are some of the qualities that a person needs to have if they want to become an actor?"},
                {"id": "s10", "text": "Can you think of any disadvantages of working as an actor?"},
            ],
        },
    ]

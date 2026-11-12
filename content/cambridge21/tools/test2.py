"""Cambridge IELTS 21 — Academic Test 2."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "cambridge21-test2",
        "title": "Cambridge IELTS 21 · Academic Test 2",
        "module": "Academic",
        "version": "cambridge21.1",
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
            "# One-day classes at Steynford College",
            "• Vietnamese food — date: {{1}} — £59 — information on the use of herbs — no places at present",
            "• Bread making — 20 March — cost: £{{2}} — extra charge for ingredients — participants make white bread, sourdough and {{3}}",
            "• Face massage — 23 February — £35 — teacher trained in {{4}} — bring a {{5}}",
            "• Candle making — date: {{6}} — £52 — only {{7}} ingredients are used — candles can be used as presents",
            "• Silk painting — 18 May — cost: £{{8}} — bring an apron or old {{9}}",
            "• DIY for beginners — 24 February — £125 — learn how to use a drill, saw and {{10}}; put up a shelf",
        ],
    )
    qs = [question(n, "l1-g1", f"One-day classes table: item {n}") for n in range(1, 11)]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "One-day classes at Steynford College",
        "context": "A telephone conversation about booking one-day classes at a college.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    walk = ["Stop for lunch in an ancient town.", "Don't miss the ruins of a certain building.",
            "Catch a boat to the start of this walk.", "Be careful of the steep and rocky paths.",
            "Don't worry about getting lost."]
    g2 = group(
        "l2-g1", "Questions 11 and 12",
        "Choose TWO letters, A–E. Which TWO pieces of advice are given about the Marsden Coastal Walk?",
        [11, 12],
    )
    qs2 = [
        question(11, "l2-g1", "The first piece of advice", "mcq", walk),
        question(12, "l2-g1", "The second piece of advice", "mcq", walk),
    ]
    heritage = ["This walk is mostly downhill.", "The paths can get busy during the day.",
                "This is a circular walk.", "A tower stands on the site of an older structure.",
                "There are far-reaching views the whole way."]
    g3 = group(
        "l2-g2", "Questions 13 and 14",
        "Choose TWO letters, A–E. Which TWO things are said about the Melby Heritage Walk?",
        [13, 14],
    )
    qs2 += [
        question(13, "l2-g2", "The first thing said about the Melby Heritage Walk", "mcq", heritage),
        question(14, "l2-g2", "The second thing said about the Melby Heritage Walk", "mcq", heritage),
    ]
    g4 = group(
        "l2-g3", "Questions 15–20",
        "Label the map below. Write the correct letter, A–I, next to Questions 15–20.",
        list(range(15, 21)), layout="map",
        figure="/media/figures/cambridge21/test2-listening-map.jpg",
        figureAlt="Map of Melby Coal Mine showing the main visitor centre, car park, engine house and locations labelled A to I.",
    )
    places = [(15, "Exhibition"), (16, "Baths"), (17, "Tools"), (18, "Vehicles"),
              (19, "Ponies"), (20, "Education centre")]
    qs2 += [question(n, "l2-g3", name, "map") for n, name in places]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Walks and Melby Coal Mine",
        "context": "A guide describes two coastal walks and the facilities at a former coal mine.",
        "groups": [g2, g3, g4], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    safety = ["the amount of plastic in the ocean", "the number of diseases caused by contaminated food",
              "the amount of food that is wasted", "the number of people who are obese",
              "the result of treating animals with antibiotics"]
    g5 = group(
        "l3-g1", "Questions 21 and 22",
        "Choose TWO letters, A–E. Which TWO facts in the sessions on food safety were new information for Nadia and Fergus?",
        [21, 22],
    )
    qs3 = [
        question(21, "l3-g1", "The first new fact", "mcq", safety),
        question(22, "l3-g1", "The second new fact", "mcq", safety),
    ]
    fraud = ["the new technology it used", "the publicity it received", "the use of multiple tests on food items",
             "the variety of dietary requirements included", "the way information was made widely accessible"]
    g6 = group(
        "l3-g2", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO features of a project aiming to prevent food fraud impressed Fergus?",
        [23, 24],
    )
    qs3 += [
        question(23, "l3-g2", "The first impressive feature", "mcq", fraud),
        question(24, "l3-g2", "The second impressive feature", "mcq", fraud),
    ]
    course = ["sustainable fishing", "targeted nutrition", "global differences in consumption",
              "sustainable agriculture", "digital technology and food"]
    g7 = group(
        "l3-g3", "Questions 25 and 26",
        "Choose TWO letters, A–E. Which TWO topics do both students recommend should be included in the course?",
        [25, 26],
    )
    qs3 += [
        question(25, "l3-g3", "The first recommended topic", "mcq", course),
        question(26, "l3-g3", "The second recommended topic", "mcq", course),
    ]
    stages = [
        "A This was challenging but enjoyable.", "B This led to some disagreement.",
        "C This was easy to decide on.", "D This was helped by the guidelines provided.",
        "E This seemed like an unnecessary stage.", "F This involved selecting a new ingredient.",
    ]
    g8 = group(
        "l3-g4", "Questions 27–30",
        "Complete the flow-chart below. Choose FOUR answers from the box and write the correct letter, A–F, next to Questions 27–30.",
        list(range(27, 31)), layout="flow", shared=stages, body=[
            "# Student project: developing a new food product",
            "## Initial aim",
            "{{27}}",
            "## Literature review",
            "{{28}}",
            "## Product development",
            "{{29}}",
            "## Product production",
            "{{30}}",
        ],
    )
    qs3 += [question(n, "l3-g4", f"Flow-chart stage {n}", "select") for n in range(27, 31)]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Food safety and a student project",
        "context": "Two students, Nadia and Fergus, discuss sessions on food safety and a project developing a new food product.",
        "groups": [g5, g6, g7, g8], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g9 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Challenges facing the cruise ship industry",
            "## Problems with overtourism",
            "• {{31}} is one of the worst problems.",
            "• A tourist {{32}} is being introduced in some cities to reduce numbers, e.g. Barcelona.",
            "• Bruges: action was taken to limit day trips from the nearby port because the city was becoming a 'theme park' (e.g. many shops were only stocking {{33}} and souvenirs).",
            "• Dubrovnik: limits the number of tourists by managing the {{34}} of cruise ship arrivals.",
            "## Problems of perception",
            "• Cruises are generally associated with the elderly.",
            "• There is an assumption about the {{35}} of cruises.",
            "• People think there may be too many {{36}}.",
            "## Solutions",
            "Cruise lines are attracting younger customers by:",
            "• becoming more sustainable e.g. using hybrid engines.",
            "• having a wide range of activities e.g. boxing, {{37}} and well-being programmes.",
            "• offering a diverse selection of food including {{38}} options.",
            "• providing reliable {{39}}.",
            "• improving marketing on social media with high quality {{40}}.",
        ],
    )
    qs4 = [question(n, "l4-g1", f"Cruise industry notes {n}") for n in range(31, 41)]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Challenges facing the cruise ship industry",
        "context": "A lecture about the challenges facing the cruise ship industry.",
        "groups": [g9], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 --------------------------------------------------------------
    p1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–5",
        "Complete the table below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(1, 6)), layout="form", body=[
            "# Research into sleep and dreaming",
            "• Humans — experience REM sleep and non-REM sleep; in REM sleep, the eyes and muscles move",
            "• {{1}} — similar brain patterns were observed when active and sleeping — indicative of dreaming",
            "• Pigeons — when sleeping, pigeons displayed activity in parts of the brain that deal with {{2}} input — may have been dreaming of flying",
            "• Whales and dolphins — still have {{3}} their brain awake when they sleep — their dreams are probably not very {{5}}",
            "• Whales and dolphins — don't experience REM sleep, as this could affect their sensitivity to {{4}}",
        ],
    )
    qs1 = [question(n, "r1-g1", f"Sleep research table {n}") for n in range(1, 6)]

    g2 = group(
        "r1-g2", "Questions 6–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(6, 14)),
    )
    statements = [
        "Dreaming about past experiences helps us to create lasting memories of them.",
        "It is now possible to tell what type of dream a dog is having.",
        "David Scheel's documentary was influential on other research into the sleeping patterns of octopuses.",
        "While it was asleep, the octopus called Costello reacted as if it was hunting.",
        "Scheel believes more research into octopuses' dreams should be carried out.",
        "We may soon be able to share the dreams of other human beings.",
        "Hearing may be an important part of the dreams of some animals.",
        "Interest in the reasons why humans dream has increased greatly in recent times.",
    ]
    qs1 += [question(n, "r1-g2", text, "tfng") for n, text in zip(range(6, 14), statements)]
    apply_keys(qs1, keys["reading"], "r1")
    p1["groups"] = [g1, g2]
    p1["questions"] = qs1
    reading.append(p1)

    # Passage 2 --------------------------------------------------------------
    p2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–19",
        "Reading Passage 2 has seven paragraphs, A–G. Which paragraph contains the following information? Write the correct letter, A–G, in boxes 14–19 on your answer sheet.",
        list(range(14, 20)), layout="match", shared=["A", "B", "C", "D", "E", "F", "G"],
    )
    info = [
        "a mention of the uncertainty regarding the purpose of certain objects",
        "the likelihood that a climatic factor increased the problems Mapungubwe faced",
        "a mention of the location where members of the king's family are thought to have lived",
        "a reference to people who brought goods by ship",
        "an estimate of the size to which the Mapungubwe community grew",
        "a mention of agricultural produce being exchanged for other items",
    ]
    qs2 = [question(n, "r2-g1", text, "match") for n, text in zip(range(14, 20), info)]

    gold = ["Not everyone in Mapungubwe used gold as a form of payment.",
            "Items of gold were placed close to where Mapungubwe kings were buried.",
            "The most valuable item discovered in Mapungubwe was a sceptre made of gold.",
            "The way gold was decorated in Mapungubwe was also practised in another kingdom.",
            "Working with gold was a respected occupation in the Mapungubwe community."]
    g4 = group(
        "r2-g2", "Questions 20 and 21",
        "Choose TWO letters, A–E. The archaeological record reveals information about gold and the kingdom of Mapungubwe. Which TWO pieces of information are mentioned by the writer?",
        [20, 21],
    )
    qs2 += [
        question(20, "r2-g2", "The first piece of information mentioned", "mcq", gold),
        question(21, "r2-g2", "The second piece of information mentioned", "mcq", gold),
    ]

    g5 = group(
        "r2-g3", "Questions 22–26",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(22, 27)), layout="summary", body=[
            "# Archaeological discoveries",
            "The Mapungubwe community's {{22}} is indicated by the amount of professionally made pottery discovered at the site. Many of these objects, such as beakers and bowls, are highly decorated and have been marked with stamps. Other finds include round ceramic objects, {{23}} and figures of various animals, as well as models of people with stretched {{24}}. It is possible that these had a role in ceremonies to honour {{25}}. In addition, pieces of {{26}} made from a local metal have been found at the site.",
        ],
    )
    qs2 += [question(n, "r2-g3", f"Archaeological discoveries summary {n}") for n in range(22, 27)]
    apply_keys(qs2, keys["reading"], "r2")
    p2["groups"] = [g3, g4, g5]
    p2["questions"] = qs2
    reading.append(p2)

    # Passage 3 --------------------------------------------------------------
    p3 = passage(3, passages["3"])
    g6 = group(
        "r3-g1", "Questions 27–29",
        "Choose the correct letter, A, B, C or D.",
        list(range(27, 30)),
    )
    mcq = [
        (27, "What is the writer doing in the first paragraph?",
         ["predicting the future impact of AI", "describing a public perception of AI",
          "outlining some possible benefits of AI", "highlighting the breadth of the influence of AI"]),
        (28, "When discussing AI solutionism in the second paragraph, the writer",
         ["points out a risk involved.", "specifies its probable origins.",
          "mentions its chief supporters.", "weighs up some pros and cons."]),
        (29, "In the fourth paragraph, the writer suggests that many politicians may",
         ["have failed to appreciate the true potential of AI initiatives.",
          "have misunderstood the function of the machine-learning sector.",
          "be unaware of the challenges of implementing national AI initiatives.",
          "be too keen to enter the race to dominate the machine-learning sector."]),
    ]
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in mcq]

    words = ["A reliability", "B funding", "C skills", "D prejudices", "E computers",
             "F equality", "G framework", "H confidentiality", "I approval"]
    g7 = group(
        "r3-g2", "Questions 30–35",
        "Complete the summary using the list of words, A–I, below.",
        list(range(30, 36)), layout="summary", shared=words, body=[
            "# AI in government, medicine and the law",
            "Neural networks are a promising area of AI technology for governments. However, many politicians overestimate their capabilities, believing that the mere addition of a neural network will produce solutions and promote {{30}}.",
            "Most public sector organisations have not set up the necessary {{31}} to manage the huge amount of data required to enable AI to function. Complex bureaucracy is another issue, as each person involved needs {{32}} to access the relevant data, which is often spread across different departments. But the main problem is that few public sector employees have the {{33}} to take full advantage of machine intelligence.",
            "The medical profession experimented with an AI programme, but their experts had little faith in its {{34}}, and the programme was abandoned. US courts also abandoned the use of algorithms when it was found that these reflected and magnified the existing {{35}} within the legal profession.",
        ],
    )
    qs3 += [question(n, "r3-g2", f"AI summary {n}", "select") for n in range(30, 36)]

    g8 = group(
        "r3-g3", "Questions 36–39",
        "Do the following statements agree with the claims of the writer in Reading Passage 3? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(36, 40)),
    )
    yn = [
        "Stuart Russell's proposals regarding the use of AI are impractical.",
        "Rodney Brooks' view has attracted unfair criticism from supporters of AI.",
        "Nowadays, the need to protect AI systems is always taken into account when they are set up.",
        "In order to benefit from AI and minimise the harms, we have to explore people's concerns about its use.",
    ]
    qs3 += [question(n, "r3-g3", text, "ynng") for n, text in zip(range(36, 40), yn)]

    g9 = group(
        "r3-g4", "Question 40",
        "Choose the correct letter, A, B, C or D.",
        [40],
    )
    qs3 += [question(40, "r3-g4", "What would be a suitable subtitle for Reading Passage 3?", "mcq", [
        "How to make the most of what AI has to offer",
        "Why AI may not be the answer to our problems",
        "Why governments should not invest in AI systems",
        "How AI could improve the efficiency of the public sector",
    ])]
    apply_keys(qs3, keys["reading"], "r3")
    p3["groups"] = [g6, g7, g8, g9]
    p3["questions"] = qs3
    reading.append(p3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The plans below show a college café before it was redesigned and how it looks now.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/cambridge21/test2-writing-task1.jpg",
            "figureAlt": "Two floor plans of a college cafe, labelled 'Cafe before redesign' and 'Cafe today', showing the kitchen, serving area, staff dining rooms, tables and chairs, toilets and outdoor seating.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "Some people say that in the digital age, theatres and cinemas are no longer important as people can watch all the entertainment they want online. Others argue that theatres and cinemas are still important both economically and culturally.\n\nDiscuss both these views and give your own opinion.",
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
            "description": "The examiner asks you about yourself, your home, work or studies and other familiar topics.",
            "questions": [
                {"id": "s1", "text": "How well do you know the capital city of your country?"},
                {"id": "s2", "text": "Do you think cities are exciting places to live?"},
                {"id": "s3", "text": "Why do some people dislike living in a city?"},
                {"id": "s4", "text": "If you could visit any city in the world, where would you go?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a time when you read or heard something that you thought was not true.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a time when you read or heard something that you thought was not true.",
                "bullets": ["where you read/heard this", "what you read/heard", "why you thought it was not true"],
                "rounding": "and explain how you felt about reading/hearing this thing that you thought was not true.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: honesty and children; honesty and advertising.",
            "questions": [
                {"id": "s5", "text": "Honesty and children. Do you think children are more honest than adults?"},
                {"id": "s6", "text": "Why do adults tell children it's important to be honest?"},
                {"id": "s7", "text": "Do you think there are sometimes good reasons for adults not to tell children the truth?"},
                {"id": "s8", "text": "Honesty and advertising. Are there any claims in advertisements that are sometimes not true?"},
                {"id": "s9", "text": "Why do people still buy things even when they know advertisements aren't completely accurate?"},
                {"id": "s10", "text": "Do you think advertisements that are dishonest should be banned?"},
            ],
        },
    ]

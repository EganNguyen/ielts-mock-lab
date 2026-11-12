"""Cambridge IELTS 21 — Academic Test 4."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "cambridge21-test4",
        "title": "Cambridge IELTS 21 · Academic Test 4",
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
        "Complete the form below. Write ONE WORD ONLY for each answer.",
        list(range(1, 11)), layout="form", body=[
            "# Survey about shopping in Broadbeach",
            "Name: Martyn {{1}}",
            "## Today's journey to Broadbeach town centre",
            "• used his {{2}}",
            "## Purpose of today's trip",
            "• has visited the {{3}}",
            "• looking for a new {{4}}",
            "• collecting {{5}} (after repair)",
            "## Preferred day for shopping",
            "• {{6}}",
            "## Opinions about shopping in the town centre",
            "• Finds the service in shops is excellent",
            "• Thinks there are too many places selling {{7}}",
            "• Would like more places to buy {{8}}",
            "## Opinions about new out-of-town Shopping Centre",
            "• Likes the {{9}} best",
            "• Believes the {{10}} is unnecessary",
        ],
    )
    qs = [question(n, "l1-g1", f"Shopping survey form {n}") for n in range(1, 11)]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "A shopping survey in Broadbeach",
        "context": "A conversation between a researcher and a man about shopping in Broadbeach.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    areas = ["the Digital Marketing Centre", "the TalkCon Zone", "the Breakout area",
             "the Business Village", "the Business Connections Zone"]
    g2 = group(
        "l2-g1", "Questions 11 and 12",
        "Choose TWO letters, A–E. In which TWO areas of the business exhibition did James Craig promote his company last year?",
        [11, 12],
    )
    qs2 = [
        question(11, "l2-g1", "The first area", "mcq", areas),
        question(12, "l2-g1", "The second area", "mcq", areas),
    ]
    discounts = ["They are available to all members of exhibiting companies.",
                 "They can be used for both food and clothing.",
                 "They only apply if people spend at least £400.",
                 "They can be used by family members.",
                 "The percentage saved is always the same."]
    g3 = group(
        "l2-g2", "Questions 13 and 14",
        "Choose TWO letters, A–E. Which TWO facts are given about discounts on popular brands available to exhibitors?",
        [13, 14],
    )
    qs2 += [
        question(13, "l2-g2", "The first fact", "mcq", discounts),
        question(14, "l2-g2", "The second fact", "mcq", discounts),
    ]
    topics = ["A Supporting job seekers", "B Dealing with personal problems",
              "C Effects of an unexpectedly rapid expansion", "D A global range of business experiences",
              "E Coping with financial set-backs", "F Developing a company in response to changing markets",
              "G Combining business success with contributions to charities"]
    g4 = group(
        "l2-g3", "Questions 15–20",
        "Which topic will each of the following speakers focus on? Choose SIX answers from the box and write the correct letter, A–G, next to Questions 15–20.",
        list(range(15, 21)), layout="match", shared=topics,
    )
    speakers = [(15, "Jim Clowrie"), (16, "David France"), (17, "Oliver Stanton"),
                (18, "Francesca Heptonstall"), (19, "Salman Khan"), (20, "Annie Craven")]
    qs2 += [question(n, "l2-g3", name, "match") for n, name in speakers]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "A business exhibition",
        "context": "A talk about a business exhibition and the speakers who will present at it.",
        "groups": [g2, g3, g4], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    g5 = group("l3-g1", "Questions 21–23", "Choose the correct letter, A, B or C.", list(range(21, 24)))
    qs3 = [
        question(21, "l3-g1", "Which aspect of their presentation are Mia and Leo both concerned about?", "mcq",
                 ["meeting the deadline", "finding suitable examples", "including original ideas"]),
        question(22, "l3-g1", "The students decide to focus their assignment on housing for", "mcq",
                 ["family groups.", "old people.", "single people."]),
        question(23, "l3-g1", "The students agree that demand for accommodation in urban areas should be met by", "mcq",
                 ["repurposing offices and factories.", "constructing tall buildings.",
                  "developing creative ideas for smaller homes."]),
    ]
    opinions = [
        "A This could cause unnecessary anxiety.", "B This would be especially beneficial for city residents.",
        "C This would be challenging for young people.", "D This would have environmental benefits.",
        "E This could encourage creativity.", "F This could lead to social problems.",
        "G This could enable retired people to share a project.",
        "H This would help some people but cause problems for others.",
        "I This would suit both existing and new members of a household.",
    ]
    g6 = group(
        "l3-g2", "Questions 24–30",
        "What opinion is given about each of the following developments? Choose SEVEN answers from the box and write the correct letter, A–I, next to Questions 24–30.",
        list(range(24, 31)), layout="match", shared=opinions,
    )
    developments = [(24, "use of roof space for gardens"), (25, "shared working spaces"),
                    (26, "moveable internal walls"), (27, "smart mirrors in bathrooms"),
                    (28, "bike sheds with charging points"), (29, "restriction of cars to certain areas"),
                    (30, "communal vegetable plots")]
    qs3 += [question(n, "l3-g2", name, "match") for n, name in developments]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "A presentation on houses of the future",
        "context": "Two students, Mia and Leo, discuss their presentation on houses of the future.",
        "groups": [g5, g6], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g7 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Music therapy for surgical patients",
            "## Background",
            "• Surgery impacts patients because they may experience discomfort or unwelcome changes to their {{31}}.",
            "• Current post-surgical strategies focus mainly on pain relief.",
            "## Recent research",
            "• A study reviewed data from about 100 {{32}} and found that listening to music",
            "  – improved hospital patients' sense of wellbeing.",
            "  – reduced the length of their stay.",
            "• The patients in the study all listened to music with a {{33}} effect.",
            "• The music was mostly played through music {{34}}.",
            "• Patients reported an absence or low levels of {{35}}.",
            "• Medical records confirmed that patients who were played music in hospital needed less {{36}} than those who weren't played music.",
            "• The best results were achieved when patients were played music while they were {{37}}.",
            "• The study concluded that playing music was effective because it served as a {{38}}.",
            "• The researchers recommend playing either music or sounds from {{39}} to all surgical patients.",
            "• A future study will investigate the best {{40}} for the music.",
        ],
    )
    qs4 = [question(n, "l4-g1", f"Music therapy notes {n}") for n in range(31, 41)]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Music therapy for surgical patients",
        "context": "A lecture about music therapy for surgical patients.",
        "groups": [g7], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 --------------------------------------------------------------
    p1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–7",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(1, 8)),
    )
    statements = [
        "Water hyacinth was introduced as a decorative plant in east Africa.",
        "Fishermen took some water hyacinth plants to Lake Victoria.",
        "It is now difficult to force boats through the thick water hyacinth on Lake Victoria.",
        "Chemicals produced by the water hyacinth plants are affecting the numbers of fish in Lake Victoria.",
        "Cooking with charcoal has been proved to be even worse for people's health than cooking with wood.",
        "People found it impossible to remove much water hyacinth from Lake Victoria.",
        "Scientists started investigating the possibility of using water hyacinth to generate biogas in the last century.",
    ]
    qs1 = [question(n, "r1-g1", text, "tfng") for n, text in zip(range(1, 8), statements)]

    g2 = group(
        "r1-g2", "Questions 8–10",
        "Complete the flow-chart below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
        list(range(8, 11)), layout="flow", body=[
            "# Generating biogas for domestic use in Dunga",
            "First, place water hyacinth together with some {{8}} into a digester",
            "↓",
            "Leave the mixture until the {{9}} is completed",
            "↓",
            "Capture the gas emitted by the digester and use {{10}} to transport it to individual homes",
            "↓",
            "Then use the gas for cooking as well as making water fit for human consumption",
        ],
    )
    qs1 += [question(n, "r1-g2", f"Biogas flow-chart {n}") for n in range(8, 11)]

    g3 = group(
        "r1-g3", "Questions 11–13",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(11, 14)), layout="notes", body=[
            "# Cooking with biogas in Dunga",
            "## Benefits for the women in the village of cooking with biogas",
            "• no need for them to spend so much {{11}} collecting fuel",
            "• they can focus on different tasks that bring in {{12}}",
            "• they are less likely to experience certain diseases connected to burning wood",
            "## Drawbacks of changing to biogas",
            "• the {{13}} of the digesters is beyond the reach of most villages",
        ],
    )
    qs1 += [question(n, "r1-g3", f"Biogas notes {n}") for n in range(11, 14)]
    apply_keys(qs1, keys["reading"], "r1")
    p1["groups"] = [g1, g2, g3]
    p1["questions"] = qs1
    reading.append(p1)

    # Passage 2 --------------------------------------------------------------
    p2 = passage(2, passages["2"])
    words = ["A basic outlook", "B employment opportunities", "C wealthy visitors", "D distant country",
             "E primary objective", "F similar advantages", "G thriving economy", "H nearby district",
             "I dense population", "J new immigrants"]
    g4 = group(
        "r2-g1", "Questions 14–19",
        "Complete the summary using the list of words, A–J, below.",
        list(range(14, 20)), layout="summary", shared=words, body=[
            "# Multilingualism in Delhi",
            "The city of Delhi has a {{14}} and as you walk through its streets you hear people speaking a variety of languages. Some of them have spent their entire life in Delhi, while others are {{15}} Whether they have come from a {{16}} or have travelled from the other side of India, they have all come in search of things such as improved {{17}}.",
            "A team of researchers led by Professor Ianthi Tsimpli of Cambridge University is collecting data on primary-age schoolchildren in Delhi and other Indian cities. The {{18}} of the research is to discover why multilingual Indian schoolchildren do not experience {{19}} to those that multilingual schoolchildren in Europe experience.",
        ],
    )
    qs2 = [question(n, "r2-g1", f"Multilingualism summary {n}", "select") for n in range(14, 20)]

    g5 = group(
        "r2-g2", "Questions 20–23",
        "Do the following statements agree with the claims of the writer in Reading Passage 2? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(20, 24)),
    )
    yn = [
        "Ten-year-old Indian schoolchildren tend to perform better in literacy tests than in numeracy tests.",
        "Tsimpli had problems convincing some female students to take part in the study.",
        "Tsimpli and her team wanted to know if there is a connection between poor academic performance and being taught in an unfamiliar language.",
        "The researchers have decided against investigating the impact teaching methodology may have on learning outcomes.",
    ]
    qs2 += [question(n, "r2-g2", text, "ynng") for n, text in zip(range(20, 24), yn)]

    g6 = group("r2-g3", "Questions 24–26", "Choose the correct letter, A, B, C or D.", list(range(24, 27)))
    qs2 += [
        question(24, "r2-g3", "What point does the writer make about primary schools in India in the sixth paragraph?", "mcq",
                 ["Exposure to English outside of school is of limited benefit.",
                  "Children learn English more easily when they are well motivated.",
                  "Poor children may be disadvantaged further by being instructed in English.",
                  "There is little consistency across schools with regard to instruction in English."]),
        question(25, "r2-g3", "What is Tsimpli suggesting when she uses the phrase 'that ship has sailed'?", "mcq",
                 ["The findings of the report may be of little help to some Indian schoolchildren.",
                  "Instruction in English could be better adapted to the needs of schoolchildren.",
                  "Schools have had limited success in teaching English as a separate subject.",
                  "It is too late to remove English completely as a language of instruction in schools."]),
        question(26, "r2-g3", "In the eighth paragraph, what do we learn has surprised researchers?", "mcq",
                 ["Boys and girls from low socio-economic groups have similar general intelligence levels.",
                  "The age at which children move into a slum does not affect their academic performance.",
                  "Slum children and children from other urban poor backgrounds have similar life experiences.",
                  "The literacy and numeracy skills of slum children are not lower than those of children from other urban poor backgrounds."]),
    ]
    apply_keys(qs2, keys["reading"], "r2")
    p2["groups"] = [g4, g5, g6]
    p2["questions"] = qs2
    reading.append(p2)

    # Passage 3 --------------------------------------------------------------
    p3 = passage(3, passages["3"])
    words = ["A educational use", "B rare materials", "C inferior makes", "D product exchange",
             "E necessary skills", "F international markets", "G challenging task", "H memorable object",
             "I internet purchase", "J numerous problems"]
    g7 = group(
        "r3-g1", "Questions 27–32",
        "Complete the summary using the list of words, A–J, below.",
        list(range(27, 33)), layout="summary", shared=words, body=[
            "# A birthday gift",
            "Peter Bellerby's plan to give his father a globe for his birthday was an unexpectedly {{27}} for which he had to overcome {{28}}.",
            "He soon learnt that a straightforward {{29}} would not be possible. Some {{30}} that had been intended for {{31}} were available, as were some expensive antique globes, but these were beyond his budget. He even travelled to places where people might still have the {{32}}, but Bellerby could not find what he wanted.",
        ],
    )
    qs3 = [question(n, "r3-g1", f"Globemakers summary {n}", "select") for n in range(27, 33)]

    g8 = group(
        "r3-g2", "Questions 33–36",
        "Do the following statements agree with the claims of the writer in Reading Passage 3? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(33, 37)),
    )
    yn = [
        "The assumption today that people in the past knew very little about geography is correct.",
        "Plato was criticised for saying the world was shaped like a leather ball.",
        "The globe made by Crates of Mallus was an accurate representation of the known world.",
        "Bellerby assumed he would have few problems locating a well-made globe.",
    ]
    qs3 += [question(n, "r3-g2", text, "ynng") for n, text in zip(range(33, 37), yn)]

    g9 = group("r3-g3", "Questions 37–40", "Choose the correct letter, A, B, C or D.", list(range(37, 41)))
    qs3 += [
        question(37, "r3-g3", "When Bellerby had to attach the gores to the globe surface,", "mcq",
                 ["he decided it was best to work quickly.", "he became aware of an unexpected issue.",
                  "he was worried about the quality of his materials.", "he nearly gave up the whole project."]),
        question(38, "r3-g3", "The reviewer mentions other globe makers of the past because", "mcq",
                 ["Bellerby was particularly inspired by them.", "their achievements are not widely known.",
                  "Bellerby had something in common with each of them.", "their difficulties could have been avoided."]),
        question(39, "r3-g3", "What point is made about Bellerby in the seventh paragraph?", "mcq",
                 ["He had long working relationships with numerous craftsmen.",
                  "He understands the lack of interest in traditional crafts.",
                  "He appreciates the importance of careful planning.",
                  "He regrets the loss of many globe-making skills."]),
        question(40, "r3-g3", "What does the reviewer say about Bellerby's book in the final paragraph?", "mcq",
                 ["It does not tell you how to create a profitable business.",
                  "It overlooks some important mapmakers.", "It fails to discuss the future of globe-making.",
                  "It does not give enough details about individual customers."]),
    ]
    apply_keys(qs3, keys["reading"], "r3")
    p3["groups"] = [g7, g8, g9]
    p3["questions"] = qs3
    reading.append(p3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The chart and table below show the results of a survey of library users at a university.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/cambridge21/test4-writing-task1.jpg",
            "figureAlt": "Pie chart showing categories of library users and a table showing library user satisfaction percentages for opening hours, staff helpfulness, books, journals and wi-fi.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "Some people argue that primary schools focus too much on formal learning.\n\nTo what extent do you agree with this opinion?\n\nHow important do you think it is for children to play as well as learn in the primary school classroom?",
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
                {"id": "s1", "text": "When do you usually eat bread?"},
                {"id": "s2", "text": "How important is bread in your culture?"},
                {"id": "s3", "text": "Have you tried any kinds of bread from other countries?"},
                {"id": "s4", "text": "Would you be interested in learning how to make bread?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a person you know who is very competitive.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a person you know who is very competitive.",
                "bullets": ["who this person is", "what this person is competitive about",
                            "how successful this person is"],
                "rounding": "and explain why you think this person is so competitive.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: competitions; being competitive in sports.",
            "questions": [
                {"id": "s5", "text": "Competitions. What kinds of competitions do people like to enter in your country?"},
                {"id": "s6", "text": "What do you think is the best kind of prize to win in a competition?"},
                {"id": "s7", "text": "Why do people like watching quiz shows and other competitions on TV?"},
                {"id": "s8", "text": "Being competitive in sports. How important is it to be very competitive at sport?"},
                {"id": "s9", "text": "Do you think sportspeople perform better when they play against competitors who are stronger than they are?"},
                {"id": "s10", "text": "Why do some people think that taking part in sport is more important than winning?"},
            ],
        },
    ]

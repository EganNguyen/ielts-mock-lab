"""IELTS 20 Academic — Test 4."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts20-test4",
        "title": "IELTS 20 · Academic Test 4",
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
        "Complete the notes below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 11)), layout="notes", body=[
            "# Advice on family visit",
            "## Accommodation",
            "• {{1}} Hotel on George Street",
            "• cost of family room per night: £{{2}} (approx.)",
            "## Recommended trips",
            "• a {{3}} tour of the city centre (starts in Carlton Square)",
            "• a trip by {{4}} to the old fort",
            "## Science Museum",
            "• best day to visit: {{5}}",
            "• see the exhibition about {{6}}, which opens soon",
            "## Food",
            "• Clacton Market: good for {{7}} food; need to have lunch before {{8}} p.m.",
            "## Theatre tickets",
            "• save up to {{9}}% on ticket prices at bargaintickets.com",
            "## Free activities",
            "• Blakewell Gardens: Roots Music Festival",
            "• climb Telegraph Hill to see a view of the {{10}}",
        ])
    qs = [question(n, "l1-g1", prompt) for n, prompt in [
        (1, "Name of the hotel on George Street"),
        (2, "Cost of a family room per night"),
        (3, "Type of tour of the city centre"),
        (4, "How to travel to the old fort"),
        (5, "Best day to visit the Science Museum"),
        (6, "Subject of the exhibition opening soon"),
        (7, "Type of food Clacton Market is good for"),
        (8, "Time by which to have lunch"),
        (9, "Maximum percentage saved on theatre tickets"),
        (10, "What can be seen from Telegraph Hill"),
    ]]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Advice on a family visit",
        "context": "A man asks a friend for advice about where to take his visiting family.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    children = [
        "Children can get their photo taken with a football player.",
        "There is a competition for children today.",
        "Parents must stay with their children at all times.",
        "Children will need sunhats and drinks.",
        "The cafe has a special offer on meals for children.",
    ]
    g2 = group(
        "l2-g1", "Questions 11 and 12",
        "Choose TWO letters, A–E. Which TWO things does the speaker say about visiting the football stadium with children?",
        [11, 12],
    )
    qs2 = [
        question(11, "l2-g1", "First thing the speaker says about visiting with children", "mcq", children),
        question(12, "l2-g1", "Second thing the speaker says about visiting with children", "mcq", children),
    ]
    features = [
        "VIP tour", "360 cinema experience", "audio guide",
        "dressing room tour", "tours in other languages",
    ]
    g3 = group(
        "l2-g2", "Questions 13 and 14",
        "Choose TWO letters, A–E. Which TWO features of the stadium tour are new this year?",
        [13, 14],
    )
    qs2 += [
        question(13, "l2-g2", "First new feature of the stadium tour", "mcq", features),
        question(14, "l2-g2", "Second new feature of the stadium tour", "mcq", features),
    ]
    events = [
        "A The introduction of pay for the players",
        "B a change to the design of the goal",
        "C the first use of lights for matches",
        "D the introduction of goalkeepers",
        "E the first international match",
        "F two changes to the rules of the game",
        "G the introduction of a fee for spectators",
        "H an agreement on the length of a game",
    ]
    g4 = group(
        "l2-g3", "Questions 15–20",
        "Which event in the history of football in the UK took place in each of the following years? Choose SIX answers from the box and write the correct letter, A–H.",
        list(range(15, 21)), layout="match", shared=events,
    )
    qs2 += [question(n, "l2-g3", f"{year}", "match") for n, year in [
        (15, "1870"), (16, "1874"), (17, "1875"),
        (18, "1877"), (19, "1878"), (20, "1880"),
    ]]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "A tour of the football stadium",
        "context": "A guide gives a tour group information about visiting the stadium and its history.",
        "groups": [g2, g3, g4], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    benefits = [
        "improved fine motor skills", "improved memory", "improved concentration",
        "improved imagination", "improved spatial awareness",
    ]
    g5 = group(
        "l3-g1", "Questions 21 and 22",
        "Choose TWO letters, A–E. Which TWO benefits for children of learning to write did both students find surprising?",
        [21, 22],
    )
    qs3 = [
        question(21, "l3-g1", "First surprising benefit of learning to write", "mcq", benefits),
        question(22, "l3-g1", "Second surprising benefit of learning to write", "mcq", benefits),
    ]
    problems = [
        "not spacing letters correctly", "not writing in a straight line",
        "applying too much pressure when writing", "confusing letter shapes",
        "writing very slowly",
    ]
    g6 = group(
        "l3-g2", "Questions 23 and 24",
        "Choose TWO letters, A–E. For children with dyspraxia, which TWO problems with handwriting do the students think are easiest to correct?",
        [23, 24],
    )
    qs3 += [
        question(23, "l3-g2", "First handwriting problem easiest to correct", "mcq", problems),
        question(24, "l3-g2", "Second handwriting problem easiest to correct", "mcq", problems),
    ]
    g7 = group(
        "l3-g3", "Questions 25–30", "Choose the correct letter, A, B or C.",
        list(range(25, 31)),
    )
    mcq = [
        (25, "What does the woman say about using laptops to teach writing to children with dyslexia?",
         ["Children often lack motivation to learn that way.",
          "Children become fluent relatively quickly.",
          "Children react more positively if they make a mistake."]),
        (26, "When discussing whether to teach cursive or print writing, the woman thinks that",
         ["cursive writing disadvantages a certain group of children.",
          "print writing is associated with lower academic performance.",
          "most teachers in the UK prefer a traditional approach to handwriting."]),
        (27, "According to the students, what impact does poor handwriting have on exam performance?",
         ["There is evidence to suggest grades are affected by poor handwriting.",
          "Neat handwriting is less important now than it used to be.",
          "Candidates write more slowly and produce shorter answers."]),
        (28, "What prediction does the man make about the future of handwriting?",
         ["Touch typing will be taught before writing by hand.",
          "Children will continue to learn to write by hand.",
          "People will dislike handwriting on digital devices."]),
        (29, "The woman is concerned that relying on digital devices has made it difficult for her to",
         ["take detailed notes.", "spell and punctuate.", "read old documents."]),
        (30, "How do the students feel about their own handwriting?",
         ["concerned they are unable to write quickly",
          "embarrassed by comments made about it",
          "regretful that they have lost the habit"]),
    ]
    qs3 += [question(n, "l3-g3", prompt, "mcq", options) for n, prompt, options in mcq]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Teaching handwriting",
        "context": "Two education students discuss an assignment on teaching handwriting to children.",
        "groups": [g5, g6, g7], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g8 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Research in the area around the Chembe Bird Sanctuary",
            "## The importance of birds of prey to the local communities",
            "• They destroy {{31}} and other rodents.",
            "• They help to prevent farmers from being bitten by {{32}}.",
            "• They have been an important part of the local culture for many years.",
            "• They now support the economy by encouraging {{33}} in the area.",
            "## Falling numbers of birds of prey",
            "• The birds may be accidentally killed by {{34}} when they are hunting or sleeping.",
            "• They may be electrocuted by power lines, especially when there is a lot of {{35}}.",
            "• Local farmers may illegally shoot them or {{36}} them.",
            "## Ways of protecting chickens from birds of prey",
            "• clearing away vegetation from the area (unhelpful)",
            "• providing a {{37}} for chickens (expensive)",
            "• frightening birds of prey by keeping a {{38}} or making a {{39}}, e.g. with metal objects",
            "• a {{40}} of methods is usually most effective.",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "Rodents destroyed by birds of prey"),
        (32, "Animal whose bite birds of prey help prevent"),
        (33, "What birds of prey encourage in the area"),
        (34, "Cause of accidental deaths while hunting or sleeping"),
        (35, "Weather condition that increases electrocution risk"),
        (36, "What farmers may illegally do to the birds besides shooting"),
        (37, "Structure provided for chickens (expensive option)"),
        (38, "Animal kept to frighten birds of prey"),
        (39, "Type of object made to frighten birds of prey"),
        (40, "What approach to protection is most effective"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Birds of prey and farming",
        "context": "A lecture about research into conflicts between birds of prey and farmers in Zambia.",
        "groups": [g8], "questions": qs4, "transcript": transcripts["4"],
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
            "# The life and work of Georgia O'Keeffe",
            "• studied art, then worked as a {{1}} in various places in the USA",
            "• created drawings using {{2}}, which were exhibited in New York City",
            "• moved to New York and became famous for her paintings of the city's {{3}}",
            "• produced a series of innovative close-up paintings of {{4}}",
            "• went to New Mexico and was initially inspired to paint the many {{5}} that could be found there",
            "• continued to paint various features that together formed the dramatic {{6}} of New Mexico for over forty years",
            "• travelled widely by plane in later years, and painted pictures of clouds and {{7}} seen from above",
        ])
    qs = [question(n, "r1-g1", f"Georgia O'Keeffe notes {n}") for n in range(1, 8)]
    g2 = group(
        "r1-g2", "Questions 8–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(8, 14)),
    )
    qs += [
        question(8, "r1-g2", "Georgia O'Keeffe's style was greatly influenced by the changing fashions in art over the seven decades of her career.", "tfng"),
        question(9, "r1-g2", "When O'Keeffe finished high school, she had already made her mind up about the career that she wanted.", "tfng"),
        question(10, "r1-g2", "Alfred Stieglitz first discovered O'Keeffe's work when she sent some abstract drawings to his gallery in New York City.", "tfng"),
        question(11, "r1-g2", "O'Keeffe was the subject of Stieglitz's photographic work for many years.", "tfng"),
        question(12, "r1-g2", "O'Keeffe's paintings of the patio of her house in Abiquiú were among the artist's favourite works.", "tfng"),
        question(13, "r1-g2", "O'Keeffe produced a greater quantity of work during the 1950s to 1970s than at any other time in her life.", "tfng"),
    ]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 --------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–17",
        "Reading Passage 2 has six paragraphs, A–F. Which paragraph contains the following information?",
        list(range(14, 18)), layout="match", shared=list("ABCDEF"),
    )
    qs2 = [
        question(14, "r2-g1", "how a type of plant functions as a natural protection for coastlines", "match"),
        question(15, "r2-g1", "a prediction about how long it could take to stop noticing the effects of climate change", "match"),
        question(16, "r2-g1", "a reference to the fact that a solution is particularly cost-effective", "match"),
        question(17, "r2-g1", "a mention of a technology used to locate areas most in need of intervention", "match"),
    ]
    g4 = group(
        "r2-g2", "Questions 18–22",
        "Complete the sentences below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(18, 23)), layout="summary", body=[
            "The stormwater-management programme in Miami Beach has involved the installation of efficient {{18}}.",
            "The construction of {{19}} was the first stage of a project to ensure the success of mangroves in Indonesia.",
            "As a response to rising floodwaters in the Mekong Delta, a not-for-profit organisation has been building houses that can {{20}}.",
            "Rising sea levels in Bangladesh have made it necessary to introduce various {{21}} that are suitable for areas of high salt content.",
            "A project in LA has increased the number of {{22}} on the city's streets.",
        ])
    qs2 += [question(n, "r2-g2", f"Climate adaptation sentence {n}") for n in range(18, 23)]
    people = [
        "A Yanira Pineda", "B Susanna Toi", "C Elizabeth English",
        "D Raisa Chowdhury", "E Greg Spotts",
    ]
    g5 = group(
        "r2-g3", "Questions 23–26",
        "Look at the following statements and the list of people below. Match each statement with the correct person, A–E.",
        list(range(23, 27)), layout="match", shared=people,
    )
    qs2 += [
        question(23, "r2-g3", "It is essential to adopt strategies which involve and help residents of the region.", "match"),
        question(24, "r2-g3", "Interventions which reduce heat are absolutely vital for our survival in this location.", "match"),
        question(25, "r2-g3", "More work will need to be done in future decades to deal with the impact of rising water levels.", "match"),
        question(26, "r2-g3", "The number of locations requiring action to adapt to flooding has grown in recent years.", "match"),
    ]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 --------------------------------------------------------------
    r3 = passage(3, passages["3"])
    g6 = group(
        "r3-g1", "Questions 27–31",
        "Reading Passage 3 has seven paragraphs, A–G. Which paragraph contains the following information? NB You may use any letter more than once.",
        list(range(27, 32)), layout="match", shared=list("ABCDEFG"),
    )
    qs3 = [
        question(27, "r3-g1", "an example of how one predator has been protected by the introduction of livestock guard dogs", "match"),
        question(28, "r3-g1", "an optimistic suggestion about the possible positive developments in the use of livestock guard dogs", "match"),
        question(29, "r3-g1", "a description of how the methods used by livestock guard dogs help to keep predators away", "match"),
        question(30, "r3-g1", "claims by different academics that the use of livestock guard dogs is a successful way of protecting farmers' herds", "match"),
        question(31, "r3-g1", "a reference to how livestock guard dogs gain their skills", "match"),
    ]
    people = [
        "A Dan Macon", "B Silvia Ribeiro", "C Linda van Bommel",
        "D Julie Young", "E Bethany Smith",
    ]
    g7 = group(
        "r3-g2", "Questions 32–36",
        "Look at the following statements and the list of people below. Match each statement with the correct person, A–E.",
        list(range(32, 37)), layout="match", shared=people,
    )
    qs3 += [
        question(32, "r3-g2", "The use of guard dogs may save the lives of both livestock and wild animals.", "match"),
        question(33, "r3-g2", "Claims of a change in behaviour from those using livestock guard dogs may not be totally accurate.", "match"),
        question(34, "r3-g2", "There may be negative results if the use of livestock guard dogs is not sufficiently widespread.", "match"),
        question(35, "r3-g2", "Livestock guard dogs are the best way of protecting farm animals, as long as the dogs are appropriately handled.", "match"),
        question(36, "r3-g2", "Teaching a livestock guard dog how to do its work needs a different focus from teaching a house guard dog.", "match"),
    ]
    g8 = group(
        "r3-g3", "Questions 37–40",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(37, 41)), layout="summary", body=[
            "# Unintended ecological effects of using guard dogs",
            "In Namibia, livestock guard dogs have been used to protect domestic animals from attacks by cheetahs. This has led to a rise in the deaths of other predators, particularly {{37}}. In addition, it has been suggested that the dogs could have {{38}}, which may affect other species, and that they may reduce the amount of {{39}} available to certain wild animals. On the other hand, these dogs may help birds by protecting their nests. These might otherwise be threatened by predators such as {{40}}.",
        ])
    qs3 += [question(n, "r3-g3", f"Guard dog summary {n}") for n in range(37, 41)]
    apply_keys(qs3, keys["reading"], "r3")
    r3["groups"] = [g6, g7, g8]
    r3["questions"] = qs3
    reading.append(r3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The diagram below shows how fabric is manufactured from bamboo.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts20/test4-writing-task1.jpg",
            "figureAlt": "Flow diagram showing nine stages in the manufacture of bamboo fabric, from planting and harvesting to weaving and finished clothing.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "Many aspects of the way people dress today are influenced by global fashion trends.\n\nHow has global fashion become such a strong influence on people's lives? Do you think this is a positive or negative development?",
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
            "description": "The examiner asks you about personal qualities.",
            "questions": [
                {"id": "s1", "text": "What do you think your best personal qualities are? [Why?]"},
                {"id": "s2", "text": "Do you have the same personal qualities as your parents? [Why/Why not?]"},
                {"id": "s3", "text": "What personal qualities are important to you in a friend? [Why?]"},
                {"id": "s4", "text": "Do you think you have the personal qualities to be a good/successful leader? [Why/Why not?]"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a time when you had a long discussion about a news story.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a time when you had a long discussion about a news story.",
                "bullets": ["what the news story was about", "who you discussed this news story with",
                            "what people's opinions were"],
                "rounding": "and explain why you had such a long discussion about this news story.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: the news and discussion programmes.",
            "questions": [
                {"id": "s5", "text": "How do most people find out about the news in your country?"},
                {"id": "s6", "text": "Are people more interested in local news than national news?"},
                {"id": "s7", "text": "How important is it to know about international news?"},
                {"id": "s8", "text": "Why are discussion programmes involving members of the public popular on TV and radio?"},
                {"id": "s9", "text": "What kinds of people want to take part in discussion programmes?"},
                {"id": "s10", "text": "Do discussion programmes influence people in a good or bad way?"},
            ],
        },
    ]

"""IELTS 19 Academic - Test 3."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts19-test3",
        "title": "IELTS 19 · Academic Test 3",
        "module": "Academic",
        "version": "ielts19.3",
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

    # Part 1 ---------------------------------------------------------------
    g1 = group(
        "l1-g1", "Questions 1–6",
        "Complete the notes below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 7)), layout="notes", body=[
            "# Local food shops",
            "## Where to go",
            "• Kite Place — near the {{1}}",
            "## Fish market",
            "• Cross the {{2}} and turn right",
            "• Best to go before {{3}} pm, earlier than closing time",
            "## Organic shop",
            "• Called {{4}}",
            "• Below a restaurant in the large, grey building",
            "• Look for the large {{5}} outside",
            "## Supermarket",
            "• Take a {{6}} minibus, number 289",
        ])
    qs = [question(n, "l1-g1", prompt) for n, prompt in [
        (1, "Kite Place is near this"), (2, "Cross this and turn right for the fish market"),
        (3, "Best time to go to the fish market, before this time"), (4, "Name of the organic shop"),
        (5, "Large object outside the organic shop"), (6, "Colour of the minibus"),
    ]]
    g2 = group(
        "l1-g2", "Questions 7–10",
        "Complete the table below. Write ONE WORD ONLY for each answer.",
        list(range(7, 11)), layout="table", body=[
            "# Shopping",
            "• Fish market — a dozen prawns — a handful of {{7}} (type of seaweed)",
            "• Organic shop — beans and a {{8}} for dessert — spices and {{9}}",
            "• Bakery — a brown loaf — a {{10}} tart",
        ])
    qs += [question(n, "l1-g2", prompt) for n, prompt in [
        (7, "Type of seaweed from the fish market"), (8, "Fruit bought at the organic shop for dessert"),
        (9, "Spices and this are also bought at the organic shop"), (10, "Type of tart from the bakery"),
    ]]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Local food shops",
        "context": "A woman gives a friend directions and shopping advice for local food shops.",
        "groups": [g1, g2], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 ---------------------------------------------------------------
    info = [
        "A involves painting and drawing", "B will be led by a prize-winning author",
        "C is aimed at children with a disability", "D involves a drama activity",
        "E focuses on new relationships", "F is aimed at a specific age group",
        "G explores an unhappy feeling", "H raises awareness of a particular culture",
    ]
    g3 = group(
        "l2-g1", "Questions 11–16",
        "What information is given about each of the following festival workshops? Choose SIX answers from the box and write the correct letter, A–H, next to Questions 11–16.",
        list(range(11, 17)), layout="match", shared=info,
    )
    qs2 = [question(n, "l2-g1", prompt, "match") for n, prompt in [
        (11, "Superheroes"), (12, "Just do it"), (13, "Count on me"),
        (14, "Speak up"), (15, "Jump for joy"), (16, "Sticks and stones"),
    ]]
    alive = [
        "It will appeal to both boys and girls.", "The author is well known.",
        "It has colourful illustrations.", "It is funny.", "It deals with an important topic.",
    ]
    g4 = group(
        "l2-g2", "Questions 17 and 18",
        "Choose TWO letters, A–E. Which TWO reasons does the speaker give for recommending Alive and Kicking?",
        [17, 18],
    )
    qs2 += [
        question(17, "l2-g2", "First reason for recommending Alive and Kicking", "mcq", alive),
        question(18, "l2-g2", "Second reason for recommending Alive and Kicking", "mcq", alive),
    ]
    advice = [
        "Encourage children to write down new vocabulary.", "Allow children to listen to audio books.",
        "Get recommendations from librarians.", "Give children a choice about what they read.",
        "Only read aloud to children until they can read independently.",
    ]
    g5 = group(
        "l2-g3", "Questions 19 and 20",
        "Choose TWO letters, A–E. Which TWO pieces of advice does the speaker give to parents about reading?",
        [19, 20],
    )
    qs2 += [
        question(19, "l2-g3", "First piece of advice to parents about reading", "mcq", advice),
        question(20, "l2-g3", "Second piece of advice to parents about reading", "mcq", advice),
    ]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Children's book festival",
        "context": "A festival organiser talks about workshops and recommends books for children.",
        "groups": [g3, g4, g5], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 ---------------------------------------------------------------
    g6 = group("l3-g1", "Questions 21–25", "Choose the correct letter, A, B or C.", list(range(21, 26)))
    mcq = [
        (21, "How does Clare feel about the students in her Year 12 science class?",
         ["worried that they are not making progress", "challenged by their poor behaviour in class", "frustrated at their lack of interest in the subject"]),
        (22, "How does Jake react to Clare's suggestion about an experiment based on children's diet?",
         ["He is concerned that the results might not be meaningful.", "He feels some of the data might be difficult to obtain.", "He suspects that the conclusions might be upsetting."]),
        (23, "What problem do they agree may be involved in an experiment involving animals?",
         ["Any results may not apply to humans.", "It may be complicated to get permission.", "Students may not be happy about animal experiments."]),
        (24, "What question do they decide the experiment should address?",
         ["Are mice capable of controlling their food intake?", "Does an increase in sugar lead to health problems?", "How much do supplements of different kinds affect health?"]),
        (25, "Clare might also consider doing another experiment involving",
         ["other types of food supplement.", "different genetic strains of mice.", "varying amounts of exercise."]),
    ]
    qs3 = [question(n, "l3-g1", prompt, "mcq", options) for n, prompt, options in mcq]
    flow = ["A size", "B escape", "C age", "D water", "E cereal", "F calculations", "G changes", "H colour"]
    g7 = group(
        "l3-g2", "Questions 26–30",
        "Complete the flowchart below. Choose FIVE answers from the box and write the correct letter, A–H, next to Questions 26–30.",
        list(range(26, 31)), layout="flow", shared=flow, body=[
            "Choose mice which are all the same {{26}}.",
            "↓",
            "Divide the mice into two groups, each with a different {{27}}.",
            "↓",
            "Put each group in a separate cage. Feed group A commercial mouse food. Feed group B the same, plus sugar in {{28}}.",
            "↓",
            "Take measurements using an electronic scale.",
            "Place them in a weighing chamber to prevent {{29}}.",
            "↓",
            "Do all necessary {{30}}.",
        ])
    qs3 += [question(n, "l3-g2", prompt, "select") for n, prompt in [
        (26, "Mice are all the same"), (27, "Each group has a different"),
        (28, "Group B's sugar is contained in"), (29, "Weighing chamber prevents"),
        (30, "All necessary tasks at the end"),
    ]]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Science experiment for Year 12 students",
        "context": "Two teachers plan a science experiment about sugar and health.",
        "groups": [g6, g7], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 ---------------------------------------------------------------
    g8 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Microplastics",
            "## Where microplastics come from",
            "• fibres from some {{31}} during washing",
            "• the breakdown of large pieces of plastic",
            "• waste from industry",
            "• the action of vehicle tyres on roads",
            "## Effects of microplastics",
            "• They cause injuries to the {{32}} of wildlife and affect their digestive systems.",
            "• They enter the food chain, e.g. in bottled and tap water, {{33}} and seafood.",
            "• They may not affect human health, but they are already banned in skin cleaning products and {{34}} in some countries.",
            "• Microplastics enter the soil through the air, rain and {{35}}.",
            "## Microplastics in the soil – a study by Anglia Ruskin University",
            "• Earthworms are important because they add {{36}} to the soil.",
            "• The study aimed to find whether microplastics in earthworms affect the {{37}} of plants.",
            "• The study found that microplastics caused:",
            "  – {{38}} loss in earthworms",
            "  – fewer seeds to germinate",
            "  – a rise in the level of {{39}} in the soil.",
            "• The study concluded:",
            "  – soil should be seen as an important natural process.",
            "  – changes to soil damage both ecosystems and {{40}}.",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "Clothing material that releases fibres when washed"),
        (32, "Part of wildlife injured by microplastics"),
        (33, "Food from the sea, besides seafood"),
        (34, "Everyday product that may contain microplastics"),
        (35, "Agricultural substance that carries microplastics into soil"),
        (36, "What earthworms add to the soil"),
        (37, "What plant process the study investigated"),
        (38, "Type of loss found in earthworms"),
        (39, "Substance whose level rose in the soil"),
        (40, "What is damaged besides ecosystems"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Microplastics",
        "context": "A lecture about microplastics, their effects and a study of soil.",
        "groups": [g8], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 ------------------------------------------------------------
    r1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–7",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(1, 8)),
    )
    qs = [question(n, "r1-g1", prompt, "tfng") for n, prompt in [
        (1, "Archaeological research had taken place on the island of Obi before the arrival of Ceri Shipton and his colleagues."),
        (2, "At the Kelo sites, the researchers found the first clam shell axes ever to be discovered in the region."),
        (3, "The size of Obi today is less than it was 18,000 years ago."),
        (4, "A change in the climate around 11,700 years ago had a greater impact on Obi than on the surrounding islands."),
        (5, "The researchers believe there is a connection between warmer, wetter weather and a change in the material used to make axes."),
        (6, "Shipton's team were surprised to find evidence of the Obi islanders' hunting practices."),
        (7, "It is thought that the Kelo shelters were occupied continuously until about 1,000 years ago."),
    ]]
    g2 = group(
        "r1-g2", "Questions 8–13",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(8, 14)), layout="notes", body=[
            "# Archaeological findings on Obi",
            "• Excavations of rock shelters inside {{8}} near the village of Kelo revealed:",
            "  – axes from around 14,000 years ago, probably used to make canoes",
            "  – axes made of {{9}}, dating from around 11,700 years ago",
            "  – {{10}} of an animal: evidence of what ancient islanders ate",
            "• evidence of travel between islands:",
            "  – obsidian: a material that is not found naturally on Obi",
            "  – {{11}} which resembled ones found on other islands.",
            "• It is thought that from 8,000 years ago, Obi islanders:",
            "  – may have switched from hunting to fishing",
            "  – made {{12}} as well as items made out of metal",
            "  – probably took part in the production and sale of {{13}}",
        ])
    qs += [question(n, "r1-g2", prompt) for n, prompt in [
        (8, "Type of shelter excavated near Kelo"), (9, "Material used for axes from 11,700 years ago"),
        (10, "Animal remains that showed what islanders ate"), (11, "Objects similar to those found on other islands"),
        (12, "Items made by later islanders besides metal objects"), (13, "Product traded from the Maluku islands"),
    ]]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 ------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–17",
        "Reading Passage 2 has eight paragraphs, A–H. Which paragraph contains the following information? Write the correct letter, A–H.",
        list(range(14, 18)), layout="match", shared=list("ABCDEFGH"),
    )
    qs2 = [question(n, "r2-g1", prompt, "match") for n, prompt in [
        (14, "reference to the need to ensure that inhabitants of wetland regions continue to benefit from them"),
        (15, "the proportion of wetlands which have already been lost"),
        (16, "reference to the idea that people are beginning to appreciate the value of wetlands"),
        (17, "mention of the cultural significance of wetlands"),
    ]]
    g4 = group(
        "r2-g2", "Questions 18–22",
        "Complete the sentences below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(18, 23)), layout="notes", body=[
            "• Peatlands which have been drained begin to release {{18}} instead of storing it.",
            "• Once peatland areas have been cleared, {{19}} are more likely to occur.",
            "• Clearing peatland forests to make way for oil palm plantations destroys the {{20}} of the local environment.",
            "• Water is drained out of peatlands through the {{21}} which are created by logging companies.",
            "• Draining peatlands leads to {{22}}, a serious problem which can eventually result in coastal flooding and land loss.",
        ])
    qs2 += [question(n, "r2-g2", prompt) for n, prompt in [
        (18, "Gas released by drained peatlands"), (19, "Events more likely after peatland clearance"),
        (20, "What oil palm plantations destroy in the local environment"), (21, "Structures created by logging companies to drain water"),
        (22, "Process that can lead to coastal flooding"),
    ]]
    experts = ["A Matthew McCartney", "B Pieter van Eijk", "C Marcel Silvius", "D Dave Tickner"]
    g5 = group(
        "r2-g3", "Questions 23–26",
        "Look at the following statements and the list of experts below. Match each statement with the correct expert, A–D.",
        list(range(23, 27)), layout="match", shared=experts,
    )
    qs2 += [question(n, "r2-g3", prompt, "match") for n, prompt in [
        (23, "Communities living in wetland regions must be included in discussions about the future of these areas."),
        (24, "Official policies towards wetlands vary from one nation to the next."),
        (25, "People cause harm to wetlands without having any intention to do so."),
        (26, "Initiatives to reverse environmental damage need not be complex."),
    ]]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 ------------------------------------------------------------
    r3 = passage(3, passages["3"])
    g6 = group("r3-g1", "Questions 27–30", "Choose the correct letter, A, B, C or D.", list(range(27, 31)))
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in [
        (27, "What does the reader learn about the conversation in the first paragraph?",
         ["The speakers are communicating in different languages.", "Neither of the speakers is familiar with their environment.", "The topic of the conversation is difficult for both speakers.", "Aspects of the conversation are challenging for both speakers."]),
        (28, "What assists the electronic translator during lectures at Karlsruhe Institute of Technology?",
         ["the repeated content of lectures", "the students' reading skills", "the languages used", "the lecturers' technical ability"]),
        (29, "When referring to The Hitchhiker's Guide to the Galaxy, the writer suggests that",
         ["the Babel fish was considered undesirable at the time.", "this book was not seriously intending to predict the future.", "artificial speech translation was not a surprising development.", "some speech translation techniques are better than others."]),
        (30, "What does the writer say about sharing earpieces?",
         ["It is something people will get used to doing.", "The reluctance to do this is understandable.", "The equipment will be unnecessary in the future.", "It is something few people need to worry about."]),
    ]]
    endings = [
        "A but there are concerns about this.", "B as systems do not need to conform to standard practices.",
        "C but they are far from perfect.", "D despite the noise issues.",
        "E because translation is immediate.", "F and have an awareness of good manners.",
    ]
    g7 = group(
        "r3-g2", "Questions 31–34",
        "Complete each sentence with the correct ending, A–F, below.",
        list(range(31, 35)), layout="match", shared=endings,
    )
    qs3 += [question(n, "r3-g2", prompt, "match") for n, prompt in [
        (31, "Speech translation methods are developing fast in Japan"),
        (32, "TV interviews that use translation voiceover methods are successful"),
        (33, "Future translation systems should address people appropriately"),
        (34, "Users may be able to maintain their local customs"),
    ]]
    g8 = group(
        "r3-g3", "Questions 35–40",
        "Do the following statements agree with the views of the writer in Reading Passage 3? Write YES if the statement agrees with the views of the writer, NO if the statement contradicts the views of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(35, 41)),
    )
    qs3 += [question(n, "r3-g3", prompt, "ynng") for n, prompt in [
        (35, "Language translation systems will be seen as very useful throughout the academic and professional worlds."),
        (36, "The overall value of automated translation to family life is yet to be shown."),
        (37, "Automated translation could make life more difficult for immigrant families."),
        (38, "Visual aspects of language translation are being considered by scientists."),
        (39, "International scientists have found English easier to translate into other languages than Latin."),
        (40, "As far as language is concerned, there is a difference between people's social and practical needs."),
    ]]
    apply_keys(qs3, keys["reading"], "r3")
    r3["groups"] = [g6, g7, g8]
    r3["questions"] = qs3
    reading.append(r3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The diagram below shows how a biofuel called ethanol is produced.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts19/test3-writing-task1.jpg",
            "figureAlt": "A circular diagram showing the stages of ethanol production, from plants and trees growing to harvesting, pre-processing, cellulose, sugars, microbes and ethanol, with carbon dioxide released at several stages.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "It is important for everyone, including young people, to save money for their future.\n\nTo what extent do you agree or disagree with this statement?",
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
            "description": "The examiner asks you about holidays.",
            "questions": [
                {"id": "s1", "text": "Do you prefer spending holidays with friends or with family? [Why?]"},
                {"id": "s2", "text": "What kind of holiday accommodation do you like to stay in? [Why?]"},
                {"id": "s3", "text": "What plans do you have for your next holiday?"},
                {"id": "s4", "text": "Is your city or region a good place for other people to visit on holiday? [Why/Why not?]"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a car journey you made that took longer than expected.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a car journey you made that took longer than expected.",
                "bullets": ["where you were going", "who you were with", "how you felt during the journey"],
                "rounding": "and explain why this car journey took longer than expected.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: driving a car and electric cars.",
            "questions": [
                {"id": "s5", "text": "How interested are young people in your country in learning to drive?"},
                {"id": "s6", "text": "What are the differences between driving in the countryside and driving in the city?"},
                {"id": "s7", "text": "Do you consider most drivers where you live to be good drivers?"},
                {"id": "s8", "text": "How popular are electric cars in your country?"},
                {"id": "s9", "text": "In what ways could more people be persuaded to buy electric cars?"},
                {"id": "s10", "text": "Do you think all cars will be electric one day?"},
            ],
        },
    ]

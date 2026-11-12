"""IELTS 19 Academic - Test 2."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts19-test2",
        "title": "IELTS 19 · Academic Test 2",
        "module": "Academic",
        "version": "ielts19.2",
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
        "Complete the form below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 7)), layout="form", body=[
            "# Guitar Group",
            "• Coordinator: Gary {{1}}",
            "• Level: {{2}}",
            "• Place: the {{3}}, {{4}} Street",
            "• First floor, Room T347",
            "• Time: Thursday morning at {{5}}",
            "• Recommended website: 'The Perfect {{6}}'",
        ])
    qs = [question(n, "l1-g1", prompt) for n, prompt in [
        (1, "Guitar group coordinator's surname"),
        (2, "Level of the guitar group"),
        (3, "Name of the building where the group meets"),
        (4, "Street name"),
        (5, "Time on Thursday morning"),
        (6, "Name of the recommended website"),
    ]]
    g2 = group(
        "l1-g2", "Questions 7–10",
        "Complete the table below. Write ONE WORD ONLY for each answer.",
        list(range(7, 11)), layout="table", body=[
            "# A typical 45-minute guitar lesson",
            "• 5 minutes — tuning guitars — using an app or by {{7}}",
            "• 10 minutes — strumming chords using our thumbs — keeping time while the teacher is {{8}}",
            "• 15 minutes — playing songs — often listening to a {{9}} of a song",
            "• 10 minutes — playing single notes and simple tunes — playing together, then {{10}}",
            "• 5 minutes — noting things to practise at home",
        ])
    qs += [question(n, "l1-g2", prompt) for n, prompt in [
        (7, "Tuning guitars with an app or by this"),
        (8, "What the teacher does to keep time"),
        (9, "What students listen to when playing songs"),
        (10, "How students play single notes and simple tunes after playing together"),
    ]]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Guitar Group",
        "context": "A woman asks a friend about joining a local guitar group.",
        "groups": [g1, g2], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 ---------------------------------------------------------------
    g3 = group("l2-g1", "Questions 11–16", "Choose the correct letter, A, B or C.", list(range(11, 17)))
    mcq = [
        (11, "What made David leave London and move to Northsea?",
         ["He was eager to develop a hobby.", "He wanted to work shorter hours.", "He found his job in website design unsatisfying."]),
        (12, "The Lifeboat Institution in Northsea was built with money provided by",
         ["a local organisation.", "a local resident.", "the local council."]),
        (13, "In his health assessment, the doctor was concerned about the fact that David",
         ["might be colour blind.", "was rather short-sighted.", "had undergone eye surgery."]),
        (14, "After arriving at the lifeboat station, they aim to launch the boat within",
         ["five minutes.", "six to eight minutes.", "eight and a half minutes."]),
        (15, "As a 'helmsman', David has the responsibility of deciding",
         ["who will be the members of his crew.", "what equipment it will be necessary to take.", "if the lifeboat should be launched."]),
        (16, "As well as going out on the lifeboat, David",
         ["gives talks on safety at sea.", "helps with fundraising.", "recruits new volunteers."]),
    ]
    qs2 = [question(n, "l2-g1", prompt, "mcq", options) for n, prompt, options in mcq]
    training = [
        "The residential course developed his leadership skills.",
        "The training in use of ropes and knots was quite brief.",
        "The training exercises have built up his mental strength.",
        "The casualty care activities were particularly challenging for him.",
        "The wave tank activities provided practice in survival techniques.",
    ]
    g4 = group(
        "l2-g2", "Questions 17 and 18",
        "Choose TWO letters, A–E. Which TWO things does David say about the lifeboat volunteer training?",
        [17, 18],
    )
    qs2 += [
        question(17, "l2-g2", "First thing David says about volunteer training", "mcq", training),
        question(18, "l2-g2", "Second thing David says about volunteer training", "mcq", training),
    ]
    motivating = [
        "working as part of a team", "experiences when working in winter",
        "being thanked by those he has helped", "the fact that it keeps him fit",
        "the chance to develop new equipment",
    ]
    g5 = group(
        "l2-g3", "Questions 19 and 20",
        "Choose TWO letters, A–E. Which TWO things does David find most motivating about the work he does?",
        [19, 20],
    )
    qs2 += [
        question(19, "l2-g3", "First motivating thing about the work", "mcq", motivating),
        question(20, "l2-g3", "Second motivating thing about the work", "mcq", motivating),
    ]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Working as a lifeboat volunteer",
        "context": "A lifeboat volunteer talks about his work and training.",
        "groups": [g3, g4, g5], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 ---------------------------------------------------------------
    g6 = group("l3-g1", "Questions 21–24", "Choose the correct letter, A, B or C.", list(range(21, 25)))
    mcq3 = [
        (21, "At first, Don thought the topic of recycling footwear might be too",
         ["limited in scope.", "hard to research.", "boring for listeners."]),
        (22, "When discussing trainers, Bella and Don disagree about",
         ["how popular they are among young people.", "how suitable they are for school.", "how quickly they wear out."]),
        (23, "Bella says that she sometimes recycles shoes because",
         ["they no longer fit.", "she no longer likes them.", "they are no longer in fashion."]),
        (24, "What did the article say that confused Don?",
         ["Public consumption of footwear has risen.", "Less footwear is recycled now than in the past.", "People dispose of more footwear than they used to."]),
    ]
    qs3 = [question(n, "l3-g1", prompt, "mcq", options) for n, prompt, options in mcq3]
    reasons = [
        "A one shoe was missing", "B the colour of one shoe had faded", "C one shoe had a hole in it",
        "D the shoes were brand new", "E the shoes were too dirty", "F the stitching on the shoes was broken",
    ]
    g7 = group(
        "l3-g2", "Questions 25–28",
        "What reasons did the recycling manager give for rejecting footwear, according to the students? Choose FOUR answers from the box and write the correct letter, A–F, next to Questions 25–28.",
        list(range(25, 29)), layout="match", shared=reasons,
    )
    qs3 += [question(n, "l3-g2", prompt, "match") for n, prompt in [
        (25, "the high-heeled shoes"), (26, "the ankle boots"), (27, "the baby shoes"), (28, "the trainers"),
    ]]
    g8 = group("l3-g3", "Questions 29–30", "Choose the correct letter, A, B or C.", list(range(29, 31)))
    qs3 += [question(n, "l3-g3", prompt, "mcq", options) for n, prompt, options in [
        (29, "Why did the project to make 'new' shoes out of old shoes fail?",
         ["People believed the 'new' pairs of shoes were unhygienic.", "There were not enough good parts to use in the old shoes.", "The shoes in the 'new' pairs were not completely alike."]),
        (30, "Bella and Don agree that they can present their topic",
         ["from a new angle.", "with relevant images.", "in a straightforward way."]),
    ]]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Recycling footwear",
        "context": "Two students discuss an article about recycling footwear for a presentation.",
        "groups": [g6, g7, g8], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 ---------------------------------------------------------------
    g9 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Tardigrades",
            "• more than 1,000 species, 0.05–1.2 millimetres long",
            "• also known as water 'bears' (due to how they {{31}}) and 'moss piglets'",
            "## Physical appearance",
            "• {{32}} body and four pairs of legs",
            "• has {{33}} for gripping",
            "• absence of respiratory organs",
            "• body filled with a liquid that carries both {{34}} and blood",
            "• mouth shaped like a {{35}} with teeth called stylets",
            "## Habitat",
            "• often found at the bottom of a lake or on plants",
            "• very resilient and can exist in very low or high {{36}}",
            "## Cryptobiosis",
            "• In dry conditions, they roll into a ball called a 'tun'.",
            "• They stay alive with a much lower metabolism than usual.",
            "• A type of {{37}} ensures their DNA is not damaged.",
            "• Research is underway to find out how many days they can stay alive in {{38}}.",
            "## Feeding",
            "• consume liquids, e.g. those found in moss or {{39}}",
            "• may eat other tardigrades",
            "## Conservation status",
            "• They are not considered to be {{40}}",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "How tardigrades move, giving them the name water 'bears'"),
        (32, "Shape of the tardigrade's body"),
        (33, "Body parts used for gripping"),
        (34, "Gas carried by the liquid in the body"),
        (35, "Shape of the mouth"),
        (36, "Conditions of this kind can be very low or very high"),
        (37, "Type of substance that protects DNA"),
        (38, "Place where researchers test how long they survive"),
        (39, "Plant material where they find liquids"),
        (40, "Conservation status they are not considered to have"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Tardigrades",
        "context": "A lecture about tardigrades and their ability to survive extreme conditions.",
        "groups": [g9], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 ------------------------------------------------------------
    r1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–7",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(1, 8)), layout="notes", body=[
            "# Britain's Industrial Revolution",
            "## Steam power",
            "• Newcomen's steam engine was used in mines to remove water.",
            "• In Watt and Boulton's steam engine, the movement of the {{1}} was linked to a gear system.",
            "• A greater supply of {{2}} was required to power steam engines.",
            "## Textile industry",
            "• Before the Industrial Revolution, spinners and weavers worked at home and in {{3}}.",
            "• Not as much {{4}} was needed to produce cloth once the spinning jenny and power loom were invented.",
            "## Iron industry",
            "• Smelting of iron ore with coke resulted in material that was better {{5}}.",
            "• Demand for iron increased with the growth of the {{6}}.",
            "## Communications",
            "• Cooke and Wheatstone patented the first telegraphy system.",
            "• The telegraphy system was used to prevent locomotives colliding.",
            "## Urbanisation",
            "• Small towns turned into cities very quickly.",
            "• The new cities were dirty, crowded and lacked sufficient {{7}}.",
        ])
    qs = [question(n, "r1-g1", prompt) for n, prompt in [
        (1, "Moving part linked to a gear system"), (2, "Fuel needed in greater supply"),
        (3, "Workplace for spinners and weavers before industrialisation"), (4, "What was needed less to produce cloth"),
        (5, "Quality of material produced by smelting with coke"), (6, "Growing form of transport that increased iron demand"),
        (7, "Public service lacking in the new cities"),
    ]]
    g2 = group(
        "r1-g2", "Questions 8–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(8, 14)),
    )
    qs += [question(n, "r1-g2", prompt, "tfng") for n, prompt in [
        (8, "Britain's canal network grew rapidly so that more goods could be transported around the country."),
        (9, "Costs in the iron industry rose when the technique of smelting iron ore with coke was introduced."),
        (10, "Samuel Morse's communication system was more reliable than that developed by William Cooke and Charles Wheatstone."),
        (11, "The economic benefits of industrialisation were limited to certain sectors of society."),
        (12, "Some skilled weavers believed that the introduction of the new textile machines would lead to job losses."),
        (13, "There was some sympathy among local people for the Luddites who were arrested near Huddersfield."),
    ]]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 ------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–18",
        "Reading Passage 2 has six paragraphs, A–F. Which paragraph contains the following information? Write the correct letter, A–F. NB You may use any letter more than once.",
        list(range(14, 19)), layout="match", shared=list("ABCDEF"),
    )
    qs2 = [question(n, "r2-g1", prompt, "match") for n, prompt in [
        (14, "reference to two chemical compounds which impact on performance"),
        (15, "examples of strategies for minimising the effects of stress"),
        (16, "how a sportsperson accounted for their own experience of stress"),
        (17, "study results indicating links between stress responses and performance"),
        (18, "mention of people who can influence how athletes perceive their stress responses"),
    ]]
    g4 = group(
        "r2-g2", "Questions 19–22",
        "Complete the sentences below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(19, 23)), layout="notes", body=[
            "• Performance stress involves many demands on the athlete, for example, coping with the possible risk of {{19}}.",
            "• Cortisol can cause tennis players to produce fewer {{20}}.",
            "• Psychologists can help athletes to view their physiological responses as the effect of a positive feeling such as {{21}}.",
            "• {{22}} is an example of a psychological technique which can reduce an athlete's stress responses.",
        ])
    qs2 += [question(n, "r2-g2", prompt) for n, prompt in [
        (19, "Possible risk athletes must cope with"), (20, "What cortisol reduces in tennis players"),
        (21, "Positive feeling that physiological responses can be attributed to"), (22, "Psychological technique that can reduce stress responses"),
    ]]
    raducanu = [
        "the stage at which she dropped out of the tournament",
        "symptoms of her performance stress at the tournament",
        "measures which she had taken to manage her stress levels",
        "aspects of the Wimbledon tournament which increased her stress levels",
        "reactions to her social media posts about her experience at Wimbledon",
    ]
    g5 = group(
        "r2-g3", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO facts about Emma Raducanu's withdrawal from the Wimbledon tournament are mentioned in the text?",
        [23, 24],
    )
    qs2 += [
        question(23, "r2-g3", "First fact about Raducanu's withdrawal", "mcq", raducanu),
        question(24, "r2-g3", "Second fact about Raducanu's withdrawal", "mcq", raducanu),
    ]
    anxiety = [
        "the factors which determine how severe it may be",
        "how long it takes for its effects to become apparent",
        "which of its symptoms is most frequently encountered",
        "the types of athletes who are most likely to suffer from it",
        "the harm that can result if athletes experience it too often",
    ]
    g6 = group(
        "r2-g4", "Questions 25 and 26",
        "Choose TWO letters, A–E. Which TWO facts about anxiety are mentioned in Paragraph E of the text?",
        [25, 26],
    )
    qs2 += [
        question(25, "r2-g4", "First fact about anxiety", "mcq", anxiety),
        question(26, "r2-g4", "Second fact about anxiety", "mcq", anxiety),
    ]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5, g6]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 ------------------------------------------------------------
    r3 = passage(3, passages["3"])
    phrases = [
        "A appeal", "B determined", "C intrigued", "D single", "E achievement", "F devoted",
        "G involved", "H unique", "I innovative", "J satisfaction", "K intent",
    ]
    g7 = group(
        "r3-g1", "Questions 27–32",
        "Complete the summary using the list of phrases, A–K, below.",
        list(range(27, 33)), layout="summary", shared=phrases, body=[
            "# Maryam Mirzakhani",
            "Maryam Mirzakhani is regarded as {{27}} in the field of mathematics because she was the only female holder of the prestigious Fields Medal – a record that she retained at the time of her death. However, maths held little {{28}} for her as a child and in fact her performance was below average until she was {{29}} once by a difficult puzzle that one of her siblings showed her.",
            "Later, as a professional mathematician, she had an inquiring mind and proved herself to be {{30}} when things did not go smoothly. She said she got the greatest {{31}} from making ground-breaking discoveries and in fact she was responsible for some extremely {{32}} mathematical studies.",
        ])
    qs3 = [question(n, "r3-g1", prompt, "select") for n, prompt in [
        (27, "How Mirzakhani is regarded in mathematics"), (28, "What maths held little of for her as a child"),
        (29, "How she became interested in maths"), (30, "How she proved herself when things went badly"),
        (31, "What she got from ground-breaking discoveries"), (32, "Type of mathematical studies she produced"),
    ]]
    g8 = group(
        "r3-g2", "Questions 33–37",
        "Do the following statements agree with the claims of the writer in Reading Passage 3? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(33, 38)),
    )
    qs3 += [question(n, "r3-g2", prompt, "ynng") for n, prompt in [
        (33, "Many people who ended up winning prestigious intellectual prizes only reached an average standard when young."),
        (34, "Einstein's failures as a young man were due to his lack of confidence."),
        (35, "It is difficult to reach agreement on whether some children are actually born gifted."),
        (36, "Einstein was upset by the public's view of his life's work."),
        (37, "Einstein put his success down to the speed at which he dealt with scientific questions."),
    ]]
    g9 = group("r3-g3", "Questions 38–40", "Choose the correct letter, A, B, C or D.", list(range(38, 41)))
    qs3 += [question(n, "r3-g3", prompt, "mcq", options) for n, prompt, options in [
        (38, "What does Eyre believe is needed for children to equal 'gifted' standards?",
         ["strict discipline from the teaching staff", "assistance from their peers in the classroom", "the development of a spirit of inquiry towards their studies", "the determination to surpass everyone else's achievements"]),
        (39, "What is the result of Ericsson's research?",
         ["Very gifted students do not need to work on improving memory skills.", "Being born with a special gift is not the key factor in becoming expert.", "Including time for physical exercise is crucial in raising performance.", "10,000 hours of relevant and demanding work will create a genius."]),
        (40, "In the penultimate paragraph, it is stated the key to some deprived children's success is",
         ["a regular and nourishing diet at home.", "the loving support of more than one parent.", "a community which has well-funded facilities for learning.", "the guidance of someone who recognises the benefits of learning."]),
    ]]
    apply_keys(qs3, keys["reading"], "r3")
    r3["groups"] = [g7, g8, g9]
    r3["questions"] = qs3
    reading.append(r3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The plans below show a harbour in 2000 and how it looks today.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts19/test2-writing-task1.jpg",
            "figureAlt": "Two plans of Porth Harbour, comparing the facilities in 2000 with the present day.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "The working week should be shorter and workers should have a longer weekend.\n\nDo you agree or disagree?",
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
            "description": "The examiner asks you about travelling by plane.",
            "questions": [
                {"id": "s1", "text": "Have you travelled a lot by plane? [To where?/Why not?]"},
                {"id": "s2", "text": "Why do you think some people enjoy travelling by plane?"},
                {"id": "s3", "text": "Would you like to live near an airport? [Why/Why not?]"},
                {"id": "s4", "text": "In the future, do you think that you will travel by plane more often? [Why/Why not?]"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a person from your country who has won a prize, award or medal.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a person from your country who has won a prize, award or medal.",
                "bullets": [
                    "who this person is",
                    "which prize, award or medal they received",
                    "what they did to win this",
                ],
                "rounding": "and explain whether you think it was right that this person received this prize, award or medal.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: rewards for children at school and rewards for sportspeople.",
            "questions": [
                {"id": "s5", "text": "What types of school prizes do children in your country receive?"},
                {"id": "s6", "text": "What do you think are the advantages of rewarding schoolchildren for good work?"},
                {"id": "s7", "text": "Do you agree that it's more important for children to receive rewards from their parents than from teachers?"},
                {"id": "s8", "text": "Do you think that some sportspeople (e.g. top footballers) are paid too much money?"},
                {"id": "s9", "text": "Should everyone on a team get the same prize money when they win?"},
                {"id": "s10", "text": "Do you agree with the view that, in sport, taking part is more important than winning?"},
            ],
        },
    ]

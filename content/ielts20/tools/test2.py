"""IELTS 20 Academic — Test 2."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts20-test2",
        "title": "IELTS 20 · Academic Test 2",
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
            "# Practical support for carers",
            "• time for other responsibilities — a {{1}}",
            "## Assessment of mother's needs",
            "This may include discussion of:",
            "• how much {{2}} the caring involves",
            "• types of tasks, e.g. help with dressing, helping her have a {{3}}, shopping, helping with meals, dealing with {{4}}",
            "• especially difficult aspects, e.g. loss of {{5}}, {{6}} her, preventing a {{7}}",
            "## Types of support that may be offered",
            "• transport costs, e.g. the cost of a {{8}}",
            "• car-related costs, e.g. fuel and {{9}}",
            "• help with housework",
            "• help to reduce {{10}}",
        ])
    qs = [
        question(1, "l1-g1", "What the carer can have time for other responsibilities"),
        question(2, "l1-g1", "What the assessment asks how much the caring involves"),
        question(3, "l1-g1", "Help with dressing and helping her have this"),
        question(4, "l1-g1", "What the carer may need help dealing with"),
        question(5, "l1-g1", "Difficult aspect: loss of this"),
        question(6, "l1-g1", "Difficult aspect: doing this to her"),
        question(7, "l1-g1", "Difficult aspect: preventing this"),
        question(8, "l1-g1", "Transport cost example"),
        question(9, "l1-g1", "Car-related cost besides fuel"),
        question(10, "l1-g1", "What support may help to reduce"),
    ]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Support for carers",
        "context": "A woman asks a friend for advice about the practical support available for carers.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    roles = [
        "A providing entertainment",
        "B providing publicity about a council service",
        "C contacting local businesses",
        "D giving advice to visitors",
        "E collecting feedback on events",
        "F selling tickets",
        "G introducing guest speakers at an event",
        "H encouraging cooperation between local organisations",
        "I helping people find their seats",
    ]
    g2 = group(
        "l2-g1", "Questions 11–16",
        "What is the role of the volunteers in each of the following activities? Choose SIX answers from the box and write the correct letter, A–I.",
        list(range(11, 17)), layout="match", shared=roles,
    )
    qs2 = [
        question(11, "l2-g1", "walking around the town centre", "match"),
        question(12, "l2-g1", "helping at concerts", "match"),
        question(13, "l2-g1", "getting involved with community groups", "match"),
        question(14, "l2-g1", "helping with a magazine", "match"),
        question(15, "l2-g1", "participating at lunches for retired people", "match"),
        question(16, "l2-g1", "helping with the website", "match"),
    ]
    g3 = group(
        "l2-g2", "Questions 17–20", "Choose the correct letter, A, B or C.",
        list(range(17, 21)),
    )
    mcq = [
        (17, "Which event requires the largest number of volunteers?",
         ["the music festival", "the science festival", "the book festival"]),
        (18, "What is the most important requirement for volunteers at the festivals?",
         ["interpersonal skills", "personal interest in the event", "flexibility"]),
        (19, "New volunteers will start working in the week beginning",
         ["2 September.", "9 September.", "23 September."]),
        (20, "What is the next annual event for volunteers?",
         ["a boat trip", "a barbecue", "a party"]),
    ]
    qs2 += [question(n, "l2-g2", prompt, "mcq", options) for n, prompt, options in mcq]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "The town volunteer scheme",
        "context": "A council officer explains the volunteer scheme to a group of new volunteers.",
        "groups": [g2, g3], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    opinions = [
        "A The information given about this was too vague.",
        "B This may not be relevant to their course.",
        "C This will involve only a small number of statistics.",
        "D It will be easy to find facts about this.",
        "E The facts about this may not be reliable.",
        "F No useful research has been done on this.",
        "G The information provided about this was interesting.",
    ]
    g4 = group(
        "l3-g1", "Questions 21–25",
        "What is Rosie and Colin's opinion about each of the following aspects of human geography? Choose FIVE answers from the box and write the correct letter, A–G.",
        list(range(21, 26)), layout="match", shared=opinions,
    )
    qs3 = [question(n, "l3-g1", topic, "match") for n, topic in [
        (21, "Population"), (22, "Health"), (23, "Economies"),
        (24, "Culture"), (25, "Poverty"),
    ]]
    g5 = group(
        "l3-g2", "Questions 26–30", "Choose the correct letter, A, B or C.",
        list(range(26, 31)),
    )
    mcq3 = [
        (26, "Rosie says that in her own city the main problem is",
         ["crime.", "housing.", "unemployment."]),
        (27, "What recent additions to the outskirts of their cities are both students happy about?",
         ["conference centres", "sports centres", "retail centres"]),
        (28, "The students agree that developing disused industrial sites may",
         ["have unexpected costs.", "damage the urban environment.",
          "destroy valuable historical buildings."]),
        (29, "The students will mention Masdar City as an example of an attempt to achieve",
         ["daily collections for waste recycling.", "sustainable energy use.",
          "free transport for everyone."]),
        (30, "When discussing the Eco town of Greenhill Abbots, Colin is uncertain about",
         ["what its objectives were.", "why there was opposition to it.",
          "how much of it has actually been built."]),
    ]
    qs3 += [question(n, "l3-g2", prompt, "mcq", options) for n, prompt, options in mcq3]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Planning a human geography assignment",
        "context": "Two students discuss possible topics for their human geography assignment.",
        "groups": [g4, g5], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g6 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Developing food trends",
            "• The growth in interest in food fashions started with {{31}} of food being shared on social media.",
            "• The UK food industry is constantly developing products which are new or different.",
            "• Influencers on social media become brand ambassadors.",
            "• Sales of {{32}} food brands have grown this way.",
            "• Supermarkets track demand for ingredients on social media.",
            "• Famous {{33}} are influential.",
            "## Marketing campaigns",
            "• The avocado: {{34}} were invited to visit growers in South Africa; advertising focused on its {{35}} benefits.",
            "• Oat milk: a Swedish brand's media campaign received publicity by upsetting competitors; promotion in the USA through {{36}} shops reduced the need for advertising; it appealed to consumers concerned about the {{37}}.",
            "• Norwegian skrei: helped strengthen the {{38}} of Norwegian seafood.",
            "## Ethical concerns",
            "• Quinoa: its success led to an increase in its {{39}}; overuse of resources resulted in poor quality {{40}}.",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "What started the growth in interest in food fashions"),
        (32, "Type of food brands whose sales grew through influencers"),
        (33, "Famous people who are influential"),
        (34, "People invited to visit avocado growers"),
        (35, "What avocado advertising focused on"),
        (36, "Type of shops used to promote oat milk in the USA"),
        (37, "What oat milk consumers are concerned about"),
        (38, "What Norwegian skrei helped strengthen"),
        (39, "What quinoa's success increased"),
        (40, "What overuse of resources did to quinoa quality"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Developing food trends",
        "context": "A lecture about how food trends are created and marketed.",
        "groups": [g6], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 --------------------------------------------------------------
    r1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–6",
        "Complete the notes below. Choose ONE WORD AND/OR A NUMBER from the passage for each answer.",
        list(range(1, 7)), layout="notes", body=[
            "# Manatees",
            "## Appearance",
            "• look similar to dugongs, but with a differently shaped {{1}}",
            "## Movement",
            "• have fewer neck bones than most mammals",
            "• need to use their {{2}} to help turn their bodies around in order to look sideways",
            "• sense vibrations in the water by means of {{3}} on their skin",
            "## Feeding",
            "• eat mainly aquatic vegetation, such as {{4}}",
            "• grasp and pull up plants with their {{5}}",
            "## Breathing",
            "• come to the surface for air every 2–4 minutes when awake and every 15–20 while sleeping",
            "• may regulate the {{6}} of their bodies by using muscles of the diaphragm to store air internally",
        ])
    qs = [question(n, "r1-g1", f"Manatee notes {n}") for n in range(1, 7)]
    g2 = group(
        "r1-g2", "Questions 7–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(7, 14)),
    )
    qs += [
        question(7, "r1-g2", "West Indian manatees can be found in a variety of different aquatic habitats.", "tfng"),
        question(8, "r1-g2", "The Florida manatee lives in warmer waters than the Antillean manatee.", "tfng"),
        question(9, "r1-g2", "The African manatee's range is limited to coastal waters between the West African countries of Mauritania and Angola.", "tfng"),
        question(10, "r1-g2", "The extent of the loss of Amazonian manatees in the mid-twentieth century was only revealed many years later.", "tfng"),
        question(11, "r1-g2", "It is predicted that West Indian manatee populations will fall in the coming decades.", "tfng"),
        question(12, "r1-g2", "The risk to manatees from entanglement and plastic consumption increased significantly in the period 2009–2020.", "tfng"),
        question(13, "r1-g2", "There is some legislation in place which aims to reduce the likelihood of boat strikes on manatees in Florida.", "tfng"),
    ]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 --------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–16",
        "Reading Passage 2 has six paragraphs, A–F. Which paragraph contains the following information? NB You may use any letter more than once.",
        list(range(14, 17)), layout="match", shared=list("ABCDEF"),
    )
    qs2 = [
        question(14, "r2-g1", "mention of false assumptions about why people procrastinate", "match"),
        question(15, "r2-g1", "reference to the realisation that others also procrastinate", "match"),
        question(16, "r2-g1", "neurological evidence of a link between procrastination and emotion", "match"),
    ]
    g4 = group(
        "r2-g2", "Questions 17–22",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(17, 23)), layout="summary", body=[
            "# What makes us procrastinate?",
            "Many people think that procrastination is the result of {{17}}. Others believe it to be the result of an inability to organise time efficiently. But scientific studies suggest that procrastination is actually due to poor mood management. The tasks we are most likely to put off are those that could damage our self-esteem or cause us to feel {{18}} when we think about them. Research comparing chronic procrastinators with other people even found differences in the brain regions associated with regulating emotions and identifying {{19}}.",
            "Emotionally loaded and difficult tasks often cause us to procrastinate. Getting ready to take {{20}} might be a typical example of one such task. People who are likely to procrastinate tend to be either {{21}} or those with low self-esteem.",
            "Procrastination is only a short-term measure for managing emotions. It's often followed by a feeling of {{22}}, which worsens our mood and leads to more procrastination.",
        ])
    qs2 += [question(n, "r2-g2", f"Procrastination summary {n}") for n in range(17, 23)]

    employee_options = [
        "Their salaries are lower.",
        "The quality of their work is inferior.",
        "They don't keep their jobs for as long.",
        "They don't enjoy their working lives as much.",
        "They have poorer relationships with colleagues.",
    ]
    g5 = group(
        "r2-g3", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO comparisons between employees who often procrastinate and those who do not are mentioned in the text?",
        [23, 24],
    )
    qs2 += [
        question(23, "r2-g3", "First comparison between employees who procrastinate", "mcq", employee_options),
        question(24, "r2-g3", "Second comparison between employees who procrastinate", "mcq", employee_options),
    ]
    advice = [
        "not judging ourselves harshly", "setting ourselves manageable aims",
        "rewarding ourselves for tasks achieved",
        "prioritising tasks according to their importance",
        "avoiding things that stop us concentrating on our tasks",
    ]
    g6 = group(
        "r2-g4", "Questions 25 and 26",
        "Choose TWO letters, A–E. Which TWO recommendations for getting out of a cycle of procrastination does the writer give?",
        [25, 26],
    )
    qs2 += [
        question(25, "r2-g4", "First recommendation for breaking the cycle", "mcq", advice),
        question(26, "r2-g4", "Second recommendation for breaking the cycle", "mcq", advice),
    ]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5, g6]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 --------------------------------------------------------------
    r3 = passage(3, passages["3"])
    g7 = group(
        "r3-g1", "Questions 27–32",
        "Do the following statements agree with the claims of the writer in Reading Passage 3? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(27, 33)),
    )
    qs3 = [
        question(27, "r3-g1", "When DeJesus first used ABS, he shared decision-making about strikes with it.", "ynng"),
        question(28, "r3-g1", "MLB considered it necessary to amend the size of the strike zone when criticisms were received from players.", "ynng"),
        question(29, "r3-g1", "MLB is keen to justify the money spent on improving the accuracy of ABS's calculations.", "ynng"),
        question(30, "r3-g1", "The hundred-mile-an-hour fastball led to a more exciting style of play.", "ynng"),
        question(31, "r3-g1", "The differing proposals for alterations to the baseball bat led to fierce debate on Sword's team.", "ynng"),
        question(32, "r3-g1", "ABS makes changes to the shape of the strike zone feasible.", "ynng"),
    ]
    phrases = [
        "A pitch boundary", "B numerous disputes", "C team tactics",
        "D subjective assessment", "E widespread approval", "F former roles",
        "G total silence", "H perceived area",
    ]
    g8 = group(
        "r3-g2", "Questions 33–37",
        "Complete the summary using the list of phrases, A–H, below.",
        list(range(33, 38)), layout="summary", shared=phrases, body=[
            "# Calls by the umpire",
            "Even after ABS was developed, MLB still wanted human umpires to shout out decisions as they had in their {{33}}. The umpire's job had, at one time, required a {{34}} about whether a ball was a strike. A ball is considered a strike when the batter does not hit it and it crosses through a {{35}} extending approximately from the batter's knee to his chest. In the past, {{36}} over strike calls were not uncommon, but today everyone accepts the complete ban on pushing or shoving the umpire. One difference, however, is that during the first game DeJesus used ABS, strike calls were met with {{37}}.",
        ])
    qs3 += [question(n, "r3-g2", f"Umpire summary {n}", "select") for n in range(33, 38)]
    g9 = group(
        "r3-g3", "Questions 38–40", "Choose the correct letter, A, B, C or D.",
        list(range(38, 41)),
    )
    mcq = [
        (38, "What does the writer suggest about ABS in the fifth paragraph?",
         ["It is bound to make key decisions that are wrong.",
          "It may reduce some of the appeal of the game.",
          "It will lead to the disappearance of human umpires.",
          "It may increase calls for the rules of baseball to be changed."]),
        (39, "Morgan Sword says that the introduction of ABS",
         ["was regarded as an experiment without a guaranteed outcome.",
          "was intended to keep up with developments in other sports.",
          "was a response to changing attitudes about the role of sport.",
          "was an attempt to ensure baseball retained a young audience."]),
        (40, "Why does the writer include the views of Noe and Russo?",
         ["to show that attitudes to technology vary widely",
          "to argue that people have unrealistic expectations of sport",
          "to indicate that accuracy is not the same thing as enjoyment",
          "to suggest that the number of baseball fans needs to increase"]),
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
            "prompt": "The plans below show the site of a farm in 1950 and the same site today.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts20/test2-writing-task1.jpg",
            "figureAlt": "Two plans of Beechwood Farm, comparing the site in 1950 with the site today.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "In many countries, primary and secondary schools close for two months or more in the summer holidays.\n\nWhat is the value of long school holidays?\n\nWhat are the arguments in favour of shorter school holidays?",
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
            "description": "The examiner asks you about fruit.",
            "questions": [
                {"id": "s1", "text": "What's your favourite fruit?"},
                {"id": "s2", "text": "Are there any kinds of fruit that you don't like eating?"},
                {"id": "s3", "text": "Do you like eating cooked food that has fruit in it?"},
                {"id": "s4", "text": "Where's the best place to buy fruit where you live?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a time when you changed a plan you had made.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a time when you changed a plan you had made.",
                "bullets": ["what your original plan was", "why you changed it", "what new plan you made"],
                "rounding": "and explain how you felt about changing your plan.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: making plans and choosing a career.",
            "questions": [
                {"id": "s5", "text": "What kinds of plans do friends make together?"},
                {"id": "s6", "text": "Do you think it's better to discuss future plans with friends or with family?"},
                {"id": "s7", "text": "When making plans for the future, is it important not to copy friends?"},
                {"id": "s8", "text": "When people are choosing what to study, how important is it that their course should lead directly to a career?"},
                {"id": "s9", "text": "Why is it a good idea to get some work experience before deciding on a future career?"},
                {"id": "s10", "text": "How easy do you think it is for people to change from one career to another?"},
            ],
        },
    ]

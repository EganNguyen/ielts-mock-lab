"""Cambridge IELTS 21 — Academic Test 1."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    listening = build_listening(keys, transcripts)
    reading = build_reading(passages, keys)
    writing = build_writing()
    speaking = build_speaking()
    return {
        "id": "cambridge21-test1",
        "title": "Cambridge IELTS 21 · Academic Test 1",
        "module": "Academic",
        "version": "cambridge21.1",
        "listening": listening,
        "reading": reading,
        "writing": writing,
        "speaking": speaking,
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
        "l1-g1", "Questions 1–6",
        "Complete the table below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 7)), layout="form", body=[
            "# Oyster Bay Sailing Club Courses",
            "• Taster day — introduction to sailing — £120 if booking one place — small groups (max {{1}} people)",
            "• Level 1 — basic theory, e.g. understanding the {{2}} and tides",
            "• Level 1 — basic sailing skills, including {{3}}",
            "• Level 1 — £200 — a {{4}} is available for club members",
            "• Level 1 — all inclusive, plus a useful {{5}}",
            "• Level 1 — a {{6}} at the end of the course for all participants",
        ],
    )
    qs = [
        question(1, "l1-g1", "Maximum number of people in a Taster day group"),
        question(2, "l1-g1", "What Level 1 theory helps you understand, with tides"),
        question(3, "l1-g1", "Basic sailing skills, including …"),
        question(4, "l1-g1", "What is available for club members on Level 1"),
        question(5, "l1-g1", "Useful item included in the Level 1 cost"),
        question(6, "l1-g1", "What participants receive at the end of Level 1"),
    ]

    g2 = group(
        "l1-g2", "Questions 7–10",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(7, 11)), layout="notes", body=[
            "# General information",
            "• Participants must be able to swim.",
            "• Bring suitable clothing, a {{7}} and toiletries (e.g. shampoo).",
            "• There is a {{8}} at the club.",
            "• Online training {{9}} are recommended.",
            "• {{10}} are available for course participants.",
        ],
    )
    qs += [
        question(7, "l1-g2", "Item to bring with toiletries"),
        question(8, "l1-g2", "Facility at the club"),
        question(9, "l1-g2", "Recommended online training material"),
        question(10, "l1-g2", "What is available for course participants"),
    ]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "A sailing course enquiry",
        "context": "A telephone conversation between a man and a woman about sailing courses at Oyster Bay Sailing Club.",
        "groups": [g1, g2], "questions": qs,
        "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    g3 = group(
        "l2-g1", "Questions 11–16",
        "Choose the correct letter, A, B or C.",
        list(range(11, 17)),
    )
    mcq = [
        (11, "What should trainees always expect to get when working on low budget short films?",
         ["travel expenses", "a minimum wage", "meals"]),
        (12, "According to the speaker, on big budget films trainees may get experience of",
         ["makeup for special effects.", "working with different ethnicities.", "creating a variety of hair styles."]),
        (13, "The speaker says a problem for makeup artists is",
         ["dealing with difficult directors.", "being shouted at by their supervisor.", "waiting around for hours doing nothing."]),
        (14, "How did the speaker feel when she met famous actors for the first time?",
         ["very shy", "very proud", "very disappointed"]),
        (15, "What advice does the speaker give about makeup kits?",
         ["Always carry a basic kit with you.", "Only buy the best products for a makeup kit.",
          "Ask other makeup artists to check your kit."]),
        (16, "What advice does the speaker give about creating a portfolio?",
         ["Keep print and digital photos.", "Only include a small selection of photos.",
          "Get permission to use photos."]),
    ]
    qs2 = [question(n, "l2-g1", prompt, "mcq", options) for n, prompt, options in mcq]

    abilities = ["A being well-organised", "B being flexible", "C working quickly"]
    g4 = group(
        "l2-g2", "Questions 17–20",
        "What ability is required for each of the following duties? Write the correct letter, A, B or C, next to Questions 17–20.",
        list(range(17, 21)), layout="match", shared=abilities,
    )
    qs2 += [
        question(17, "l2-g2", "Prepping an actor", "match"),
        question(18, "l2-g2", "Continuity", "match"),
        question(19, "l2-g2", "General", "match"),
        question(20, "l2-g2", "Applying makeup", "match"),
    ]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Working as a makeup trainee",
        "context": "A podcast interview with a makeup artist about how to become a makeup trainee in the film industry.",
        "groups": [g3, g4], "questions": qs2,
        "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    lecture_options = [
        "the references to local problems",
        "the broad focus of the examples",
        "the practical suggestions for solutions",
        "the type of issues discussed",
        "the implications for government policy",
    ]
    g5 = group(
        "l3-g1", "Questions 21 and 22",
        "Choose TWO letters, A–E. Which TWO features of the lecture on ocean biodiversity had the greatest impact on the students?",
        [21, 22],
    )
    qs3 = [
        question(21, "l3-g1", "The first feature that made the greatest impact", "mcq", lecture_options),
        question(22, "l3-g1", "The second feature that made the greatest impact", "mcq", lecture_options),
    ]
    project_options = [
        "the team's previous successes",
        "its wide geographical scale",
        "the use of new technology",
        "the extensive statistical evidence",
        "the large range of specialists involved",
    ]
    g6 = group(
        "l3-g2", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO details about the research project particularly impressed the students?",
        [23, 24],
    )
    qs3 += [
        question(23, "l3-g2", "The first detail that particularly impressed them", "mcq", project_options),
        question(24, "l3-g2", "The second detail that particularly impressed them", "mcq", project_options),
    ]
    opinions = [
        "A This is aimed at a very specialist audience.",
        "B This is now rather outdated.",
        "C This was an effective description of a new danger.",
        "D This suggests possible ways to improve the situation.",
        "E This does not give a balanced account.",
        "F This is too predictable to be useful.",
        "G This gives insufficient evidence for its claims.",
        "H This gives a clear explanation of the problems.",
    ]
    g7 = group(
        "l3-g3", "Questions 25–30",
        "What is the students' opinion of each of the following resources related to ocean biodiversity? Choose SIX answers from the box and write the correct letter, A–H, next to Questions 25–30.",
        list(range(25, 31)), layout="match", shared=opinions,
    )
    resources = [
        (25, "Article on invasive lionfish"), (26, "Documentary on microplastics"),
        (27, "Podcast on ocean pollution"), (28, "Book on coastal ecosystems"),
        (29, "Article on metal toxicity"), (30, "Podcast on floating marine cities"),
    ]
    qs3 += [question(n, "l3-g3", text, "match") for n, text in resources]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "A lecture on ocean biodiversity",
        "context": "Two students, Phil and Lucy, discuss a lecture they attended and a list of resources for a seminar.",
        "groups": [g5, g6, g7], "questions": qs3,
        "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g8 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Sources of rubber",
            "Three resources which are essential for industrial civilisation",
            "• {{31}}",
            "• fossil fuels",
            "• rubber",
            "## Natural rubber",
            "This mainly comes from the Para rubber tree, now cultivated in South-East Asia.",
            "The supply is limited because",
            "• the growth of the tree is {{32}}",
            "• production cannot easily be adjusted because of increasing or decreasing {{33}}",
            "• the tree only grows near the {{34}}",
            "• extracting the latex (rubber) is labour-intensive",
            "• it is very difficult to {{35}} rubber after production.",
            "New threats include",
            "• lack of genetic diversity, leading to danger of disease caused by a {{36}}",
            "• a shift to the cultivation of palm oil",
            "• extreme {{37}} events.",
            "## Synthetic rubber",
            "• may be used for engine parts and cooking utensils",
            "• is less {{38}} than natural rubber",
            "• is unsuitable for many purposes e.g. the tyres of aircraft.",
            "## An alternative source of natural rubber",
            "• A wild flower (a type of dandelion) has rubber in its {{39}}",
            "• It can be grown in many locations and does not require good {{40}}",
        ],
    )
    qs4 = [question(n, "l4-g1", f"Note completion {n}") for n in range(31, 41)]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Sources of rubber",
        "context": "A lecture about natural and synthetic rubber and a possible alternative source.",
        "groups": [g8], "questions": qs4,
        "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 --------------------------------------------------------------
    p1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–7",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(1, 8)), layout="notes", body=[
            "# Gwendoline and Margaret Davies",
            "## Family and early life",
            "• their grandfather's wealth came from {{1}} and transportation businesses",
            "• their upbringing gave them a sense of social responsibility",
            "• their {{2}} was designed to give them an interest in activities such as collecting art",
            "• their governess took them on trips to art galleries",
            "• they took lengthy {{3}} about the things they saw in art galleries",
            "## The sisters as art collectors",
            "• their {{4}} showed they liked Old Master paintings, but they were expensive to buy",
            "• their early purchases were safe, popular paintings",
            "• the first Impressionist paintings they bought showed places in {{5}}",
            "## Impact of First World War",
            "• they helped bring artists from Belgium to Wales",
            "• they worked in a {{6}} for soldiers in France",
            "## Opinions about the sisters as art collectors",
            "• were not considered typical collectors – they lived in isolation in the countryside and did not have any {{7}} who were artists",
        ],
    )
    qs1 = [question(n, "r1-g1", f"Notes completion {n}") for n in range(1, 8)]

    g2 = group(
        "r1-g2", "Questions 8–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(8, 14)),
    )
    statements = [
        "The Davies sisters' childhood influenced the way they decided to use their wealth.",
        "The Jean-Baptiste-Camille Corot paintings in the Davies sisters' collection were purchased from a gallery in France.",
        "Hugh Blaker opposed the Davies sisters' decision to buy art by French Impressionists.",
        "The exhibition of Cezanne paintings at the Bath gallery was very popular with the public.",
        "The impact of the First World War encouraged Gwendoline to reconsider her interest in collecting art.",
        "The Davies sisters bought French Impressionist art during a period when very few people were doing so.",
    ]
    qs1 += [question(n, "r1-g2", text, "tfng") for n, text in zip(range(8, 14), statements)]
    apply_keys(qs1, keys["reading"], "r1")
    p1["groups"] = [g1, g2]
    p1["questions"] = qs1
    reading.append(p1)

    # Passage 2 --------------------------------------------------------------
    p2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–17",
        "Reading Passage 2 has seven sections, A–G. Which section contains the following information? Write the correct letter, A–G, in boxes 14–17 on your answer sheet.",
        list(range(14, 18)), layout="match", shared=["A", "B", "C", "D", "E", "F", "G"],
    )
    info = [
        "examples of strategies to decrease the noise that the public are exposed to",
        "data indicating the extent of the problem of excessive noise",
        "a description of physiological changes in our bodies when we hear sudden noises",
        "evidence that a relatively quiet environment can be more beneficial than a totally silent one",
    ]
    qs2 = [question(n, "r2-g1", text, "match") for n, text in zip(range(14, 18), info)]

    g4 = group(
        "r2-g2", "Questions 18–21",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(18, 22)), layout="summary", body=[
            "# Flotation Tanks",
            "According to Justin Feinstein, flotation tanks allow people to concentrate on their own {{18}}, which helps them relax and enables them to meditate.",
            "Feinstein and his colleagues conducted an experiment in which 50 people, who were all suffering from stress and related issues, were given a {{19}} to complete before and after using a flotation tank. Participants reported a reduction in their symptoms after an hour in the tank, together with signs of relaxation and improved general {{20}}.",
            "In another experiment, the researchers had 48 people spend periods of 90 minutes either lying back in a chair or floating in a tank. Brain scans then revealed that those people who had been in a tank had decreased activity in parts of the brain associated with {{21}}.",
        ],
    )
    qs2 += [question(n, "r2-g2", f"Summary completion {n}") for n in range(18, 22)]

    people = ["A Nick Antonio", "B Justin Feinstein", "C Tai Dotan Ben-Soussan", "D Eric Pfeifer"]
    g5 = group(
        "r2-g3", "Questions 22–26",
        "Look at the following statements and the list of people below. Match each statement with the correct person, A, B, C or D. NB You may use any letter more than once.",
        list(range(22, 27)), layout="match", shared=people,
    )
    stmts = [
        "It is unpleasant and upsetting for people to be placed in a silent environment against their will.",
        "The trend towards creating quieter urban locations is likely to increase in the coming years.",
        "When our body's senses are completely deprived of input, our minds compensate for this by creating the illusion of images and sounds.",
        "Even a short amount of silent time can have a positive impact.",
        "External and internal quietness makes us more conscious of events occurring in our surroundings and helps us react appropriately to these events.",
    ]
    qs2 += [question(n, "r2-g3", text, "match") for n, text in zip(range(22, 27), stmts)]
    apply_keys(qs2, keys["reading"], "r2")
    p2["groups"] = [g3, g4, g5]
    p2["questions"] = qs2
    reading.append(p2)

    # Passage 3 --------------------------------------------------------------
    p3 = passage(3, passages["3"])
    g6 = group(
        "r3-g1", "Questions 27–30",
        "Choose the correct letter, A, B, C or D.",
        list(range(27, 31)),
    )
    mcq = [
        (27, "What does the reviewer suggest about the cultivation and trading of sugar in the first paragraph?",
         ["Sugar has played a major role in international relations.",
          "Beet sugar has been made more internationally competitive.",
          "Cane sugar is thought to be of superior quality to beet sugar.",
          "New locations for cultivating sugar have increased production."]),
        (28, "In the second paragraph, when discussing the sugar market in Britain, the reviewer stresses",
         ["how the sources used changed over time.", "how developments in agriculture affected trade.",
          "the increased demand for sugar over the years.", "the growing support for ethical methods of cultivation."]),
        (29, "What is the reviewer doing in the third paragraph?",
         ["describing an efficient approach to sugar cultivation", "explaining why the use of sugar plantations declined",
          "addressing a misconception about the growing of sugar cane", "evaluating different approaches to the cultivation of sugar cane"]),
        (30, "In the final paragraph, what does the reviewer suggest is the overall message of Bosma's book?",
         ["Sugar is a harmful and unnecessary product.", "Economic pressure is needed to control sugar production.",
          "Conditions for workers in sugar production should be improved.",
          "Intensive marketing of sugar has had disastrous consequences."]),
    ]
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in mcq]

    words = [
        "A national governments", "B agricultural developments", "C less wealthy nations",
        "D untrained workers", "E small-scale cultivation", "F outdated methods",
        "G financial controls", "H migrant workers", "I powerful individuals and businesses",
    ]
    g7 = group(
        "r3-g2", "Questions 31–36",
        "Complete the summary using the list of words, A–I, below.",
        list(range(31, 37)), layout="summary", shared=words, body=[
            "# Sugar cultivation and production",
            "The book The World of Sugar points out the similarities in the way that sugar was cultivated around the world. In the big industries in both Germany and the US, sugar farming depended on {{31}}. However, in other parts of the world such as South Asia and Latin America, {{32}} continued.",
            "Sugar production has also involved {{33}} who were eager to protect their markets. In countries such as Cuba the sugar industry therefore had a major influence on {{34}}.",
            "To support the interests of sugar producers, {{35}} were established. As a result of this, {{36}} were penalised.",
        ],
    )
    qs3 += [question(n, "r3-g2", f"Summary completion {n}", "select") for n in range(31, 37)]

    g8 = group(
        "r3-g3", "Questions 37–40",
        "Do the following statements agree with the views of the writer in Reading Passage 3? Write YES if the statement agrees with the views of the writer, NO if the statement contradicts the views of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(37, 41)),
    )
    yn = [
        "Sugar has now become available in large quantities due to a range of agricultural developments.",
        "Advertisers initially marketed sugar as a luxury product.",
        "The invention of high-fructose corn syrup was a positive development.",
        "High-fructose corn syrup is an ingredient in many processed foods.",
    ]
    qs3 += [question(n, "r3-g3", text, "ynng") for n, text in zip(range(37, 41), yn)]
    apply_keys(qs3, keys["reading"], "r3")
    p3["groups"] = [g6, g7, g8]
    p3["questions"] = qs3
    reading.append(p3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The graph below gives information about the number of jobs in four sectors of the economy in the US between 1960 and 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/cambridge21/test1-writing-task1.jpg",
            "figureAlt": "Line graph showing the number of jobs in manufacturing, retail, agriculture and healthcare in the US from 1960 to 2020.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "The best way to provide enough homes in large cities is to build tall apartment blocks.\n\nTo what extent do you agree or disagree with this statement?",
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
                {"id": "s1", "text": "Where do you go to get a haircut?"},
                {"id": "s2", "text": "Have you changed your hairstyle recently?"},
                {"id": "s3", "text": "Would you ever change the colour of your hair?"},
                {"id": "s4", "text": "Do you enjoy going to the hairdresser or barber?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a time when you used information for tourists, for example from a guidebook or online.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a time when you used information for tourists, for example from a guidebook or online.",
                "bullets": ["where you got this information", "what place this information was about",
                            "what information you got"],
                "rounding": "and explain whether this information was very helpful for you.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: different types of holidays and tourist attractions.",
            "questions": [
                {"id": "s5", "text": "Different types of holidays. What are the most popular kinds of holidays for people from your country to go on?"},
                {"id": "s6", "text": "Do you think most people prefer to have a holiday abroad rather than in their own country?"},
                {"id": "s7", "text": "Why do some people want to do absolutely nothing when they go away on holiday?"},
                {"id": "s8", "text": "Tourist attractions. What are the kinds of tourist attraction that visitors to your country like to see?"},
                {"id": "s9", "text": "Do you think tourist attractions such as museums should be free for local people to visit?"},
                {"id": "s10", "text": "What can make a tourist attraction disappointing for visitors?"},
            ],
        },
    ]

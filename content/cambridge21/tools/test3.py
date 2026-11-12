"""Cambridge IELTS 21 — Academic Test 3."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "cambridge21-test3",
        "title": "Cambridge IELTS 21 · Academic Test 3",
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
        "Complete the notes below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 11)), layout="notes", body=[
            "# Ferry to Shetland Islands",
            "• Name of ferry company: {{1}} Ferries",
            "• Ferries depart seven times per {{2}} in summer",
            "• Cost for four people with car: a little less than £{{3}}",
            "• Cancellation policy: receive a {{4}} (if cancelled a month in advance)",
            "## Advice",
            "• Cabins: book one with a {{5}}",
            "• luxury cabins have a TV",
            "• Bring snacks and {{6}} for the children",
            "• A {{7}} is required for the dog kennels",
            "• Try to see {{8}} in the morning",
            "• If time, visit {{9}} Castle",
            "• The {{10}} restaurant in a nearby village is recommended",
        ],
    )
    qs = [question(n, "l1-g1", f"Ferry notes {n}") for n in range(1, 11)]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "A ferry booking to the Shetland Islands",
        "context": "A telephone conversation about booking a ferry to the Shetland Islands.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 -----------------------------------------------------------------
    popular = ["low price", "locally sourced", "freshly made", "convenience", "unusual food"]
    g2 = group(
        "l2-g1", "Questions 11 and 12",
        "Choose TWO letters, A–E. Which TWO explanations for the popularity of street food are given?",
        [11, 12],
    )
    qs2 = [
        question(11, "l2-g1", "The first explanation", "mcq", popular),
        question(12, "l2-g1", "The second explanation", "mcq", popular),
    ]
    places = ["music festivals", "food markets", "weddings", "parties", "parks"]
    g3 = group(
        "l2-g2", "Questions 13 and 14",
        "Choose TWO letters, A–E. Which TWO places are recommended for new street food businesses?",
        [13, 14],
    )
    qs2 += [
        question(13, "l2-g2", "The first recommended place", "mcq", places),
        question(14, "l2-g2", "The second recommended place", "mcq", places),
    ]
    g4 = group("l2-g3", "Questions 15–16", "Choose the correct letter, A, B or C.", [15, 16])
    qs2 += [
        question(15, "l2-g3", "What does the speaker say about getting equipment for a street food business?", "mcq",
                 ["High quality equipment is a good investment.", "It's best to buy second-hand equipment.",
                  "Renting equipment can be cheap."]),
        question(16, "l2-g3", "What advice is given about creating a product for a street food business?", "mcq",
                 ["Provide information about the ingredients.", "It is important to have an original product.",
                  "The presentation is an important factor."]),
    ]
    problems = ["A Some ingredients were too expensive.", "B The meals took a long time to prepare.",
                "C They had no money for marketing.", "D It was difficult to get a permit to sell food.",
                "E A competitor was selling similar food in their area.", "F They worked very long hours."]
    g5 = group(
        "l2-g4", "Questions 17–20",
        "What problem did the owners of each of the following street food businesses experience? Choose FOUR answers from the box and write the correct letter, A–F, next to Questions 17–20.",
        list(range(17, 21)), layout="match", shared=problems,
    )
    businesses = [(17, "Thai Basil"), (18, "Basque"), (19, "Lou's kitchen"), (20, "Chip Chop")]
    qs2 += [question(n, "l2-g4", name, "match") for n, name in businesses]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Street food businesses",
        "context": "A talk about setting up a street food business, including advice from established owners.",
        "groups": [g2, g3, g4, g5], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 -----------------------------------------------------------------
    terms = ["Their definitions keep changing.", "People think they mean the same thing.",
             "The term 'eco-friendly' is preferable.", "They are often used imprecisely.",
             "Companies should avoid using them on clothing labels."]
    g6 = group(
        "l3-g1", "Questions 21 and 22",
        "Choose TWO letters, A–E. Which TWO points do the speakers make about the terms 'ethical' and 'sustainable' fashion?",
        [21, 22],
    )
    qs3 = [
        question(21, "l3-g1", "The first point", "mcq", terms),
        question(22, "l3-g1", "The second point", "mcq", terms),
    ]
    wool = ["Sheep are generally well-treated.", "Wool is easy to recycle.", "Wool is a long-lasting fabric.",
            "Wool production involves few chemicals.",
            "Sheep do less environmental damage than other livestock."]
    g7 = group(
        "l3-g2", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO claims about wool production do the speakers disagree with?",
        [23, 24],
    )
    qs3 += [
        question(23, "l3-g2", "The first claim they disagree with", "mcq", wool),
        question(24, "l3-g2", "The second claim they disagree with", "mcq", wool),
    ]
    comments = [
        "A The production process is fuel efficient.", "B It is the least sustainable of alternative fabrics.",
        "C Production costs are high.", "D It provides additional health benefits.",
        "E It is not durable in the long-term.",
        "F It needs to be produced in a certain way to be sustainable.",
        "G Chemicals required for production can be reused.", "H This is from a wholly sustainable source.",
    ]
    g8 = group(
        "l3-g3", "Questions 25–30",
        "What comment do the speakers make about each of the following semi-synthetic fabrics? Choose SIX answers from the box and write the correct letter, A–H, next to Questions 25–30.",
        list(range(25, 31)), layout="match", shared=comments,
    )
    fabrics = [(25, "Lyocell"), (26, "Cupro"), (27, "Bamboo"), (28, "EcoVero"), (29, "Cork"), (30, "Hemp")]
    qs3 += [question(n, "l3-g3", name, "match") for n, name in fabrics]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Ethical and sustainable fashion",
        "context": "Two students discuss a project on ethical and sustainable fashion.",
        "groups": [g6, g7, g8], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 -----------------------------------------------------------------
    g9 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Invasive species",
            "Definition: an animal or plant that causes harm to an environment after being introduced by humans",
            "## An invasive species can be a problem when it:",
            "• eats native species.",
            "• introduces a new {{31}}",
            "• takes food from native species.",
            "• threatens an entire {{32}}",
            "## How invasive species spread",
            "• accidentally e.g. via people returning from their {{33}} or on cargo ships",
            "• intentionally e.g. for pest control, or as {{34}}",
            "## Examples of invasive species",
            "• Rhinella marina (toads)",
            "  – were introduced to Australia from Hawaii in 1935 to eat a type of insect that was damaging the {{35}} plantations.",
            "  – failed to solve the problem and became widespread in the north of Australia.",
            "  – are poisonous for any species that eats them and reduce the food available for native frogs.",
            "• Japanese knotweed plants were popular among 19th-century gardeners in the UK.",
            "• Rhododendron plants prevent {{36}} from reaching native plants.",
            "• Grey squirrels from N. America reduce sources of food for the UK's native red squirrels and spread a {{37}} that kills red squirrels.",
            "## Tackling invasive species",
            "• Monitoring helps us to understand the {{38}} of invasive species and the impact they have.",
            "• Setting up a national {{39}} makes it easier to track them.",
            "• Asking the public to {{40}} and report them helps with monitoring.",
        ],
    )
    qs4 = [question(n, "l4-g1", f"Invasive species notes {n}") for n in range(31, 41)]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Invasive species",
        "context": "A lecture about invasive species, how they spread and how they can be controlled.",
        "groups": [g9], "questions": qs4, "transcript": transcripts["4"],
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
            "# The saiga",
            "## Adaptations",
            "• has a large bulbous nose with swollen nostrils that:",
            "  – keep {{1}} out",
            "  – lower the temperature of its {{2}} in summer",
            "  – warm the air entering its lungs in winter",
            "• grows a thick {{3}} in winter, which it loses in spring",
            "## Reasons for population decline",
            "• poaching, especially for the {{4}} of male saiga",
            "• expansion of farms and settlements, causing:",
            "  – reduction in the size of the saiga's {{5}}",
            "  – loss of access to the {{6}} which they use for migration",
            "• various forms of disease, leading to mass mortality events",
            "• climate change, causing the disappearance of {{7}} which the saiga relied on",
        ],
    )
    qs1 = [question(n, "r1-g1", f"Saiga notes {n}") for n in range(1, 8)]

    g2 = group(
        "r1-g2", "Questions 8–13",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(8, 14)),
    )
    statements = [
        "Today, numbers of saiga are distributed evenly across four nations in Central Asia: Kazakhstan, Russia, Mongolia and Uzbekistan.",
        "For most of the 20th century, the population of saiga were falling.",
        "Efforts to protect rhinos in Africa had a significant effect on saiga populations.",
        "Unpredictable fluctuations in climate are threatening the wildlife of Central Asia more than in other parts of the world.",
        "The Altyn Dala Conservation Initiative was formed for the benefit of a number of different animals.",
        "The Altyn Dala Conservation Initiative's recognition as a World Restoration Flagship project attracted additional international funding for the scheme.",
    ]
    qs1 += [question(n, "r1-g2", text, "tfng") for n, text in zip(range(8, 14), statements)]
    apply_keys(qs1, keys["reading"], "r1")
    p1["groups"] = [g1, g2]
    p1["questions"] = qs1
    reading.append(p1)

    # Passage 2 --------------------------------------------------------------
    p2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–18",
        "Do the following statements agree with the information given in Reading Passage 2? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(14, 19)),
    )
    statements = [
        "The population of Dar es Salaam is rising more rapidly than was previously predicted.",
        "Most of the residents of Dar es Salaam live in high-rise blocks on the edge of the city.",
        "Residents have been consulted about their views on the suburban rail line in Dar es Salaam.",
        "The majority of the present residential development in Dar es Salaam is unplanned.",
        "Dar es Salaam's authorities have decided to follow the public transport plan adopted by a large number of African cities.",
    ]
    qs2 = [question(n, "r2-g1", text, "tfng") for n, text in zip(range(14, 19), statements)]

    g4 = group(
        "r2-g2", "Questions 19–26",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(19, 27)), layout="notes", body=[
            "# Dar es Salaam's DART Bus Rapid Transit system",
            "## Features",
            "• the buses use designated {{19}} to cut down on delays",
            "• passengers pay fares before {{20}}",
            "• passengers in {{21}} can use every part of the system",
            "## Problems",
            "• the temperature control is sometimes not activated in order to reduce {{22}} use",
            "• insufficient number of vehicles are available due to the effects of a severe {{23}}",
            "• passengers are unable to use {{24}} because some equipment is out of action",
            "• tickets have to be checked manually at station {{25}}",
            "• {{26}} frequently build up during rush hours",
        ],
    )
    qs2 += [question(n, "r2-g2", f"DART notes {n}") for n in range(19, 27)]
    apply_keys(qs2, keys["reading"], "r2")
    p2["groups"] = [g3, g4]
    p2["questions"] = qs2
    reading.append(p2)

    # Passage 3 --------------------------------------------------------------
    p3 = passage(3, passages["3"])
    g5 = group("r3-g1", "Questions 27–30", "Choose the correct letter, A, B, C or D.", list(range(27, 31)))
    mcq = [
        (27, "What is the writer doing in the second paragraph?",
         ["pinpointing some key changes in our understanding of prehistory",
          "outlining some aspects of prehistory which are still poorly understood",
          "summarising some attitudes towards recent archaeological revelations",
          "giving an overview of some current disagreements among archaeologists"]),
        (28, "In the sixth paragraph, the writer mentions mobile phones to make the point that",
         ["most developments happen in a gradual way.", "innovation can come from a variety of sources.",
          "not all technological advancements are positive.", "the path of evolution can often be unpredictable."]),
        (29, "In the seventh paragraph, the phrase 'unpick this stuff' refers to the task of",
         ["assessing the impact of certain recent research findings.",
          "questioning the authenticity of evidence used in earlier research.",
          "conducting research into how prehistoric societies were organised.",
          "reevaluating research influenced by outdated beliefs about society."]),
        (30, "What does the writer suggest in the final paragraph?",
         ["Studying past societies could help us create a fairer society today.",
          "We should not judge past societies by the standards of modern society.",
          "We still have much to learn about how societies have evolved over history.",
          "There is more than one way to interpret evidence about societies in prehistoric times."]),
    ]
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in mcq]

    endings = [
        "A Homo sapiens emerged at an earlier point in time than experts previously believed.",
        "B previous assumptions about who had power in the prehistoric world were inaccurate.",
        "C gender roles in extinct hominin species were different from those in Homo sapiens societies.",
        "D experts may have been mistaken about who looked for food in early human communities.",
        "E Homo sapiens was probably not the only species capable of sophisticated workmanship.",
        "F other species managed to survive in harsh environments before the arrival of Homo sapiens.",
    ]
    g6 = group(
        "r3-g2", "Questions 31–34",
        "Complete each sentence with the correct ending, A–F, below.",
        list(range(31, 35)), layout="match", shared=endings,
    )
    sentence_starts = [
        "The findings at Kalambo Falls revealed that",
        "Evidence from high-altitude regions suggests that",
        "An academic publication from June 2023 shows that",
        "Analysis of a 4000-year-old Iberian leader indicates that",
    ]
    qs3 += [question(n, "r3-g2", text, "match") for n, text in zip(range(31, 35), sentence_starts)]

    g7 = group(
        "r3-g3", "Questions 35–40",
        "Do the following statements agree with the views of the writer in Reading Passage 3? Write YES if the statement agrees with the views of the writer, NO if the statement contradicts the views of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(35, 41)),
    )
    yn = [
        "It seems likely that the Neanderthals' cave paintings were the first examples of artwork ever created.",
        "It is very rare to find prehistoric artwork carved onto shells.",
        "The methods which the researchers used to examine the Rising Star cave system were rather unconventional.",
        "It is unclear how old the etchings in the Rising Star cave system are.",
        "The means used to publicise the findings from the Rising Star cave system added to the controversy that surrounds them.",
        "The size of H. naledi brains is a key factor in the question of whether these hominins were able to produce art.",
    ]
    qs3 += [question(n, "r3-g3", text, "ynng") for n, text in zip(range(35, 41), yn)]
    apply_keys(qs3, keys["reading"], "r3")
    p3["groups"] = [g5, g6, g7]
    p3["questions"] = qs3
    reading.append(p3)
    return reading


def build_writing():
    return [
        {
            "id": "writing-task-1", "number": 1, "title": "Writing Task 1",
            "prompt": "The diagram below shows how one type of desert, known as a rain-shadow desert, is formed.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/cambridge21/test3-writing-task1.jpg",
            "figureAlt": "Diagram showing seven numbered stages in the formation of a rain-shadow desert, from winds approaching the coast to dry winds reaching inland areas.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "All university undergraduate courses should include a period of time spent studying abroad or doing a work placement.\n\nDo you think the advantages of this would outweigh the disadvantages?",
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
                {"id": "s1", "text": "When you go shopping, do you usually pay for things by cash or by card?"},
                {"id": "s2", "text": "Are you generally careful about how much money you spend?"},
                {"id": "s3", "text": "Have you ever spent money on something you didn't need?"},
                {"id": "s4", "text": "How important is it to you to save money for the future?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe an interesting garden or park you have seen.",
            "questions": [],
            "cueCard": {
                "topic": "Describe an interesting garden or park you have seen.",
                "bullets": ["where this garden or park is", "how big it is", "what you saw in this garden/park"],
                "rounding": "and explain why you think this garden/park is interesting.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: homes and gardens; gardening as a hobby.",
            "questions": [
                {"id": "s5", "text": "Homes and gardens. What are the advantages of having a home with a garden?"},
                {"id": "s6", "text": "How could people living in apartment blocks grow plants and vegetables?"},
                {"id": "s7", "text": "How interested are people in your country in TV shows and magazines about gardens?"},
                {"id": "s8", "text": "Gardening as a hobby. Do you think that gardening is a hobby mainly for older people?"},
                {"id": "s9", "text": "What are the benefits for people of gardening as a hobby?"},
                {"id": "s10", "text": "Will gardening be a more popular hobby in the future?"},
            ],
        },
    ]

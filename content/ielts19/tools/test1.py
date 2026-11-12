"""IELTS 19 Academic - Test 1."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts19-test1",
        "title": "IELTS 19 · Academic Test 1",
        "module": "Academic",
        "version": "ielts19.1",
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
        "l1-g1", "Questions 1–10",
        "Complete the notes below. Write ONE WORD AND/OR A NUMBER for each answer.",
        list(range(1, 11)), layout="notes", body=[
            "# Hinchingbrooke Country Park",
            "## The park",
            "• Area: {{1}} hectares",
            "• Habitats: wetland, grassland and woodland",
            "• Wetland: lakes, ponds and a {{2}}",
            "• Wildlife includes birds, insects and animals",
            "## Subjects studied in educational visits include",
            "• Science: Children look at {{3}} about plants, etc.",
            "• Geography: includes learning to use a {{4}} and compass",
            "• History: changes in land use",
            "• Leisure and tourism: mostly concentrates on the park's {{5}}",
            "• Music: Children make {{6}} with natural materials, and experiment with rhythm and speed.",
            "## Benefits of outdoor educational visits",
            "• They give children a feeling of {{7}} that they may not have elsewhere.",
            "• Children learn new {{8}} and gain self-confidence.",
            "## Practical issues",
            "• Cost per child: £{{9}}",
            "• Adults, such as {{10}}, free",
        ])
    qs = [question(n, "l1-g1", prompt) for n, prompt in [
        (1, "Size of the park in hectares"),
        (2, "Wetland feature besides lakes and ponds"),
        (3, "What children look at in Science"),
        (4, "What Geography teaches children to use, besides a compass"),
        (5, "What Leisure and tourism concentrates on"),
        (6, "What children make with natural materials in Music"),
        (7, "Feeling outdoor visits give children"),
        (8, "What children learn and gain self-confidence from"),
        (9, "Cost per child"),
        (10, "Adults such as these are free"),
    ]]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "Hinchingbrooke Country Park",
        "context": "A teaching assistant telephones a country park to arrange a school visit.",
        "groups": [g1], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 ---------------------------------------------------------------
    g2 = group("l2-g1", "Questions 11–15", "Choose the correct letter, A, B or C.", list(range(11, 16)))
    mcq = [
        (11, "During the visit to Malatte, in France, members especially enjoyed",
         ["going to a theme park.", "experiencing a river trip.", "visiting a cheese factory."]),
        (12, "What will happen in Stanthorpe to mark the 25th anniversary of the Twinning Association?",
         ["A tree will be planted.", "A garden seat will be bought.", "A footbridge will be built."]),
        (13, "Which event raised most funds this year?",
         ["the film show", "the pancake evening", "the cookery demonstration"]),
        (14, "For the first evening with the French visitors, host families are advised to",
         ["take them for a walk round the town.", "go to a local restaurant.", "have a meal at home."]),
        (15, "On Saturday evening there will be the chance to",
         ["listen to a concert.", "watch a match.", "take part in a competition."]),
    ]
    qs2 = [question(n, "l2-g1", prompt, "mcq", options) for n, prompt, options in mcq]
    g3 = group(
        "l2-g2", "Questions 16–20",
        "Label the map below. Write the correct letter, A–H, next to Questions 16–20.",
        list(range(16, 21)), layout="map",
        figure="/media/figures/ielts19/test1-listening-map.jpg",
        figureAlt="A map of Farley House and its grounds, with locations labelled A to H.",
    )
    qs2 += [question(n, "l2-g2", prompt, "map") for n, prompt in [
        (16, "Farm shop"), (17, "Disabled entry"), (18, "Adventure playground"),
        (19, "Kitchen gardens"), (20, "The Temple of the Four Winds"),
    ]]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Stanthorpe Twinning Association",
        "context": "A talk about a town-twinning association and an upcoming visit from France.",
        "groups": [g2, g3], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 ---------------------------------------------------------------
    bread = [
        "receiving support from local restaurants",
        "finding a good way to prevent waste",
        "overcoming problems in a basic process",
        "experimenting with designs and colours",
        "learning how to apply 3-D printing",
    ]
    g4 = group(
        "l3-g1", "Questions 21 and 22",
        "Choose TWO letters, A–E. Which TWO things did Colin find most satisfying about his bread reuse project?",
        [21, 22],
    )
    qs3 = [
        question(21, "l3-g1", "First satisfying thing about the bread reuse project", "mcq", bread),
        question(22, "l3-g1", "Second satisfying thing about the bread reuse project", "mcq", bread),
    ]
    sensors = [
        "for use on medical products",
        "to show that food is no longer fit to eat",
        "for use with drinks as well as foods",
        "to provide applications for blind people",
        "to indicate the weight of certain foods",
    ]
    g5 = group(
        "l3-g2", "Questions 23 and 24",
        "Choose TWO letters, A–E. Which TWO ways do the students agree that touch-sensitive sensors for food labels could be developed in future?",
        [23, 24],
    )
    qs3 += [
        question(23, "l3-g2", "First future development of touch-sensitive food labels", "mcq", sensors),
        question(24, "l3-g2", "Second future development of touch-sensitive food labels", "mcq", sensors),
    ]
    opinions = [
        "A This is only relevant to young people.",
        "B This may have disappointing results.",
        "C This already seems to be widespread.",
        "D Retailers should do more to encourage this.",
        "E More financial support is needed for this.",
        "F Most people know little about this.",
        "G There should be stricter regulations about this.",
        "H This could be dangerous.",
    ]
    g6 = group(
        "l3-g3", "Questions 25–30",
        "What is the students' opinion about each of the following food trends? Choose SIX answers from the box and write the correct letter, A–H, next to Questions 25–30.",
        list(range(25, 31)), layout="match", shared=opinions,
    )
    qs3 += [question(n, "l3-g3", prompt, "match") for n, prompt in [
        (25, "Use of local products"),
        (26, "Reduction in unnecessary packaging"),
        (27, "Gluten-free and lactose-free food"),
        (28, "Use of branded products related to celebrity chefs"),
        (29, "Development of 'ghost kitchens' for takeaway food"),
        (30, "Use of mushrooms for common health concerns"),
    ]]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "Food projects and trends",
        "context": "Two students discuss a bread reuse project and predictions about food trends.",
        "groups": [g4, g5, g6], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 ---------------------------------------------------------------
    g7 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Céide Fields",
            "• an important Neolithic archaeological site in the northwest of Ireland",
            "## Discovery",
            "• In the 1930s, a local teacher realised that stones beneath the bog surface were once {{31}}.",
            "• His {{32}} became an archaeologist and undertook an investigation of the site.",
            "  – a traditional method used by local people to dig for {{33}} was used to identify where stones were located.",
            "  – carbon dating later proved the site was Neolithic.",
            "• Items are well preserved in the bog because of a lack of {{34}}.",
            "## Neolithic farmers",
            "• Houses were {{35}} in shape and had a hole in the roof.",
            "• Neolithic innovations include:",
            "  – cooking indoors",
            "  – pots used for storage and to make {{36}}",
            "• Each field at Céide was large enough to support a big {{37}}.",
            "• The fields were probably used to restrict the grazing of animals – no evidence of structures to house them during {{38}}.",
            "## Reasons for the decline in farming",
            "• A decline in {{39}} quality",
            "• An increase in {{40}}",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "What the stones beneath the bog were once used for"),
        (32, "Relative of the local teacher who became an archaeologist"),
        (33, "What the traditional digging method was used to find"),
        (34, "What the bog lacked, preserving the items"),
        (35, "Shape of the Neolithic houses"),
        (36, "What pots were used to make besides storing food"),
        (37, "Size of the family each field could support"),
        (38, "Season when animals had no structures for shelter"),
        (39, "Type of quality that declined"),
        (40, "What increased, causing farming to decline"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Céide Fields",
        "context": "A lecture about the discovery and investigation of the Céide Fields.",
        "groups": [g7], "questions": qs4, "transcript": transcripts["4"],
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
    qs = [
        question(1, "r1-g1", "People had expected Andy Murray to become the world's top tennis player for at least five years before 2016.", "tfng"),
        question(2, "r1-g1", "The change that Andy Murray made to his rackets attracted a lot of attention.", "tfng"),
        question(3, "r1-g1", "Most of the world's top players take a professional racket stringer on tour with them.", "tfng"),
        question(4, "r1-g1", "Mike and Bob Bryan use rackets that are light in comparison to the majority of rackets.", "tfng"),
        question(5, "r1-g1", "Werner Fischer played with a spaghetti-strung racket that he designed himself.", "tfng"),
        question(6, "r1-g1", "The weather can affect how professional players adjust the strings on their rackets.", "tfng"),
        question(7, "r1-g1", "It was believed that the change Pete Sampras made to his rackets contributed to his strong serve.", "tfng"),
    ]
    g2 = group(
        "r1-g2", "Questions 8–13",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(8, 14)), layout="notes", body=[
            "# The tennis racket and how it has changed",
            "• Mike and Bob Bryan made changes to the types of {{8}} used on their racket frames.",
            "• Players were not allowed to use the spaghetti-strung racket because of the amount of {{9}} it created.",
            "• Changes to rackets can be regarded as being as important as players' diets or the {{10}} they do.",
            "• All rackets used to have natural strings made from the {{11}} of animals.",
            "• Pete Sampras had metal {{12}} put into the frames of his rackets.",
            "• Gonçalo Oliveira changed the {{13}} on his racket handles.",
        ])
    qs += [question(n, "r1-g2", prompt) for n, prompt in [
        (8, "Types of finish changed on the Bryan brothers' racket frames"),
        (9, "What the spaghetti-strung racket created too much of"),
        (10, "Racket changes are as important as diet or this activity"),
        (11, "Animal part used to make natural strings"),
        (12, "Metal items added to Sampras's racket frames"),
        (13, "Part of the handle that Oliveira changed"),
    ]]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 ------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–19",
        "Reading Passage 2 has seven paragraphs, A–G. Which paragraph contains the following information? Write the correct letter, A–G. NB You may use any letter more than once.",
        list(range(14, 20)), layout="match", shared=list("ABCDEFG"),
    )
    qs2 = [question(n, "r2-g1", prompt, "match") for n, prompt in [
        (14, "a reference to a denial of involvement in piracy"),
        (15, "details of how a campaign to eradicate piracy was carried out"),
        (16, "a mention of the circumstances in which states in the ancient world would make use of pirates"),
        (17, "a reference to how people today commonly view pirates"),
        (18, "an explanation of how some people were encouraged not to return to piracy"),
        (19, "a mention of the need for many sailing vessels to stay relatively close to land"),
    ]]
    inhabitants = [
        "They often used stolen vessels to carry out pirate attacks.",
        "They managed to escape capture by the authorities because they knew the area so well.",
        "They paid for information about the routes merchant ships would take.",
        "They depended more on the sea for their livelihood than on farming.",
        "They stored many of the goods taken in pirate attacks in coves along the coastline.",
    ]
    g4 = group(
        "r2-g2", "Questions 20 and 21",
        "Choose TWO letters, A–E. Which TWO of the following statements does the writer make about inhabitants of the Mediterranean region in the ancient world?",
        [20, 21],
    )
    qs2 += [
        question(20, "r2-g2", "First statement about ancient Mediterranean inhabitants", "mcq", inhabitants),
        question(21, "r2-g2", "Second statement about ancient Mediterranean inhabitants", "mcq", inhabitants),
    ]
    greece = [
        "The state estimated that very few people were involved in piracy.",
        "Attitudes towards piracy changed shortly after the Iliad and the Odyssey were written.",
        "Important officials were known to occasionally take part in piracy.",
        "Every citizen regarded pirate attacks on cities as unacceptable.",
        "A favourable view of piracy is evident in certain ancient Greek texts.",
    ]
    g5 = group(
        "r2-g3", "Questions 22 and 23",
        "Choose TWO letters, A–E. Which TWO of the following statements does the writer make about piracy and ancient Greece?",
        [22, 23],
    )
    qs2 += [
        question(22, "r2-g3", "First statement about piracy and ancient Greece", "mcq", greece),
        question(23, "r2-g3", "Second statement about piracy and ancient Greece", "mcq", greece),
    ]
    g6 = group(
        "r2-g4", "Questions 24–26",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(24, 27)), layout="summary", body=[
            "# Ancient Rome and piracy",
            "Piracy was an issue ancient Rome had to deal with, but it also brought some benefits for Rome. For example, pirates supplied slaves that were important for Rome's industries. However, attacks on vessels transporting {{24}} to Rome resulted in calls for {{25}} for the pirates responsible. Nevertheless, piracy continued, with some pirates demanding a {{26}} for the return of the Roman officials they captured.",
        ])
    qs2 += [question(n, "r2-g4", prompt) for n, prompt in [
        (24, "Goods carried by the vessels attacked"),
        (25, "What was demanded for the pirates responsible"),
        (26, "Payment demanded for captured officials"),
    ]]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5, g6]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 ------------------------------------------------------------
    r3 = passage(3, passages["3"])
    g7 = group("r3-g1", "Questions 27–30", "Choose the correct letter, A, B, C or D.", list(range(27, 31)))
    mcq3 = [
        (27, "What point does the writer make about misinformation in the first paragraph?",
         ["Misinformation is a relatively recent phenomenon.", "Some people find it easy to identify misinformation.",
          "Misinformation changes as it is passed from one person to another.", "There may be a number of reasons for the spread of misinformation."]),
        (28, "What does the writer say about the role of technology?",
         ["It may at some point provide us with a solution to misinformation.", "It could fundamentally alter the way in which people regard information.",
          "It has changed the way in which organisations use misinformation.", "It has made it easier for people to check whether information is accurate."]),
        (29, "What is the writer doing in the fourth paragraph?",
         ["comparing the different opinions people have of misinformation", "explaining how the effects of misinformation have changed over time",
          "outlining which issues connected with misinformation are significant today", "describing the attitude of policy makers towards misinformation in the media"]),
        (30, "What point does the writer make about regulation in the USA?",
         ["The guidelines issued by the FDA need to be simplified.", "Regulation does not affect people's opinions of new prescription drugs.",
          "The USA has more regulatory bodies than most other countries.", "Regulation fails to prevent misinformation from appearing in the media."]),
    ]
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in mcq3]
    phrases = [
        "A constant conflict", "B additional evidence", "C different locations", "D experimental subjects",
        "E short period", "F extreme distrust", "G frequent exposure", "H mental operation",
        "I dubious reason", "J different ideas",
    ]
    g8 = group(
        "r3-g2", "Questions 31–36",
        "Complete the summary using the list of phrases, A–J, below.",
        list(range(31, 37)), layout="summary", shared=phrases, body=[
            "# What happens when people encounter misinformation?",
            "Although people have {{31}} to misinformation, there is debate about precisely how and when we label something as true or untrue. The philosophers Descartes and Spinoza had {{32}} about how people engage with information. While Descartes believed that people accept or reject information after considering whether it is true or not, Spinoza argued that people accepted all information they encountered (and by default misinformation) and did not verify or reject it until afterwards. Moreover, Spinoza believed that a distinct {{33}} is involved in these stages. Recent research has provided {{34}} for Spinoza's theory and it would appear that people accept all encountered information as if it were true, even if this is for an extremely {{35}}, and do not label the information as true or false until later. This is consistent with the fact that the resources for scepticism and the resources for perceiving and encoding are in {{36}} in the brain.",
        ])
    qs3 += [question(n, "r3-g2", prompt, "select") for n, prompt in [
        (31, "What people have to misinformation"), (32, "What Descartes and Spinoza had about information engagement"),
        (33, "What Spinoza believed was involved in the stages"), (34, "What recent research has provided for Spinoza's theory"),
        (35, "How long people accept information as true"), (36, "Where the two sets of resources are located"),
    ]]
    g9 = group(
        "r3-g3", "Questions 37–40",
        "Do the following statements agree with the claims of the writer in Reading Passage 3? Write YES if the statement agrees with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(37, 41)),
    )
    qs3 += [question(n, "r3-g3", prompt, "ynng") for n, prompt in [
        (37, "Campaigns designed to correct misinformation will fail to achieve their purpose if people are unable to understand them."),
        (38, "Attempts to teach elementary school students about misinformation have been opposed."),
        (39, "It may be possible to overcome the problem of misinformation in a relatively short period."),
        (40, "The need to keep up with new information is hugely exaggerated in today's world."),
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
            "prompt": "The graph below gives information on the numbers of participants for different activities at one social centre in Melbourne, Australia for the period 2000 to 2020.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts19/test1-writing-task1.jpg",
            "figureAlt": "A line graph showing participant numbers for film club, martial arts, amateur dramatics, table tennis and musical performances from 2000 to 2020.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "Some people think that competition at work, at school and in daily life is a good thing. Others believe that we should try to cooperate more, rather than competing against each other.\n\nDiscuss both these views and give your own opinion.",
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
            "description": "The examiner asks you about international food.",
            "questions": [
                {"id": "s1", "text": "Can you find food from many different countries where you live? [Why/Why not?]"},
                {"id": "s2", "text": "How often do you eat typical food from other countries? [Why/Why not?]"},
                {"id": "s3", "text": "Have you ever tried making food from another country? [Why/Why not?]"},
                {"id": "s4", "text": "What food from your country would you recommend to people from other countries? [Why?]"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a law that was introduced in your country and that you thought was a very good idea.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a law that was introduced in your country and that you thought was a very good idea.",
                "bullets": [
                    "what the law was",
                    "who introduced it",
                    "when and why it was introduced",
                ],
                "rounding": "and explain why you thought this law was such a good idea.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: school rules and working in the legal profession.",
            "questions": [
                {"id": "s5", "text": "What kinds of rules are common in a school?"},
                {"id": "s6", "text": "How important is it to have rules in a school?"},
                {"id": "s7", "text": "What do you recommend should happen if children break school rules?"},
                {"id": "s8", "text": "Can you suggest why many students decide to study law at university?"},
                {"id": "s9", "text": "What are the key personal qualities needed to be a successful lawyer?"},
                {"id": "s10", "text": "Do you agree that working in the legal profession is very stressful?"},
            ],
        },
    ]

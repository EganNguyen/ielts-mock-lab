"""IELTS 19 Academic - Test 4."""
from __future__ import annotations

from common import apply_keys, group, passage, question


def build(passages, keys, transcripts):
    return {
        "id": "ielts19-test4",
        "title": "IELTS 19 · Academic Test 4",
        "module": "Academic",
        "version": "ielts19.4",
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
            "# First day at work",
            "• Name of supervisor: {{1}}",
            "• Where to leave coat and bag: use {{2}} in staffroom",
            "• See Tiffany in HR: to give {{3}} number",
            "• to collect {{4}}",
            "• Location of HR office: on {{5}} floor",
            "• Supervisor's mobile number: {{6}}",
        ])
    qs = [question(n, "l1-g1", prompt) for n, prompt in [
        (1, "Name of the supervisor"), (2, "Where to leave coat and bag in the staffroom"),
        (3, "Document number to give Tiffany"), (4, "Item to collect from Tiffany"),
        (5, "Floor where the HR office is"), (6, "Supervisor's mobile number"),
    ]]
    g2 = group(
        "l1-g2", "Questions 7–10",
        "Complete the table below. Write ONE WORD ONLY for each answer.",
        list(range(7, 11)), layout="table", body=[
            "# Responsibilities",
            "• Bakery section — check sell-by dates — change price labels — use {{7}} labels",
            "• Sushi takeaway counter — re-stock with {{8}} boxes if needed — wipe preparation area and clean the sink — do not clean any knives",
            "• Meat and fish counters — clean the serving area, including the weighing scales — collect {{9}} for the fish from the cold-room — must wear special {{10}}",
        ])
    qs += [question(n, "l1-g2", prompt) for n, prompt in [
        (7, "Colour of the price labels"), (8, "Material of the takeaway boxes"),
        (9, "What to collect for the fish"), (10, "Special clothing to wear"),
    ]]
    apply_keys(qs, keys["listening"], "l1")
    parts.append({
        "id": "l1", "number": 1, "title": "First day at work",
        "context": "A new employee is given instructions on their first day at a supermarket.",
        "groups": [g1, g2], "questions": qs, "transcript": transcripts["1"],
    })

    # Part 2 ---------------------------------------------------------------
    problems = [
        "There is a risk of serious injury.", "They are unsuitable for certain age groups.",
        "They are unsuitable for people with health issues.", "It is difficult to stay motivated.",
        "There is a lack of individual support.",
    ]
    g3 = group(
        "l2-g1", "Questions 11 and 12",
        "Choose TWO letters, A–E. Which TWO problems with some training programmes for new runners does Liz mention?",
        [11, 12],
    )
    qs2 = [
        question(11, "l2-g1", "First problem with some training programmes", "mcq", problems),
        question(12, "l2-g1", "Second problem with some training programmes", "mcq", problems),
    ]
    tips = [
        "doing two runs a week", "running in the evening", "going on runs with a friend",
        "listening to music during runs", "running very slowly",
    ]
    g4 = group(
        "l2-g2", "Questions 13 and 14",
        "Choose TWO letters, A–E. Which TWO tips does Liz recommend for new runners?",
        [13, 14],
    )
    qs2 += [
        question(13, "l2-g2", "First tip for new runners", "mcq", tips),
        question(14, "l2-g2", "Second tip for new runners", "mcq", tips),
    ]
    reasons = ["A a lack of confidence", "B a dislike of running", "C a lack of time"]
    g5 = group(
        "l2-g3", "Questions 15–18",
        "What reason prevented each of the following members of the Compton Park Runners Club from joining until recently? Write the correct letter, A, B, or C next to Questions 15–18.",
        list(range(15, 19)), layout="match", shared=reasons,
    )
    qs2 += [question(n, "l2-g3", prompt, "match") for n, prompt in [
        (15, "Ceri"), (16, "James"), (17, "Leo"), (18, "Mark"),
    ]]
    g6 = group("l2-g4", "Questions 19 and 20", "Choose the correct letter, A, B or C.", [19, 20])
    qs2 += [question(n, "l2-g4", prompt, "mcq", options) for n, prompt, options in [
        (19, "What does Liz say about running her first marathon?",
         ["It had always been her ambition.", "Her husband persuaded her to do it.", "She nearly gave up before the end."]),
        (20, "Liz says new runners should sign up for a race",
         ["every six months.", "within a few weeks of taking up running.", "after completing several practice runs."]),
    ]]
    apply_keys(qs2, keys["listening"], "l2")
    parts.append({
        "id": "l2", "number": 2, "title": "Compton Park Runners",
        "context": "A running coach gives advice to new runners and describes her own experience.",
        "groups": [g3, g4, g5, g6], "questions": qs2, "transcript": transcripts["2"],
    })

    # Part 3 ---------------------------------------------------------------
    g7 = group("l3-g1", "Questions 21–25", "Choose the correct letter, A, B or C.", list(range(21, 26)))
    qs3 = [question(n, "l3-g1", prompt, "mcq", options) for n, prompt, options in [
        (21, "Kieran thinks the packing advice given by Jane's grandfather is",
         ["common sense.", "hard to follow.", "over-protective."]),
        (22, "How does Jane feel about the books her grandfather has given her?",
         ["They are not worth keeping.", "They should go to a collector.", "They have sentimental value for her."]),
        (23, "Jane and Kieran agree that hardback books should be",
         ["put out on display.", "given as gifts to visitors.", "more attractively designed."]),
        (24, "While talking about taking a book from a shelf, Jane",
         ["describes the mistakes other people make doing it.", "reflects on a significant childhood experience.", "explains why some books are easier to remove than others."]),
        (25, "What do Jane and Kieran suggest about new books?",
         ["Their parents liked buying them as presents.", "They would like to buy more of them.", "Not everyone can afford them."]),
    ]]
    locations = [
        "A near the entrance", "B in the attic", "C at the back of the shop", "D on a high shelf",
        "E near the stairs", "F in a specially designed space", "G within the café",
    ]
    g8 = group(
        "l3-g2", "Questions 26–30",
        "Where does Jane's grandfather keep each of the following types of books in his shop? Choose FIVE answers from the box and write the correct letter, A–G, next to Questions 26–30.",
        list(range(26, 31)), layout="match", shared=locations,
    )
    qs3 += [question(n, "l3-g2", prompt, "match") for n, prompt in [
        (26, "rare books"), (27, "children's books"), (28, "unwanted books"),
        (29, "requested books"), (30, "coursebooks"),
    ]]
    apply_keys(qs3, keys["listening"], "l3")
    parts.append({
        "id": "l3", "number": 3, "title": "A second-hand bookshop",
        "context": "Two students discuss a bookshop owned by Jane's grandfather.",
        "groups": [g7, g8], "questions": qs3, "transcript": transcripts["3"],
    })

    # Part 4 ---------------------------------------------------------------
    g9 = group(
        "l4-g1", "Questions 31–40",
        "Complete the notes below. Write ONE WORD ONLY for each answer.",
        list(range(31, 41)), layout="notes", body=[
            "# Tree planting",
            "## Reforestation projects should:",
            "• include a range of tree species",
            "• not include invasive species because of possible {{31}} with native species",
            "• aim to capture carbon, protect the environment and provide sustainable sources of {{32}} for local people",
            "• use tree seeds with a high genetic diversity to increase resistance to {{33}} and climate change",
            "• plant trees on previously forested land which is in a bad condition, not select land which is being used for {{34}}",
            "## Large-scale reforestation projects",
            "• Base planning decisions on information from accurate {{35}}.",
            "• Drones are useful for identifying areas in Brazil which are endangered by keeping {{36}} and illegal logging.",
            "## Lampang Province, Northern Thailand",
            "• A forest was restored in an area damaged by mining.",
            "• A variety of native fig trees were planted, which are important for:",
            "  – supporting many wildlife species",
            "  – increasing the {{37}} of recovery by attracting animals and birds, e.g. {{38}} were soon attracted to the area.",
            "## Involving local communities",
            "• Destruction of mangrove forests in Madagascar made it difficult for people to make a living from {{39}}.",
            "• The mangrove reforestation project:",
            "  – provided employment for local people",
            "  – restored a healthy ecosystem",
            "  – protects against the higher risk of {{40}}",
        ])
    qs4 = [question(n, "l4-g1", prompt) for n, prompt in [
        (31, "Possible negative interaction with native species"), (32, "What local people need sustainable sources of"),
        (33, "What genetic diversity helps trees resist, besides climate change"), (34, "Land use that should not be taken for planting"),
        (35, "Accurate information used for planning"), (36, "Activity that endangers areas in Brazil"),
        (37, "What fig trees increase in the recovery process"), (38, "Animal group attracted to the restored forest"),
        (39, "Activity local people in Madagascar relied on"), (40, "Natural hazard reduced by mangrove restoration"),
    ]]
    apply_keys(qs4, keys["listening"], "l4")
    parts.append({
        "id": "l4", "number": 4, "title": "Tree planting",
        "context": "A lecture about successful reforestation projects around the world.",
        "groups": [g9], "questions": qs4, "transcript": transcripts["4"],
    })
    return parts


def build_reading(passages, keys):
    reading = []

    # Passage 1 ------------------------------------------------------------
    r1 = passage(1, passages["1"])
    g1 = group(
        "r1-g1", "Questions 1–6",
        "Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.",
        list(range(1, 7)),
    )
    qs = [question(n, "r1-g1", prompt, "tfng") for n, prompt in [
        (1, "Forty years ago, there were fewer butterflies in Britain than at present."),
        (2, "Caterpillars are eaten by a number of different predators."),
        (3, "'Phenology' is a term used to describe a creature's ability to alter the location of a lifecycle event."),
        (4, "Some species of butterfly have a reduced lifespan due to spring temperature increases."),
        (5, "There is a clear reason for the adaptations that butterflies are making to climate change."),
        (6, "The data used in the study was taken from the work of amateur butterfly watchers."),
    ]]
    g2 = group(
        "r1-g2", "Questions 7–13",
        "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(7, 14)), layout="notes", body=[
            "# Butterflies in the UK",
            "## The Small Blue",
            "• has large {{7}}",
            "• first appears at the start of {{8}}",
            "• completes more than one reproductive cycle per year",
            "## The High Brown Fritillary",
            "• has one reproductive cycle",
            "• is considered to be more {{9}} than other species",
            "• its caterpillars occupy a limited range of {{10}}",
            "## The Silver-studded Blue",
            "• is already able to reproduce twice a year in warm areas of {{11}}",
            "## The White Admiral",
            "• is found in {{12}} areas of England",
            "• both climate change and the {{13}} of the caterpillar are possible reasons for decline",
        ])
    qs += [question(n, "r1-g2", prompt) for n, prompt in [
        (7, "What the Small Blue has large numbers of"), (8, "Season when the Small Blue first appears"),
        (9, "How the High Brown Fritillary is described compared with other species"), (10, "What the High Brown Fritillary's caterpillars have a limited range of"),
        (11, "Where the Silver-studded Blue can reproduce twice a year"), (12, "Part of England where the White Admiral is found"),
        (13, "Caterpillar's food-related cause of decline"),
    ]]
    apply_keys(qs, keys["reading"], "r1")
    r1["groups"] = [g1, g2]
    r1["questions"] = qs
    reading.append(r1)

    # Passage 2 ------------------------------------------------------------
    r2 = passage(2, passages["2"])
    g3 = group(
        "r2-g1", "Questions 14–17",
        "Reading Passage 2 has six paragraphs, A–F. Which paragraph contains the following information? Write the correct letter, A–F.",
        list(range(14, 18)), layout="match", shared=list("ABCDEF"),
    )
    qs2 = [question(n, "r2-g1", prompt, "match") for n, prompt in [
        (14, "reference to the rapidly increasing need for one raw material in the transport industry"),
        (15, "a rough estimate of the area of the Earth covered by the oceans"),
        (16, "how a particular underwater habitat, where minerals and organisms co-exist, is formed"),
        (17, "reference to the fact that the countries of the world have yet to agree on rules for the exploration of the seabed"),
    ]]
    people = [
        "A Professor Mat Upton",
        "B Julie Hunter, Julian Aguon and Pradeep Singh",
        "C Dr Jon Copley",
        "D Mike Johnston",
        "E Verena Tunnicliffe",
    ]
    g4 = group(
        "r2-g2", "Questions 18–23",
        "Look at the following statements and the list of people below. Match each statement with the correct person or people, A–E. NB You may use any letter more than once.",
        list(range(18, 24)), layout="match", shared=people,
    )
    qs2 += [question(n, "r2-g2", prompt, "match") for n, prompt in [
        (18, "A move away from the exploration of heavily mined reserves on land is a good idea."),
        (19, "The negative effects of undersea exploration on local areas and their inhabitants are being ignored."),
        (20, "There are more worthwhile things to extract from the sea than minerals."),
        (21, "No other form of human exploration will have such a destructive impact on marine life as deep-sea mining."),
        (22, "More is known about outer space than about what lies beneath the oceans."),
        (23, "There is one marine life habitat where experts agree mining should not take place."),
    ]]
    g5 = group(
        "r2-g3", "Questions 24–26",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(24, 27)), layout="summary", body=[
            "# Mining the sea floor",
            "Mining corporations believe that the mineral resources lying under the sea may be superior to those found in the earth. They also say that these can be removed without producing much {{24}}. The extraction is often done by adapting the {{25}} that has already been used to work on land. The method of excavation involves removing the seawater from the slurry that is brought up to ships and returning it to the seabed. However, concerned groups strongly believe that {{26}} is necessary due to the possible number of unidentified consequences.",
        ])
    qs2 += [question(n, "r2-g3", prompt) for n, prompt in [
        (24, "What deep-sea mining produces very little of"), (25, "Equipment adapted from land mining"),
        (26, "What concerned groups believe is necessary"),
    ]]
    apply_keys(qs2, keys["reading"], "r2")
    r2["groups"] = [g3, g4, g5]
    r2["questions"] = qs2
    reading.append(r2)

    # Passage 3 ------------------------------------------------------------
    r3 = passage(3, passages["3"])
    g6 = group("r3-g1", "Questions 27–30", "Choose the correct letter, A, B, C or D.", list(range(27, 31)))
    qs3 = [question(n, "r3-g1", prompt, "mcq", options) for n, prompt, options in [
        (27, "What is the writer doing in the first paragraph?",
         ["setting out two opposing views about human nature", "justifying his opinion about our tendency to be greedy", "describing a commonly held belief about people's behaviour", "explaining why he thinks that humans act in a selfish manner"]),
        (28, "What point is made about Richard Dawkins' book The Selfish Gene?",
         ["Its appeal lay in the radical nature of its ideas.", "Its success was due to the scientific support it offered.", "It presented a view that was in line with the attitudes of its time.", "It took an innovative approach to the analysis of human psychology."]),
        (29, "What does the writer suggest about the prehistoric era in the fourth paragraph?",
         ["Societies were more complex than many people believe.", "Supplies of natural resources were probably relatively plentiful.", "Most estimates about population sizes are likely to be inaccurate.", "Humans moved across continents more than was previously thought."]),
        (30, "The writer refers to Bruce Knauft's work as support for the idea that",
         ["selfishness is a relatively recent development in human societies.", "only people in isolated communities can live in an unselfish manner.", "very few lifestyles have survived unchanged since prehistoric times.", "hunter-gatherer cultures worldwide are declining in number."]),
    ]]
    g7 = group(
        "r3-g2", "Questions 31–35",
        "Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        list(range(31, 36)), layout="summary", body=[
            "# Contemporary hunter-gatherer societies",
            "Bruce Knauft's research shows that contemporary hunter-gatherer societies tend to exhibit a high level of {{31}} in all areas of life. In these cultures, distributing resources fairly among all members is a moral obligation. These societies also employ strategies to prevent differences in {{32}} occurring: for example, the !Kung follow a custom whereby the credit for one person's success at {{33}} is given to another member of the group. Individuals who behave in a {{34}} manner are punished by being excluded from the group, and women have a considerable amount of {{35}} in choices regarding work and marriage.",
        ])
    qs3 += [question(n, "r3-g2", prompt) for n, prompt in [
        (31, "High level of equality in hunter-gatherer societies"), (32, "Differences of this kind are prevented"),
        (33, "Activity whose credit is given to another person"), (34, "Manner that leads to exclusion from the group"),
        (35, "What women have a considerable amount of"),
    ]]
    g8 = group(
        "r3-g3", "Questions 36–40",
        "Do the following statements agree with the views of the writer in Reading Passage 3? Write YES if the statement agrees with the views of the writer, NO if the statement contradicts the views of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.",
        list(range(36, 41)),
    )
    qs3 += [question(n, "r3-g3", prompt, "ynng") for n, prompt in [
        (36, "Some anthropologists are mistaken about the point when the number of societies such as the !Kung began to decline."),
        (37, "Humans who developed warlike traits in prehistory would have had an advantage over those who did not."),
        (38, "Being peaceful and cooperative is a natural way for people to behave."),
        (39, "Negative traits are more apparent in some modern cultures than in others."),
        (40, "Animal research has failed to reveal a link between changes in the environment and the emergence of aggressive tendencies."),
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
            "prompt": "The charts below give information on the location and types of dance classes young people in a town in Australia are currently attending.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "instructions": ["Write at least 150 words.", "You should spend about 20 minutes on this task."],
            "minimumWords": 150, "suggestedMinutes": 20,
            "figure": "/media/figures/ielts19/test4-writing-task1.jpg",
            "figureAlt": "A pie chart showing where dance classes take place and a bar chart comparing ballet, tap and modern dance enrolments for under-11s and 11-16-year-olds.",
        },
        {
            "id": "writing-task-2", "number": 2, "title": "Writing Task 2",
            "prompt": "In many countries nowadays, consumers can go to a supermarket and buy food produced all over the world.\n\nDo you think this is a positive or negative development?",
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
            "description": "The examiner asks you about cafés.",
            "questions": [
                {"id": "s1", "text": "Do you have a favourite café? [Why/Why not?]"},
                {"id": "s2", "text": "Do you often go to cafés by yourself? [Why/Why not?]"},
                {"id": "s3", "text": "What do you think helps to make a café very popular? [Why?]"},
                {"id": "s4", "text": "Why do some people prefer cafés that are part of large chains, rather than small, local cafés?"},
            ],
        },
        {
            "id": "speaking-2", "number": 2, "title": "Part 2 · Cue card",
            "description": "Describe a place you visited that has beautiful views.",
            "questions": [],
            "cueCard": {
                "topic": "Describe a place you visited that has beautiful views.",
                "bullets": ["where this place is", "when and why you visited it", "what views you can see from this place"],
                "rounding": "and explain why you think these views are so beautiful.",
                "preparationSeconds": 60, "speakingSeconds": 120,
            },
        },
        {
            "id": "speaking-3", "number": 3, "title": "Part 3 · Discussion",
            "description": "Discussion topics: the beauty industry and beauty and culture.",
            "questions": [
                {"id": "s5", "text": "Do you agree that most beauty products are a waste of money?"},
                {"id": "s6", "text": "How does the beauty industry advertise its products so successfully?"},
                {"id": "s7", "text": "What do you think of the view that beauty products should not be advertised to children?"},
                {"id": "s8", "text": "Why do many people equate youth with beauty?"},
                {"id": "s9", "text": "Do you think that being beautiful could affect a person's success in life?"},
                {"id": "s10", "text": "Why might society's ideas about beauty change over time?"},
            ],
        },
    ]

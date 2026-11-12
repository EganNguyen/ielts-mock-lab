import type { Question, QuestionGroup, ReadingPassage } from '../lib/types'

const q = (question: Question): Question => question

const passage1Groups: QuestionGroup[] = [
  {
    id: 'r1-g1',
    label: 'Questions 1–6',
    instructions: 'Reading Passage 1 has six paragraphs, A–F. Choose the correct heading for each paragraph from the list of headings below. Write the correct number, i–viii.',
    range: [1, 6],
    sharedOptions: [
      'i   A cultural and ecological partnership',
      'ii   The mechanics of a changing landscape',
      'iii   From near-extinction to a new idea',
      'iv   A genetic legacy with consequences',
      'v   The economic case for ranching',
      'vi   Conflict over land and disease',
      'vii   A species in steep decline',
      'viii   How tourism saved a small town',
    ],
    note: 'There are more headings than paragraphs, so you will not use all of them.',
  },
  {
    id: 'r1-g2',
    label: 'Questions 7–13',
    instructions: 'Do the following statements agree with the information given in Reading Passage 1? Write TRUE if the statement agrees with the information, FALSE if the statement contradicts the information, or NOT GIVEN if there is no information on this.',
    range: [7, 13],
  },
]

const passage1Questions: Question[] = [
  q({ id: 'r1', number: 1, groupId: 'r1-g1', type: 'heading', prompt: 'Paragraph A', answer: 'vii', explanation: 'Paragraph A describes the collapse of bison numbers from tens of millions to a few hundred.' }),
  q({ id: 'r2', number: 2, groupId: 'r1-g1', type: 'heading', prompt: 'Paragraph B', answer: 'ii', explanation: 'Paragraph B explains how grazing, wallowing and trampling change the grassland.' }),
  q({ id: 'r3', number: 3, groupId: 'r1-g1', type: 'heading', prompt: 'Paragraph C', answer: 'iii', explanation: 'Paragraph C describes the first conservation efforts after near-extinction.' }),
  q({ id: 'r4', number: 4, groupId: 'r1-g1', type: 'heading', prompt: 'Paragraph D', answer: 'iv', explanation: 'Paragraph D focuses on the genetic bottleneck and cattle ancestry.' }),
  q({ id: 'r5', number: 5, groupId: 'r1-g1', type: 'heading', prompt: 'Paragraph E', answer: 'i', explanation: 'Paragraph E describes tribal restoration and the Buffalo Treaty, linking culture and ecology.' }),
  q({ id: 'r6', number: 6, groupId: 'r1-g1', type: 'heading', prompt: 'Paragraph F', answer: 'vi', explanation: 'Paragraph F discusses disputes over brucellosis, land and how bison should be treated.' }),
  q({ id: 'r7', number: 7, groupId: 'r1-g2', type: 'tfng', prompt: 'By the late nineteenth century, only a few hundred wild bison remained.', answer: 'TRUE', explanation: 'The passage says that by 1884 fewer than 350 wild bison survived.' }),
  q({ id: 'r8', number: 8, groupId: 'r1-g2', type: 'tfng', prompt: 'Bison grazing can increase the variety of plant life in a grassland.', answer: 'TRUE', explanation: 'Grazing removes dominant tall grasses and allows shorter plants to flourish, raising plant diversity.' }),
  q({ id: 'r9', number: 9, groupId: 'r1-g2', type: 'tfng', prompt: 'The first bison reserves in the United States were created by Native American tribes.', answer: 'FALSE', explanation: 'The first reserves were established by government agencies and private conservation groups; tribal-led restoration came much later.' }),
  q({ id: 'r10', number: 10, groupId: 'r1-g2', type: 'tfng', prompt: 'Every modern bison herd contains some cattle DNA.', answer: 'FALSE', explanation: 'Many commercial herds show cattle ancestry, but the Yellowstone herd does not.' }),
  q({ id: 'r11', number: 11, groupId: 'r1-g2', type: 'tfng', prompt: 'Yellowstone’s bison are descended from a very small number of animals.', answer: 'TRUE', explanation: 'The Yellowstone herd grew from roughly two dozen animals.' }),
  q({ id: 'r12', number: 12, groupId: 'r1-g2', type: 'tfng', prompt: 'The Buffalo Treaty has been signed by every tribal nation in North America.', answer: 'NOT GIVEN', explanation: 'The passage says more than twenty nations signed it, but does not say that every tribal nation did.' }),
  q({ id: 'r13', number: 13, groupId: 'r1-g2', type: 'tfng', prompt: 'Ranchers and conservationists agree on how bison should be managed.', answer: 'FALSE', explanation: 'The final paragraph describes continuing disagreement over disease risk, land and whether bison are wildlife or livestock.' }),
]

const passage2Groups: QuestionGroup[] = [
  {
    id: 'r2-g1',
    label: 'Questions 14–19',
    instructions: 'Reading Passage 2 has six paragraphs, A–F. Choose the correct heading for each paragraph from the list of headings below. Write the correct number, i–vii.',
    range: [14, 19],
    sharedOptions: [
      'i   The problem of noise pollution',
      'ii   A tool for restoring damaged areas',
      'iii   An environment full of information',
      'iv   The difficulty of interpreting recordings',
      'v   How marine animals find their way by sound',
      'vi   Evidence from a single species',
      'vii   The economic value of fishing',
    ],
    note: 'There are more headings than paragraphs, so you will not use all of them.',
  },
  {
    id: 'r2-g2',
    label: 'Questions 20–23',
    instructions: 'Choose the correct letter, A, B, C or D.',
    range: [20, 23],
  },
  {
    id: 'r2-g3',
    label: 'Questions 24–26',
    instructions: 'Complete the summary below. Write NO MORE THAN TWO WORDS from the passage for each answer.',
    range: [24, 26],
  },
]

const passage2Questions: Question[] = [
  q({ id: 'r14', number: 14, groupId: 'r2-g1', type: 'heading', prompt: 'Paragraph A', answer: 'iii', explanation: 'Paragraph A explains that the sea is filled with biological and physical sound.' }),
  q({ id: 'r15', number: 15, groupId: 'r2-g1', type: 'heading', prompt: 'Paragraph B', answer: 'vi', explanation: 'Paragraph B focuses on research into humpback whale song.' }),
  q({ id: 'r16', number: 16, groupId: 'r2-g1', type: 'heading', prompt: 'Paragraph C', answer: 'v', explanation: 'Paragraph C shows how coral larvae use sound to choose where to settle.' }),
  q({ id: 'r17', number: 17, groupId: 'r2-g1', type: 'heading', prompt: 'Paragraph D', answer: 'i', explanation: 'Paragraph D describes the rise in shipping noise and its effects.' }),
  q({ id: 'r18', number: 18, groupId: 'r2-g1', type: 'heading', prompt: 'Paragraph E', answer: 'ii', explanation: 'Paragraph E describes acoustic enrichment projects that help restore reefs.' }),
  q({ id: 'r19', number: 19, groupId: 'r2-g1', type: 'heading', prompt: 'Paragraph F', answer: 'iv', explanation: 'Paragraph F discusses the challenges of analysing recordings and the limits of the evidence.' }),
  q({
    id: 'r20', number: 20, groupId: 'r2-g2', type: 'mcq',
    prompt: 'Why did early researchers describe the ocean as silent?',
    options: ['Their equipment could not detect low-frequency sound.', 'They did not spend long enough at sea.', 'They believed marine animals were unable to hear.', 'They only studied shallow water.'],
    answer: 'A', explanation: 'Early hydrophones were designed around human hearing and missed the low frequencies used by many marine animals.',
  }),
  q({
    id: 'r21', number: 21, groupId: 'r2-g2', type: 'mcq',
    prompt: 'What is notable about humpback whale songs?',
    options: ['They are identical in every ocean.', 'They change over time and spread between populations.', 'They are sung only during the night.', 'They are too quiet for humans to hear.'],
    answer: 'B', explanation: 'The songs gradually change and new versions spread across ocean basins.',
  }),
  q({
    id: 'r22', number: 22, groupId: 'r2-g2', type: 'mcq',
    prompt: 'Coral larvae use underwater sound mainly to',
    options: ['avoid predators.', 'choose a suitable place to settle.', 'locate food.', 'communicate with adult corals.'],
    answer: 'B', explanation: 'Larvae are more likely to settle on surfaces near the sound of a healthy reef community.',
  }),
  q({
    id: 'r23', number: 23, groupId: 'r2-g2', type: 'mcq',
    prompt: 'Shipping noise is a particular concern because it',
    options: ['masks sounds that animals depend on.', 'raises the temperature of the water.', 'attracts large predators to ports.', 'prevents larvae from feeding.'],
    answer: 'A', explanation: 'Low-frequency ship noise can drown out the calls and environmental cues that animals use.',
  }),
  q({
    id: 'r24', number: 24, groupId: 'r2-g3', type: 'short',
    prompt: 'Modern surveys produce huge quantities of [[blank]], which machine learning can help analyse.',
    answer: 'acoustic data', accepted: ['acousticdata', 'underwater recordings', 'recordings'],
    explanation: 'The passage refers to the enormous amount of acoustic data collected by modern surveys.',
  }),
  q({
    id: 'r25', number: 25, groupId: 'r2-g3', type: 'short',
    prompt: 'In one experiment, recordings of healthy reefs attracted more [[blank]] to damaged areas.',
    answer: 'fish', accepted: ['young fish'], explanation: 'Playing healthy reef soundscapes attracted fish to degraded reef patches.',
  }),
  q({
    id: 'r26', number: 26, groupId: 'r2-g3', type: 'short',
    prompt: 'The writer argues that reducing [[blank]] should form part of ocean conservation.',
    answer: 'shipping noise', accepted: ['shippingnoise', 'ship noise', 'noise from ships'],
    explanation: 'The final paragraph calls for quieter ships and lower shipping noise.',
  }),
]

const passage3Groups: QuestionGroup[] = [
  {
    id: 'r3-g1',
    label: 'Questions 27–32',
    instructions: 'Do the following statements agree with the views of the writer in Reading Passage 3? Write YES if the statement agrees with the views of the writer, NO if the statement contradicts the views of the writer, or NOT GIVEN if it is impossible to say what the writer thinks about this.',
    range: [27, 32],
  },
  {
    id: 'r3-g2',
    label: 'Questions 33–36',
    instructions: 'Reading Passage 3 has seven paragraphs, A–G. Which paragraph contains the following information? Write the correct letter, A–G.',
    range: [33, 36],
    note: 'You may use any letter more than once.',
  },
  {
    id: 'r3-g3',
    label: 'Questions 37–40',
    instructions: 'Choose the correct letter, A, B, C or D.',
    range: [37, 40],
  },
]

const passage3Questions: Question[] = [
  q({ id: 'r27', number: 27, groupId: 'r3-g1', type: 'ynng', prompt: 'Tetlock’s experts performed worse than a simple statistical rule.', answer: 'YES', explanation: 'The passage says their forecasts were sometimes less accurate than simple extrapolation.' }),
  q({ id: 'r28', number: 28, groupId: 'r3-g1', type: 'ynng', prompt: 'Hedgehogs make more accurate forecasters than foxes.', answer: 'NO', explanation: 'The passage says the opposite: foxes tend to forecast more accurately.' }),
  q({ id: 'r29', number: 29, groupId: 'r3-g1', type: 'ynng', prompt: 'Most superforecasters were employed by universities.', answer: 'NOT GIVEN', explanation: 'The passage describes their thinking habits but not their employers.' }),
  q({ id: 'r30', number: 30, groupId: 'r3-g1', type: 'ynng', prompt: 'Combining several forecasts tends to improve accuracy.', answer: 'YES', explanation: 'Averaging independent forecasts reduced error and improved accuracy.' }),
  q({ id: 'r31', number: 31, groupId: 'r3-g1', type: 'ynng', prompt: 'Artificial intelligence has replaced human forecasters in government.', answer: 'NO', explanation: 'The passage says AI is used alongside people, not instead of them.' }),
  q({ id: 'r32', number: 32, groupId: 'r3-g1', type: 'ynng', prompt: 'Superforecasters revise their beliefs when new evidence appears.', answer: 'YES', explanation: 'Frequent, small updates in response to new information are one of their defining habits.' }),
  q({ id: 'r33', number: 33, groupId: 'r3-g2', type: 'match', prompt: 'a comparison between two styles of thinking', answer: 'B', explanation: 'Paragraph B contrasts hedgehogs, who rely on one big idea, with foxes, who draw on many.' }),
  q({ id: 'r34', number: 34, groupId: 'r3-g2', type: 'match', prompt: 'a reference to the difficulty of predicting rare events', answer: 'F', explanation: 'Paragraph F discusses rare “black swan” events and the lack of feedback.' }),
  q({ id: 'r35', number: 35, groupId: 'r3-g2', type: 'match', prompt: 'an example of people and machines working together', answer: 'E', explanation: 'Paragraph E describes hybrid teams in which human judgement refines machine output.' }),
  q({ id: 'r36', number: 36, groupId: 'r3-g2', type: 'match', prompt: 'a description of a large forecasting tournament', answer: 'C', explanation: 'Paragraph C describes the Good Judgment Project and its thousands of participants.' }),
  q({
    id: 'r37', number: 37, groupId: 'r3-g3', type: 'mcq',
    prompt: 'Tetlock’s early findings were surprising because the experts',
    options: ['were less accurate than simple rules.', 'refused to make numerical predictions.', 'were too confident to take part.', 'had all been chosen by governments.'],
    answer: 'A', explanation: 'The experts’ record was no better, and sometimes worse, than simple extrapolation from past data.',
  }),
  q({
    id: 'r38', number: 38, groupId: 'r3-g3', type: 'mcq',
    prompt: 'What is typical of superforecasters?',
    options: ['They avoid making numerical estimates.', 'They revise probabilities as events unfold.', 'They prefer to work without other people.', 'They rely on a single guiding theory.'],
    answer: 'B', explanation: 'They assign probabilities and update them frequently in small increments.',
  }),
  q({
    id: 'r39', number: 39, groupId: 'r3-g3', type: 'mcq',
    prompt: 'According to the passage, AI forecasting models',
    options: ['have made human judgement unnecessary.', 'are most useful when combined with human judgement.', 'are too expensive for most organisations.', 'perform best on rare events.'],
    answer: 'B', explanation: 'The passage says hybrid human–machine teams outperform either alone.',
  }),
  q({
    id: 'r40', number: 40, groupId: 'r3-g3', type: 'mcq',
    prompt: 'What is the main point of the passage?',
    options: ['Prediction is fundamentally impossible.', 'Good forecasting is a learnable discipline rather than a mysterious talent.', 'Governments should stop using experts.', 'Algorithms will soon replace all human forecasters.'],
    answer: 'B', explanation: 'The passage argues that forecasting improves with deliberate practice, feedback and humility.',
  }),
]

export const readingPassages: ReadingPassage[] = [
  {
    id: 'reading-1',
    number: 1,
    title: 'The Return of the Bison',
    subtitle: 'How a species brought back from the edge is reshaping the grasslands — and the argument about how to protect it',
    paragraphs: [
      {
        label: 'A',
        text: 'At the beginning of the nineteenth century, an estimated thirty to sixty million bison roamed the grasslands of North America. They moved in herds so large that a single herd could take days to pass. By 1884, fewer than 350 wild bison survived. Hunters, railways and government policies had turned abundance into near-extinction in less than a century. For the Plains peoples who depended on the animal for food, shelter and ceremony, the loss was cultural as well as ecological. The bison had been the centre of a way of life, and its disappearance was a deliberate part of the campaign to dismantle that life.',
      },
      {
        label: 'B',
        text: 'Bison are often described as ecosystem engineers, and the phrase is more than a compliment. Their grazing removes the tall grasses that would otherwise dominate a meadow, allowing shorter plants and wildflowers to receive light. Their wallows — shallow depressions made by rolling in the dust — collect rainwater and become temporary pools used by insects, birds and amphibians. Their hooves break up compacted soil, and their dung returns nutrients and disperses seeds. A long-term study in Kansas found that plots grazed by bison contained a greater variety of plant species than plots left ungrazed. The animals do not simply live in a landscape; they help to make it.',
      },
      {
        label: 'C',
        text: 'Conservation began when the situation looked hopeless. In 1905, the American Bison Society was founded, with the aim of establishing captive herds and protected ranges. The Bronx Zoo bred animals, and in 1907 a small group was transported to the Wichita Mountains reserve in Oklahoma. These early reserves were created by government agencies and private conservation organisations, not by the tribal nations whose relationship with the bison had been broken. The programme worked, at least in the narrow sense that the species survived. By the 1930s there were several thousand bison, and the panic of extinction had given way to a new idea: that a wild animal could be managed, fenced and brought back.',
      },
      {
        label: 'D',
        text: 'Survival, however, came at a genetic cost. The modern plains bison population is descended from a remarkably small number of animals. Yellowstone’s herd, often treated as the most genetically wild, grew from roughly two dozen individuals. Early ranchers also crossed bison with cattle in an attempt to produce a hardier domestic animal. Genetic testing has since found cattle DNA in many commercial herds, although not in the Yellowstone population. Low genetic diversity leaves bison more vulnerable to disease and environmental change. Conservationists now argue about whether herds should be mixed to restore variation, or kept separate to preserve whatever distinctiveness remains.',
      },
      {
        label: 'E',
        text: 'In recent decades, the initiative has shifted. More than twenty tribal nations have signed the Buffalo Treaty, an agreement that treats the animal as a relative as well as a resource. For its signatories, restoration is not only a matter of biodiversity but of food sovereignty, education and cultural continuity. Tribal herds are also changing the scientific picture. Because they are managed by communities that rely on them, they are often monitored more closely than herds on remote public land. The treaty has helped to reconnect fragmented habitats and to place Indigenous knowledge at the centre of a conservation story from which it had been excluded.',
      },
      {
        label: 'F',
        text: 'The return of the bison has also revived an older conflict. Ranchers in the Yellowstone region worry that bison, which can carry brucellosis, may transmit the disease to cattle; the evidence for transmission in the wild is contested, but the economic consequences for a rancher would be severe. Others point to the damage bison can do to fences and crops when they leave protected areas. There is disagreement, too, about what a restored herd should be. Some argue that bison should be treated as wildlife, free to move across the landscape. Others regard them as livestock, to be owned, vaccinated and controlled. The animal has survived; the argument about its future has only become more complicated.',
      },
    ],
    groups: passage1Groups,
    questions: passage1Questions,
  },
  {
    id: 'reading-2',
    number: 2,
    title: 'Listening to the Ocean',
    subtitle: 'Marine scientists are learning to read the soundscape of the sea — and discovering that noise is a form of pollution',
    paragraphs: [
      {
        label: 'A',
        text: 'For most of human history, the sea was imagined as a place of silence. Sailors spoke of a “silent world”, and early naturalists assumed that sound could not travel far through water. That assumption was wrong. Water carries sound about four and a half times faster than air, and low-frequency sound can travel for hundreds of kilometres. The ocean is, in fact, an extraordinarily noisy place. Rain, waves, earthquakes and the clicks and calls of marine animals combine into a complex soundscape. A hydrophone lowered into the water does not record emptiness; it records a dense and constantly changing acoustic environment.',
      },
      {
        label: 'B',
        text: 'The most famous example is the song of the humpback whale. Male humpbacks produce long, structured sequences of moans, cries and clicks that can last for twenty minutes and carry across an entire ocean basin. The songs are not fixed. They change gradually over months and years, and new versions spread from one population to another. Researchers have used these changes to trace migration routes and social connections. The song is also a reminder that the sea is full of information: an animal can announce its presence, attract a mate or warn a rival without ever seeing the other individual.',
      },
      {
        label: 'C',
        text: 'Sound is not only communication; it is also a map. Many coral larvae are tiny, weak swimmers, yet they must find a suitable place to settle after drifting in the plankton. Experiments have shown that they are more likely to settle on surfaces near the sound of a healthy reef — the crackle of snapping shrimp, the grunts of fish — than near the relative quiet of a degraded one. The soundscape acts as a cue, allowing a larva to distinguish a living community from a dead one. Similar cues are used by some fish and crabs when choosing a habitat.',
      },
      {
        label: 'D',
        text: 'Human activity has added a new and dominant layer to this environment. Commercial shipping has increased enormously since the mid-twentieth century, and the low-frequency rumble of engines and propellers travels far through the water. In some busy shipping lanes, background noise has risen by several dozen decibels over the past seventy years. For animals that rely on low-frequency calls, the effect is like trying to hold a conversation beside a motorway. Whales may raise the volume of their calls, but this costs energy and can still fail to overcome the noise. Chronic noise has been linked to stress and to changes in feeding and migration behaviour.',
      },
      {
        label: 'E',
        text: 'If sound can damage a habitat, it can also help to repair one. In a series of experiments, researchers placed underwater speakers around patches of degraded reef and played recordings made at healthy sites. Fish arrived in greater numbers, and the patches began to accumulate the kinds of organisms that support a reef community. The technique, sometimes called acoustic enrichment, is not a substitute for reducing pollution or protecting fish stocks. But it shows that the soundscape is not merely a symptom of reef health; it can be a tool for restoring it.',
      },
      {
        label: 'F',
        text: 'The difficulty is turning all this listening into reliable knowledge. A single hydrophone can produce months of recordings, and the amount of acoustic data now being collected is far beyond what researchers can examine by hand. Machine learning can identify particular calls and patterns, but the models need carefully labelled examples and may fail when conditions change. Sound also tells us what is present, not why it matters. A recording can reveal that a species has returned to an area, but not whether the population is healthy. The next task for marine acoustics is therefore as much political as technical: to persuade shipping companies and governments that quieter ships and protected quiet areas are part of conservation, not an optional extra.',
      },
    ],
    groups: passage2Groups,
    questions: passage2Questions,
  },
  {
    id: 'reading-3',
    number: 3,
    title: 'The Prediction Paradox',
    subtitle: 'Why experts are often poor forecasters, and what the best of them do differently',
    paragraphs: [
      {
        label: 'A',
        text: 'In 1984, the psychologist Philip Tetlock began an experiment that would make him unpopular in certain circles. He recruited 284 experts in politics, economics and international affairs and asked them to make thousands of predictions about future events. Over the next twenty years, he collected more than 82,000 forecasts and compared them with what actually happened. The result was humbling. The experts were barely more accurate than chance, and in some cases they performed worse than a simple rule that extrapolated recent trends. The people who appeared most often on television were not the best forecasters; they were often the worst.',
      },
      {
        label: 'B',
        text: 'Tetlock borrowed a distinction from the philosopher Isaiah Berlin. Hedgehogs know one big thing: they organise the world around a single theory and interpret new events as confirmation of it. Foxes know many little things: they draw on different ideas, tolerate contradiction and are willing to revise their views. Foxes, Tetlock found, were significantly better at forecasting. The reason is not that they are more intelligent, but that they are less attached to a single story. A hedgehog who predicts that an economy will collapse may keep predicting collapse because the theory demands it; a fox notices the evidence that does not fit and adjusts.',
      },
      {
        label: 'C',
        text: 'The research programme eventually became a tournament. In 2011, the Good Judgment Project invited thousands of volunteers to forecast political and economic events, with their accuracy scored against real outcomes. A small group stood out. These “superforecasters” were not necessarily experts in the regions they were predicting. What distinguished them was a set of habits. They thought in probabilities rather than certainties, broke questions into smaller parts, updated their estimates frequently and in small increments, and actively looked for evidence that might prove them wrong. They also avoided hindsight bias: after an event, they reviewed their earlier reasoning instead of simply congratulating themselves on being right.',
      },
      {
        label: 'D',
        text: 'One of the most reliable findings in the field is that crowds can beat individuals. When forecasts from many independent people are averaged, the result is usually more accurate than the typical individual forecast, and sometimes better than the best one. The effect is strengthened when forecasters are asked to explain their reasoning and when their scores are visible to others. Aggregation works because individual errors are partly random: one person overestimates a risk, another underestimates it, and the average lands closer to the truth. The lesson is not that expertise is worthless, but that no single perspective should be trusted completely.',
      },
      {
        label: 'E',
        text: 'Artificial intelligence has added a new dimension. Large language models can absorb enormous quantities of news and data and produce forecasts at a speed no human team could match. In some domains, they perform surprisingly well. Yet the evidence so far suggests that the best results come from hybrid arrangements, in which a model generates a range of possibilities and human analysts judge which are plausible, ask what the model has missed and adjust for context. The machine is good at processing; the human is good at knowing which questions matter. Neither is sufficient alone.',
      },
      {
        label: 'F',
        text: 'Forecasting also has limits that no method can remove. The most consequential events are often rare, and rare events provide little feedback from which to learn. A forecaster may be right for the wrong reasons or wrong for the right ones. When a prediction fails, it is tempting to explain the failure away; when it succeeds, it is tempting to claim credit. The result is that many people improve their confidence without improving their accuracy. Tetlock calls this “belief system defence”. The best forecasters are those who resist it, who treat their own conclusions as provisional and who keep score honestly.',
      },
      {
        label: 'G',
        text: 'The practical implication is encouraging. If good forecasting were a mysterious talent, most organisations could do little to improve. But the evidence suggests that it is a discipline: a set of habits that can be taught, practised and measured. Asking better questions, assigning probabilities, seeking disconfirming evidence and reviewing outcomes are not glamorous activities. They do not produce the confident headlines that audiences reward. They do, however, produce better decisions. In a world that increasingly demands certainty, the most valuable skill may be the willingness to remain uncertain for longer.',
      },
    ],
    groups: passage3Groups,
    questions: passage3Questions,
  },
]

import type { ListeningPart, Question, QuestionGroup } from '../lib/types'

const q = (question: Question): Question => question

const part1Groups: QuestionGroup[] = [
  {
    id: 'l1-g1',
    label: 'Questions 1–10',
    instructions: 'Complete the membership form below. Write ONE WORD AND/OR A NUMBER for each answer.',
    range: [1, 10],
    layout: 'form',
  },
]

const part1Questions: Question[] = [
  q({
    id: 'l1', number: 1, groupId: 'l1-g1', type: 'short',
    prompt: 'Surname: [[blank]]',
    answer: 'Marsh', explanation: 'The caller spells her surname: M-A-R-S-H.',
  }),
  q({
    id: 'l2', number: 2, groupId: 'l1-g1', type: 'short',
    prompt: 'Street: 42 [[blank]] Road',
    answer: 'Ellison', accepted: ['ellison road'], explanation: 'She gives her address as 42 Ellison Road and spells Ellison.',
  }),
  q({
    id: 'l3', number: 3, groupId: 'l1-g1', type: 'short',
    prompt: 'Postcode: [[blank]]',
    answer: 'BR8 4QT', accepted: ['br84qt', 'br8 4qt'], explanation: 'The postcode is dictated as B-R-8, 4-Q-T.',
  }),
  q({
    id: 'l4', number: 4, groupId: 'l1-g1', type: 'short',
    prompt: 'Date of birth: [[blank]]',
    answer: '17 March 1991', accepted: ['17th march 1991', 'march 17 1991', '17/03/1991'],
    explanation: 'Elena says the seventeenth of March, nineteen ninety-one.',
  }),
  q({
    id: 'l5', number: 5, groupId: 'l1-g1', type: 'short',
    prompt: 'Membership type: [[blank]]',
    answer: 'Premium', accepted: ['premium membership'], explanation: 'She chooses the premium membership so she can use the climbing wall.',
  }),
  q({
    id: 'l6', number: 6, groupId: 'l1-g1', type: 'short',
    prompt: 'Main interest: [[blank]]',
    answer: 'climbing', accepted: ['the climbing wall', 'climbing wall'],
    explanation: 'Mia records climbing as her main interest.',
  }),
  q({
    id: 'l7', number: 7, groupId: 'l1-g1', type: 'short',
    prompt: 'Preferred start date: [[blank]]',
    answer: '1 July', accepted: ['july 1', '1st july', 'first of july', '01/07'],
    explanation: 'She asks to start on the first of July because she is away in June.',
  }),
  q({
    id: 'l8', number: 8, groupId: 'l1-g1', type: 'short',
    prompt: 'Monthly fee: £[[blank]]',
    answer: '38', accepted: ['38 pounds', '£38'], explanation: 'Premium membership costs thirty-eight pounds a month.',
  }),
  q({
    id: 'l9', number: 9, groupId: 'l1-g1', type: 'short',
    prompt: 'Payment method: [[blank]]',
    answer: 'direct debit', accepted: ['directdebit'], explanation: 'She chooses to pay by direct debit.',
  }),
  q({
    id: 'l10', number: 10, groupId: 'l1-g1', type: 'short',
    prompt: 'Email: [[blank]]',
    answer: 'elena.marsh@brightmail.com', accepted: ['elenamarsh@brightmail.com'],
    explanation: 'The email address is confirmed as elena.marsh@brightmail.com.',
  }),
]

const part2Groups: QuestionGroup[] = [
  {
    id: 'l2-g1',
    label: 'Questions 11–15',
    instructions: 'Choose the correct letter, A, B or C.',
    range: [11, 15],
  },
  {
    id: 'l2-g2',
    label: 'Questions 16–20',
    instructions: 'Where does each event take place? Choose the correct letter, A–H, from the map.',
    range: [16, 20],
    sharedOptions: [
      'A  Main entrance',
      'B  Gallery One',
      'C  Gallery Two',
      'D  Garden courtyard',
      'E  Café',
      'F  Lecture theatre',
      'G  Workshop studio',
      'H  Museum shop',
    ],
    note: 'The map is shown below. You may use any letter more than once.',
  },
]

const part2Questions: Question[] = [
  q({
    id: 'l11', number: 11, groupId: 'l2-g1', type: 'mcq',
    prompt: 'What is the main new feature of this year’s summer programme?',
    options: ['late opening on Thursdays', 'free entry to special exhibitions', 'a series of outdoor workshops'],
    answer: 'C', explanation: 'The guide says the outdoor programme is “the real headline” and the main change this year.',
  }),
  q({
    id: 'l12', number: 12, groupId: 'l2-g1', type: 'mcq',
    prompt: 'The family history workshops are designed for',
    options: ['children under 10.', 'young people aged 13 to 17.', 'adults with young families.'],
    answer: 'B', explanation: 'The sessions are for young people aged thirteen to seventeen.',
  }),
  q({
    id: 'l13', number: 13, groupId: 'l2-g1', type: 'mcq',
    prompt: 'Visitors on the night tour should bring',
    options: ['comfortable shoes.', 'a torch.', 'a camera.'],
    answer: 'A', explanation: 'The route covers uneven floors, so comfortable shoes are advised. Torches are provided and photography is not permitted.',
  }),
  q({
    id: 'l14', number: 14, groupId: 'l2-g1', type: 'mcq',
    prompt: 'The café will be closed on',
    options: ['Mondays.', 'the first week of August.', 'weekday evenings.'],
    answer: 'A', explanation: 'The café closes on Mondays for staff training.',
  }),
  q({
    id: 'l15', number: 15, groupId: 'l2-g1', type: 'mcq',
    prompt: 'What is the best way to book an event?',
    options: ['by telephone', 'on the museum website', 'at the reception desk'],
    answer: 'B', explanation: 'The website is the quickest and most reliable way to book.',
  }),
  q({
    id: 'l16', number: 16, groupId: 'l2-g2', type: 'match',
    prompt: 'local history talk', answer: 'F', explanation: 'The talk takes place in the Lecture Theatre.',
  }),
  q({
    id: 'l17', number: 17, groupId: 'l2-g2', type: 'match',
    prompt: 'children’s craft sessions', answer: 'G', explanation: 'The craft sessions are held in the Workshop Studio.',
  }),
  q({
    id: 'l18', number: 18, groupId: 'l2-g2', type: 'match',
    prompt: 'refreshments', answer: 'D', explanation: 'Refreshments are served in the Garden courtyard.',
  }),
  q({
    id: 'l19', number: 19, groupId: 'l2-g2', type: 'match',
    prompt: 'new photography exhibition', answer: 'C', explanation: 'The photography exhibition opens in Gallery Two.',
  }),
  q({
    id: 'l20', number: 20, groupId: 'l2-g2', type: 'match',
    prompt: 'evening music performance', answer: 'B', explanation: 'The evening performance is in Gallery One.',
  }),
]

const part3Groups: QuestionGroup[] = [
  {
    id: 'l3-g1',
    label: 'Questions 21–25',
    instructions: 'Choose the correct letter, A, B or C.',
    range: [21, 25],
  },
  {
    id: 'l3-g2',
    label: 'Questions 26–30',
    instructions: 'Who will be responsible for each task? Choose A, B or C.',
    range: [26, 30],
    sharedOptions: ['A  Priya', 'B  Tom', 'C  Both students'],
  },
]

const part3Questions: Question[] = [
  q({
    id: 'l21', number: 21, groupId: 'l3-g1', type: 'mcq',
    prompt: 'Why did the students choose their research topic?',
    options: ['Their tutor recommended it.', 'They had noticed a problem themselves.', 'There was little local research on it.'],
    answer: 'C', explanation: 'Priya found studies of household and restaurant waste, but almost nothing about university cafés.',
  }),
  q({
    id: 'l22', number: 22, groupId: 'l3-g1', type: 'mcq',
    prompt: 'What was the main problem when collecting the cafés’ data?',
    options: ['The cafés refused to share it.', 'The records were kept inconsistently.', 'The students did not have enough time.'],
    answer: 'B', explanation: 'Some cafés record meals sold and others only income, so the data is inconsistent.',
  }),
  q({
    id: 'l23', number: 23, groupId: 'l3-g1', type: 'mcq',
    prompt: 'What does Priya suggest about the student survey?',
    options: ['It should be kept short.', 'It should offer a small reward.', 'It should only be online.'],
    answer: 'A', explanation: 'Priya says people will not finish a survey that takes more than five minutes, so it should be short.',
  }),
  q({
    id: 'l24', number: 24, groupId: 'l3-g1', type: 'mcq',
    prompt: 'What is Tom worried about?',
    options: ['The sample may be too small.', 'The respondents may not be representative.', 'The analysis will be too complicated.'],
    answer: 'B', explanation: 'He says that standing outside one café at lunchtime would mostly reach regular customers, not the whole campus.',
  }),
  q({
    id: 'l25', number: 25, groupId: 'l3-g1', type: 'mcq',
    prompt: 'What will the students do next?',
    options: ['consult their supervisor', 'test the questionnaire', 'review more literature'],
    answer: 'B', explanation: 'They agree to test the questionnaire on about fifteen people before sending it out.',
  }),
  q({
    id: 'l26', number: 26, groupId: 'l3-g2', type: 'match',
    prompt: 'contact the café managers', answer: 'B', explanation: 'Tom offers to email the café managers to ask for access.',
  }),
  q({
    id: 'l27', number: 27, groupId: 'l3-g2', type: 'match',
    prompt: 'write the literature review', answer: 'A', explanation: 'Priya says she will draft the literature review that week.',
  }),
  q({
    id: 'l28', number: 28, groupId: 'l3-g2', type: 'match',
    prompt: 'conduct the interviews', answer: 'C', explanation: 'They agree to carry out the interviews together.',
  }),
  q({
    id: 'l29', number: 29, groupId: 'l3-g2', type: 'match',
    prompt: 'analyse the sales and waste figures', answer: 'B', explanation: 'Tom takes responsibility for analysing the figures.',
  }),
  q({
    id: 'l30', number: 30, groupId: 'l3-g2', type: 'match',
    prompt: 'prepare the final presentation', answer: 'C', explanation: 'They decide to prepare the presentation together.',
  }),
]

const part4Groups: QuestionGroup[] = [
  {
    id: 'l4-g1',
    label: 'Questions 31–40',
    instructions: 'Complete the notes below. Write NO MORE THAN TWO WORDS for each answer.',
    range: [31, 40],
    layout: 'notes',
  },
]

const part4Questions: Question[] = [
  q({
    id: 'l31', number: 31, groupId: 'l4-g1', type: 'short',
    prompt: 'Cities may offer greater [[blank]] than farmland',
    answer: 'plant diversity', accepted: ['plantdiversity', 'diversity of plants'],
    explanation: 'The lecturer says cities can offer greater plant diversity than surrounding farmland.',
  }),
  q({
    id: 'l32', number: 32, groupId: 'l4-g1', type: 'short',
    prompt: 'Bees need food, shelter and [[blank]]',
    answer: 'water', explanation: 'All bees need food, shelter and water.',
  }),
  q({
    id: 'l33', number: 33, groupId: 'l4-g1', type: 'short',
    prompt: 'Warmer cities can cause queens to emerge [[blank]]',
    answer: 'earlier', explanation: 'Warmer temperatures cause queen bees to emerge earlier in the year.',
  }),
  q({
    id: 'l34', number: 34, groupId: 'l4-g1', type: 'short',
    prompt: 'Researchers use tiny [[blank]] inside hives to record sound',
    answer: 'microphones', explanation: 'Tiny microphones are placed inside hives to record the sound of the colony.',
  }),
  q({
    id: 'l35', number: 35, groupId: 'l4-g1', type: 'short',
    prompt: 'Study in [[blank]] found more species in gardens than parks',
    answer: 'Melbourne', explanation: 'The study comparing gardens and parks took place in Melbourne.',
  }),
  q({
    id: 'l36', number: 36, groupId: 'l4-g1', type: 'short',
    prompt: 'Roof gardens can act as [[blank]] between green spaces',
    answer: 'stepping stones', accepted: ['steppingstones'],
    explanation: 'Roof gardens can act as stepping stones between larger green spaces.',
  }),
  q({
    id: 'l37', number: 37, groupId: 'l4-g1', type: 'short',
    prompt: 'Pesticide traces have been found in [[blank]]',
    answer: 'pollen', explanation: 'Traces of pesticides were found in samples of pollen.',
  }),
  q({
    id: 'l38', number: 38, groupId: 'l4-g1', type: 'short',
    prompt: 'Citizen science project: [[blank]]',
    answer: 'BeeWatch', accepted: ['bee watch'], explanation: 'The project is called BeeWatch.',
  }),
  q({
    id: 'l39', number: 39, groupId: 'l4-g1', type: 'short',
    prompt: 'Best time to record sightings: [[blank]]',
    answer: 'early morning', accepted: ['earlymorning', 'the early morning'],
    explanation: 'The lecturer recommends early morning, when bees are still warming up.',
  }),
  q({
    id: 'l40', number: 40, groupId: 'l4-g1', type: 'short',
    prompt: 'Gardeners should leave a pile of [[blank]]',
    answer: 'dead wood', accepted: ['deadwood'], explanation: 'A pile of dead wood provides nesting places for solitary bees.',
  }),
]

export const listeningParts: ListeningPart[] = [
  {
    id: 'listening-1',
    number: 1,
    title: 'A new membership',
    context: 'A telephone conversation about joining a sports centre',
    groups: part1Groups,
    questions: part1Questions,
    transcript: [
      { speaker: 'Narrator', text: 'Section 1. You will hear a telephone conversation between a woman and a receptionist at a sports centre. First, you have some time to look at questions 1 to 10. Now listen carefully.' },
      { speaker: 'Mia', text: 'Good morning, Riverside Sports Centre. Mia speaking. How can I help?' },
      { speaker: 'Elena', text: 'Oh, hello. I’m calling about joining the centre. I had a look at your website last night.' },
      { speaker: 'Mia', text: 'Wonderful. I can take your details now if you’d like. Are you interested in a particular membership?' },
      { speaker: 'Elena', text: 'I’m not sure yet. Could you tell me a little about the options?' },
      { speaker: 'Mia', text: 'Of course. We have three main types. Standard membership is twenty-four pounds a month and gives you access to the gym and the swimming pool. Student membership is nineteen pounds, but you need a valid student card. Then there’s premium membership at thirty-eight pounds. That includes the gym, the pool, all the fitness classes, and the climbing wall.' },
      { speaker: 'Elena', text: 'The climbing wall sounds interesting. I’ve wanted to try that for ages.' },
      { speaker: 'Mia', text: 'It’s very popular. We run beginner sessions on Tuesday evenings.' },
      { speaker: 'Elena', text: 'Good to know. Let’s go with premium, then.' },
      { speaker: 'Mia', text: 'Lovely. Let me take some details. What’s your full name?' },
      { speaker: 'Elena', text: 'Elena Marsh. That’s M-A-R-S-H.' },
      { speaker: 'Mia', text: 'Marsh. And your address?' },
      { speaker: 'Elena', text: 'Forty-two Ellison Road. Ellison is spelled E-L-L-I-S-O-N.' },
      { speaker: 'Mia', text: 'Forty-two Ellison Road. And the postcode?' },
      { speaker: 'Elena', text: 'B-R-8, 4-Q-T.' },
      { speaker: 'Mia', text: 'B-R-8 4-Q-T. Is that Brighton?' },
      { speaker: 'Elena', text: 'That’s right.' },
      { speaker: 'Mia', text: 'Date of birth?' },
      { speaker: 'Elena', text: 'The seventeenth of March, nineteen ninety-one.' },
      { speaker: 'Mia', text: 'Thank you. And is there a particular activity you’re most interested in? It helps us arrange your induction.' },
      { speaker: 'Elena', text: 'Definitely the climbing wall. I’ve done a bit of indoor climbing before, but I’d like to improve.' },
      { speaker: 'Mia', text: 'I’ll put climbing down as your main interest. When would you like your membership to start?' },
      { speaker: 'Elena', text: 'The first of July, if that’s possible. I’m away for most of June.' },
      { speaker: 'Mia', text: 'That’s fine. Just so you know, if you start before the thirtieth of June there’s no joining fee, but from July the joining fee is twenty pounds.' },
      { speaker: 'Elena', text: 'Ah. Could I pay the joining fee now and still start in July?' },
      { speaker: 'Mia', text: 'Actually, yes — that’s a good idea. If you pay the joining fee today, we can hold the July rate. The monthly fee will be thirty-eight pounds.' },
      { speaker: 'Elena', text: 'Great. How do I pay?' },
      { speaker: 'Mia', text: 'Most people set up a direct debit. You can also pay by card each month, but there’s a small administration charge for that. Annual payment is possible too.' },
      { speaker: 'Elena', text: 'Direct debit is easiest.' },
      { speaker: 'Mia', text: 'Perfect. I’ll need an email address for the confirmation.' },
      { speaker: 'Elena', text: 'It’s elena dot marsh at brightmail dot com.' },
      { speaker: 'Mia', text: 'Let me check that: E-L-E-N-A dot M-A-R-S-H at B-R-I-G-H-T-M-A-I-L dot com.' },
      { speaker: 'Elena', text: 'Yes, that’s right.' },
      { speaker: 'Mia', text: 'Great. I’ll send everything over this afternoon. Your induction will be on the second of July at ten in the morning. Just bring some photo identification and a bank card for the direct debit.' },
      { speaker: 'Elena', text: 'Lovely. Thanks very much for your help.' },
      { speaker: 'Mia', text: 'You’re welcome. See you in July.' },
      { speaker: 'Narrator', text: 'That is the end of Part 1. You now have some time to check your answers.' },
    ],
  },
  {
    id: 'listening-2',
    number: 2,
    title: 'Harbour Museum summer programme',
    context: 'A museum guide introduces the summer events and the building layout',
    groups: part2Groups,
    questions: part2Questions,
    transcript: [
      { speaker: 'Narrator', text: 'Section 2. You will hear a guide talking to a group of visitors at the Harbour Museum. First, you have some time to look at questions 11 to 20. Now listen carefully.' },
      { speaker: 'Guide', text: 'Good afternoon, everyone, and welcome to the Harbour Museum. My name is Louise, and I’m the events coordinator here. I’d like to tell you about our Summer Discover programme before you explore the galleries.' },
      { speaker: 'Guide', text: 'This is the fifth year of the programme, and it has grown considerably. We’ve extended our opening hours on Thursdays, and entry to the permanent collection is now free. Special exhibitions still require a ticket. But the real headline this year is a series of outdoor workshops in the museum garden. We’ll be running them every Saturday throughout July and August.' },
      { speaker: 'Guide', text: 'For anyone interested in family history, we have two workshops each month. These sessions are designed for young people aged thirteen to seventeen, although parents are welcome to come along. They introduce the archives and show participants how to trace a family tree using local records.' },
      { speaker: 'Guide', text: 'One event I’d particularly recommend is the night tour. It begins at eight o’clock and lasts about ninety minutes. The route covers some uneven floors and a narrow staircase, so please wear comfortable shoes. We provide torches, and photography isn’t permitted because the light damages some of the objects.' },
      { speaker: 'Guide', text: 'The café is open every day except Monday, when it closes for staff training. During August it will stay open until eight in the evening, so you can have dinner after a late visit.' },
      { speaker: 'Guide', text: 'Now, how do you book? The quickest way is through our website. The phone line is often very busy in the summer, and while you can book at reception, we only hold a limited number of places there. So I’d strongly suggest booking online before you come.' },
      { speaker: 'Guide', text: 'Before you explore, let me explain where everything is. You’re standing in the main entrance, marked A on your map. Directly ahead is the ticketing desk. To your left is Gallery One, which houses our maritime collection, and beyond it Gallery Two, where the new photography exhibition opens next week. If you go through Gallery Two you’ll reach the Garden courtyard. The café is opposite the courtyard, close to the main entrance. The Lecture Theatre is at the far end of the building, past Gallery One. The Workshop Studio is beside the Lecture Theatre, with its own door onto the garden. The museum shop is by the entrance, on your right.' },
      { speaker: 'Guide', text: 'Now, for today’s events. At eleven o’clock, Dr Alan Pierce will give a talk on the history of the harbour. That will be in the Lecture Theatre. It’s free, but you need to collect a ticket from the desk.' },
      { speaker: 'Guide', text: 'The children’s craft sessions run all afternoon. They take place in the Workshop Studio, where there are large tables and plenty of materials. Parents need to stay with their children.' },
      { speaker: 'Guide', text: 'If you’re feeling hungry, refreshments are being served in the Garden courtyard. There’s a small stall selling cakes and sandwiches, and the café is also open as usual.' },
      { speaker: 'Guide', text: 'The new photography exhibition, “Harbour Light”, is in Gallery Two. It features work by local photographers and runs until the end of September.' },
      { speaker: 'Guide', text: 'Finally, this evening’s music performance will be in Gallery One at seven o’clock. The gallery will close to other visitors at half past six so the musicians can set up. I hope you enjoy your visit.' },
      { speaker: 'Narrator', text: 'That is the end of Part 2. You now have some time to check your answers.' },
    ],
  },
  {
    id: 'listening-3',
    number: 3,
    title: 'A campus food waste project',
    context: 'Two students discuss their research project and divide the work',
    groups: part3Groups,
    questions: part3Questions,
    transcript: [
      { speaker: 'Narrator', text: 'Section 3. You will hear two students, Priya and Tom, discussing a research project. First, you have some time to look at questions 21 to 30. Now listen carefully.' },
      { speaker: 'Priya', text: 'Hi, Tom. Did you manage to look at the reading list for the food waste project?' },
      { speaker: 'Tom', text: 'I did. There’s quite a lot on household waste and restaurant waste, but I couldn’t find anything about university cafés.' },
      { speaker: 'Priya', text: 'That’s exactly what I noticed. When I looked at the campus sustainability report, there was almost nothing about café waste. I thought that was strange, because thousands of meals are sold on campus every day.' },
      { speaker: 'Tom', text: 'So that’s our justification for the topic — a gap in local research. Our tutor will like that.' },
      { speaker: 'Priya', text: 'I hope so. The problem is going to be getting the data. I spoke to the manager of the main café yesterday. They don’t weigh what they throw away. Some cafés record the number of meals sold, others only their income, and one just counts the number of customers.' },
      { speaker: 'Tom', text: 'So the records are inconsistent. That makes comparison difficult.' },
      { speaker: 'Priya', text: 'Very. We’ll probably need to do our own survey as well.' },
      { speaker: 'Tom', text: 'What kind of survey?' },
      { speaker: 'Priya', text: 'A short questionnaire for students — what they buy, how often they leave food, and why. If it takes more than five minutes, people won’t finish it. Let’s keep it to eight or nine questions.' },
      { speaker: 'Tom', text: 'Agreed. But where do we find people? If we only stand outside the main café at lunchtime, we’ll mostly get students who eat there every day. That won’t represent the whole campus.' },
      { speaker: 'Priya', text: 'Good point. We could use the online student portal as well, and maybe ask at the library.' },
      { speaker: 'Tom', text: 'That should help. So what’s next? Should we talk to our supervisor?' },
      { speaker: 'Priya', text: 'She’s away until Thursday. I think we should test the questionnaire first — give it to about fifteen people and see whether the questions make sense.' },
      { speaker: 'Tom', text: 'A pilot. Good idea. Then we can revise it before we send it out properly.' },
      { speaker: 'Priya', text: 'Exactly. Now, how shall we divide the work? I’m happy to draft the literature review this week. I’ve already made notes on most of the articles.' },
      { speaker: 'Tom', text: 'Great. I’ll email the café managers and ask for access. I can also start analysing the sales and waste figures once they send them.' },
      { speaker: 'Priya', text: 'Perfect. What about the interviews? We said we’d speak to the café staff as well.' },
      { speaker: 'Tom', text: 'We could do those together. It’ll be easier to take notes if there are two of us.' },
      { speaker: 'Priya', text: 'Yes, let’s do that. And the final presentation — shall we prepare it together as well?' },
      { speaker: 'Tom', text: 'Definitely. I don’t want to present on my own.' },
      { speaker: 'Priya', text: 'Nor do I. OK, I’ll send you the draft literature review by Friday.' },
      { speaker: 'Narrator', text: 'That is the end of Part 3. You now have some time to check your answers.' },
    ],
  },
  {
    id: 'listening-4',
    number: 4,
    title: 'City bees',
    context: 'A lecture about bees living in urban environments',
    groups: part4Groups,
    questions: part4Questions,
    transcript: [
      { speaker: 'Narrator', text: 'Section 4. You will hear a lecture about bees in cities. First, you have some time to look at questions 31 to 40. Now listen carefully.' },
      { speaker: 'Lecturer', text: 'Good morning. Today I want to talk about an animal that many people are surprised to find in cities: the bee. When we think of bees, we usually imagine wildflower meadows or orchards in the countryside. But over the past twenty years, researchers have discovered that towns and cities can be surprisingly good places for many bee species.' },
      { speaker: 'Lecturer', text: 'One reason is that cities can actually offer greater plant diversity than the farmland around them. Gardens, parks, balconies and roadside verges contain an enormous variety of flowers, often planted by people. A single city garden may contain more species than a large field of a single crop. For bees that feed on many different plants, this variety is valuable.' },
      { speaker: 'Lecturer', text: 'But flowers are only one requirement. Like all insects, bees need food, shelter and water. Water is often overlooked. Ponds, birdbaths and even shallow puddles provide the moisture that bees need, especially in hot weather.' },
      { speaker: 'Lecturer', text: 'The urban climate also affects bee behaviour. Cities are warmer than the surrounding countryside because of all the concrete and asphalt, which absorb heat. This can cause queen bees to emerge earlier in the year. In some years, queens may appear several weeks before their rural relatives. That can be an advantage if flowers are also available early, but it creates a risk if a cold spell follows.' },
      { speaker: 'Lecturer', text: 'To study these changes, scientists need to monitor colonies closely. One technique is to place tiny microphones inside hives. The microphones record the sound of the colony, and researchers can detect changes in the bees’ buzzing that may indicate stress, disease or the loss of a queen. It’s a remarkable example of how technology can help us understand insects without opening the hive.' },
      { speaker: 'Lecturer', text: 'Now, not all urban habitats are equally good. A study in Melbourne, Australia, compared the bee communities in private gardens with those in public parks. The gardens supported a greater number of species. The researchers suggested that this was because gardens contained more varieties of flowers and more sheltered corners. Parks were often mown too frequently and had fewer flowering plants.' },
      { speaker: 'Lecturer', text: 'However, small gardens on their own may not be enough to sustain a population. Connectivity matters. Roof gardens and green roofs can act as stepping stones between larger green spaces, allowing bees to move across the city. Even a small balcony can play a part if it is planted with the right flowers.' },
      { speaker: 'Lecturer', text: 'There are risks, too. One study collected pollen from urban hives and found traces of pesticides in the samples. The levels were usually low, but the finding shows that cities are not free from agricultural chemicals. Gardeners can help by avoiding pesticides and choosing native plants.' },
      { speaker: 'Lecturer', text: 'Finally, I want to mention a citizen science project called BeeWatch. Volunteers record sightings of bees in their local area using a mobile app. The project has produced thousands of records and helped researchers identify where particular species are thriving. If you’d like to take part, the best time to record sightings is early morning, when bees are still warming up and are easier to photograph. And if you have a garden, one of the simplest things you can do is leave a pile of dead wood in a corner. Many solitary bees nest in dead wood, and it costs nothing.' },
      { speaker: 'Lecturer', text: 'So, cities are not simply a poor substitute for the countryside. With thoughtful planting and a little tolerance for untidiness, they can become valuable habitats for a wide range of bees.' },
      { speaker: 'Narrator', text: 'That is the end of Part 4. You now have some time to check your answers. This is the end of the listening test.' },
    ],
  },
]

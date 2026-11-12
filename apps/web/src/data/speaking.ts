import type { SpeakingPart } from '../lib/types'

export const speakingParts: SpeakingPart[] = [
  {
    id: 'speaking-1',
    number: 1,
    title: 'Part 1 — Introduction and interview',
    description: 'The examiner will ask you about familiar topics. Answer naturally and develop each answer with a reason or example. This part lasts 4–5 minutes.',
    questions: [
      { id: 's1', text: 'Let’s talk about where you live. Do you live in a house or an apartment?' },
      { id: 's2', text: 'What do you like most about your neighbourhood?' },
      { id: 's3', text: 'Is there anything you would change about where you live?' },
      { id: 's4', text: 'Do you plan to stay in that area for a long time?' },
      { id: 's5', text: 'Now let’s move on to reading. Do you enjoy reading?' },
      { id: 's6', text: 'What kinds of books or articles did you read as a child?' },
      { id: 's7', text: 'Do you prefer paper books or digital books? Why?' },
      { id: 's8', text: 'When do you usually find time to read?' },
      { id: 's9', text: 'Let’s talk about your daily routine. Are you a morning person or an evening person?' },
      { id: 's10', text: 'What is the first thing you usually do after you wake up?' },
      { id: 's11', text: 'Has your daily routine changed in recent years?' },
      { id: 's12', text: 'Is there anything you would like to change about your routine?' },
    ],
  },
  {
    id: 'speaking-2',
    number: 2,
    title: 'Part 2 — Individual long turn',
    description: 'You have one minute to prepare. You may make notes. Then speak for one to two minutes. The examiner will tell you when to begin and stop.',
    questions: [],
    cueCard: {
      topic: 'Describe a place you like to go to relax.',
      bullets: [
        'where this place is',
        'how often you go there',
        'what you usually do there',
        'and explain why this place helps you relax.',
      ],
      rounding: 'Is this a place you would recommend to other people?',
      preparationSeconds: 60,
      speakingSeconds: 120,
    },
  },
  {
    id: 'speaking-3',
    number: 3,
    title: 'Part 3 — Two-way discussion',
    description: 'The examiner will ask more abstract questions connected to the topic in Part 2. Give extended answers and support your ideas with examples.',
    questions: [
      { id: 's13', text: 'Why do some people find it difficult to relax in modern cities?' },
      { id: 's14', text: 'What kinds of public spaces should cities provide so that people can relax?' },
      { id: 's15', text: 'Do you think people spend less time relaxing today than in the past?' },
      { id: 's16', text: 'How has technology changed the way people relax?' },
      { id: 's17', text: 'Should employers be responsible for helping workers manage stress?' },
      { id: 's18', text: 'Do older and younger people relax in different ways?' },
    ],
  },
]

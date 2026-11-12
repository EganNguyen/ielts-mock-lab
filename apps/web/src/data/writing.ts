import type { WritingTask } from '../lib/types'

export const writingTasks: WritingTask[] = [
  {
    id: 'writing-1',
    number: 1,
    title: 'Task 1 — Report',
    prompt: 'The bar chart below shows the percentage of adults in one country who used the internet in 2010 and 2022, by age group. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.',
    instructions: [
      'Write at least 150 words.',
      'You should spend about 20 minutes on this task.',
      'Write a report for a university lecturer. Do not give your opinion.',
    ],
    minimumWords: 150,
    suggestedMinutes: 20,
    chart: 'internet',
    modelAnswer: `The bar chart compares internet use among five age groups in a single country in 2010 and 2022. Overall, the proportion of adults using the internet rose in every age group over the twelve-year period, and the gap between younger and older users narrowed substantially.

In 2010, internet use was highest among 18–29-year-olds, at 76%, followed by the 30–44 group at 68%. Usage fell steadily with age: 45% of those aged 45–59 were online, compared with only 23% of 60–74-year-olds and just 8% of people aged 75 and over.

By 2022, the pattern had changed dramatically. Almost all 18–29-year-olds (98%) and 95% of 30–44-year-olds used the internet. The most striking increase occurred among older adults. The figure for the 45–59 group climbed to 87%, while usage among 60–74-year-olds more than tripled to 70%. Even in the oldest group, the proportion rose from 8% to 38%, although this remained well below the national average.

In short, the data show both a general expansion of internet access and a significant reduction in the age gap. Nevertheless, a clear generational difference persisted in 2022, with older adults still considerably less likely to be online than younger people.`,
    modelHighlights: [
      'A clear overview in the introduction: overall rise plus narrowing gap.',
      'Data is grouped logically, with 2010 and 2022 compared rather than listed mechanically.',
      'Precise figures are used selectively, and the most striking change (older adults) is highlighted.',
      'No opinion or speculation is included.',
      'Vocabulary of change and comparison is varied: “climbed”, “more than tripled”, “narrowed”, “well below”.',
    ],
  },
  {
    id: 'writing-2',
    number: 2,
    title: 'Task 2 — Essay',
    prompt: 'Some people believe that universities should only offer courses that lead to well-paid jobs. Others think that universities should teach subjects that benefit society, even if graduates earn less.\n\nDiscuss both views and give your own opinion.',
    instructions: [
      'Write at least 250 words.',
      'You should spend about 40 minutes on this task.',
      'Give reasons for your answer and include any relevant examples from your own knowledge or experience.',
    ],
    minimumWords: 250,
    suggestedMinutes: 40,
    modelAnswer: `Debate about the purpose of higher education often sets economic value against social value. Some argue that universities should concentrate on courses that lead directly to well-paid employment, while others believe that subjects of wider social importance deserve support even when their graduates earn less. In my view, a healthy university system needs both, but public funding should not be determined by salary outcomes alone.

Those who favour employment-focused courses make a reasonable case. Students typically invest several years and a considerable sum in their degrees, and they are entitled to expect that their qualification will improve their job prospects. Courses in engineering, medicine, computer science and finance provide obvious routes into secure careers, and economies need these graduates. If universities expanded only in fields with little labour-market demand, they might produce disillusioned graduates with large debts and limited options. From this perspective, a degree is partly a private investment, and its economic return matters.

On the other hand, a university is not merely a training provider. Subjects such as history, philosophy, social work and the arts help societies understand themselves, preserve culture and address problems that markets do not price. A social worker or a teacher may earn less than a software engineer, but their contribution to public life is substantial. Moreover, the benefits of research in the humanities are often indirect and long-term: they shape public debate, inform policy and enrich civic life. If funding were tied only to graduate salaries, these fields would shrink, and the loss would be felt across society rather than in any single balance sheet.

In my opinion, the two aims are not as opposed as they appear. Universities should ensure that every course develops transferable skills — communication, analysis, collaboration — that graduates can use in a range of careers. At the same time, governments should support subjects of social value through grants, scholarships and public-sector pathways rather than expecting students alone to bear the risk. A law graduate may work in a commercial firm; a philosophy graduate may become a teacher, a civil servant or a technology ethicist. The value of a degree cannot be reduced to a starting salary.

In conclusion, employment outcomes are a legitimate concern, but they should not be the sole measure of a university's worth. A balanced system would prepare students for work while protecting the subjects that sustain a thoughtful and functioning society.`,
    modelHighlights: [
      'Both views are developed fully before the writer’s own position is advanced.',
      'The position is clear and consistent: economic and social value are both necessary, but funding should not be salary-driven.',
      'Each paragraph has a controlling idea, explanation and example.',
      'Cohesion is natural: “from this perspective”, “on the other hand”, “moreover”, “in conclusion”.',
      'Precise vocabulary: “labour-market demand”, “indirect and long-term”, “transferable skills”, “public-sector pathways”.',
    ],
  },
]

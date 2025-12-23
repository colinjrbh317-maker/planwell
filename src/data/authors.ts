// Author data for PlanWell blog
// Extracted from existing website content (about.astro, index.astro)

export interface Author {
  slug: string;
  name: string;
  credentials: string;
  title: string;
  image: string;
  bioShort: string;
  bioFull: string;
  personalNote: string;
  email: string;
  phone: string;
}

export const authors: Record<string, Author> = {
  'brennan-rhule': {
    slug: 'brennan-rhule',
    name: 'Brennan Rhule',
    credentials: 'CFP®, ChFEBC℠, AIF®',
    title: 'Co-Founder & Financial Planner',
    image: '/images/authors/brennan-rhule.png',
    bioShort: "Virginia Tech CFP® graduate, 15+ years in the DC area. Brennan's mission is to cut through the complexity so you can retire with confidence.",
    bioFull: `Brennan graduated from Virginia Tech's CFP Board-Registered program and has spent over 15 years in the Washington, DC area working with federal employees. His experience led him to earn the ChFEBC℠ designation—becoming a true specialist in federal benefits.

Brennan's mission is simple: cut through the complexity. Federal retirement rules can feel overwhelming, but with the right guidance, every employee can retire with confidence. He loves seeing the weight lift off clients' shoulders when they finally have a clear plan.`,
    personalNote: "Brennan now calls Salem, VA home with his family. He's passionate about backpacking, rock climbing, and ice hockey—and you'll often find him adventuring in the Blue Ridge Mountains with his golden retriever and bernese mountain dog.",
    email: 'brennan.rhule@planwellfp.com',
    phone: '571-543-2783'
  },
  'david-fei': {
    slug: 'david-fei',
    name: 'David Fei',
    credentials: 'CFP®, ChFEBC℠, AIF®',
    title: 'Co-Founder & Financial Planner',
    image: '/images/authors/david-fei.jpg',
    bioShort: "20+ years helping federal families plan for life's challenges. David believes retirement planning should give you peace of mind, not more anxiety.",
    bioFull: `David has been in the financial services industry for over 20 years, bringing a wide range of experience in personal finance to every client relationship. He specializes in helping federal families tackle life's biggest financial challenges—retirement income planning, educational funding, and investment strategy.

David's approach is grounded in education. He believes that when clients truly understand their options, they make better decisions. That's why he takes the time to explain the "why" behind every recommendation.`,
    personalNote: "David stays busy with his daughters' activities, plays basketball on weekends, and hits the mountain bike trails whenever he can.",
    email: 'david.fei@planwellfp.com',
    phone: '301-388-5489'
  },
  'ben-derge': {
    slug: 'ben-derge',
    name: 'Ben Derge',
    credentials: '',
    title: 'Content Writer',
    image: '/images/authors/ben-derge.jpg',
    bioShort: 'Ben specializes in making complex federal retirement topics accessible and easy to understand.',
    bioFull: 'Ben brings clarity to federal retirement planning through well-researched articles and guides. His writing helps federal employees navigate FERS, TSP, and other benefits with confidence.',
    personalNote: '',
    email: '',
    phone: ''
  },
  'planwell-team': {
    slug: 'planwell-team',
    name: 'PlanWell Team',
    credentials: '',
    title: 'PlanWell Financial Planning',
    image: '/images/authors/planwell-logo.png',
    bioShort: 'Expert insights from the PlanWell Financial Planning team.',
    bioFull: 'The PlanWell team combines decades of experience in federal employee benefits to provide trusted guidance on FERS, TSP, FEHB, and retirement planning.',
    personalNote: '',
    email: 'info@planwellfp.com',
    phone: ''
  }
};

// Helper to get author by slug
export function getAuthor(slug: string): Author | undefined {
  return authors[slug];
}

// Helper to get author by name (for legacy data)
export function getAuthorByName(name: string): Author | undefined {
  if (name.includes('Brennan')) return authors['brennan-rhule'];
  if (name.includes('David')) return authors['david-fei'];
  if (name.includes('Ben') || name.includes('Derge')) return authors['ben-derge'];
  if (name.includes('PlanWell') || name.includes('Team')) return authors['planwell-team'];
  return authors['planwell-team']; // Default fallback
}

// Get all authors (excluding team placeholder)
export function getAllAuthors(): Author[] {
  return Object.values(authors).filter(a => a.slug !== 'planwell-team');
}

/**
 * EduPredict AI — Computer Science Course Structure
 * Derived from the dataset workbook Course_Structure sheet.
 * Types: C = Core, E = Elective, U = University, V = NUC/Vocational
 *
 * Key used in the form:
 *   'Core'        → auto-loaded, locked
 *   'Elective'    → user picks from options
 *   'University'  → auto-loaded, locked
 *   'NUC'         → auto-loaded, locked (V-type courses)
 *
 * Only courses that appear as _CA columns in the dataset are listed.
 * 300 Omega is excluded (SIWES — not in prediction model).
 */

// ── 100 Alpha (Level 100, First Semester) ────────────────────────────────────
// No previous scores — uses Entry_Academic_Score instead.
// CA columns from dataset: BIO111,CHM111,CHM119,CIT111,CSC111,MAT111,MAT112,PHY111,PHY119,CST111,GST111,EDS111,TMC111,TMC112
export const COURSES_100_ALPHA = {
  core: [
    { code: 'BIO111',  title: 'General Biology I',                                                        units: 3 },
    { code: 'CHM111',  title: 'General Physical Chemistry',                                               units: 3 },
    { code: 'CHM119',  title: 'General Chemistry Practical I',                                            units: 1 },
    { code: 'CIT111',  title: 'Microsoft Office Specialist (MS Word)',                                    units: 0 },
    { code: 'CSC111',  title: 'Introduction to Computer Science',                                         units: 3 },
    { code: 'MAT111',  title: 'Algebra',                                                                  units: 3 },
    { code: 'MAT112',  title: 'Trigonometry and Analytical Geometry',                                     units: 2 },
    { code: 'PHY111',  title: 'Mechanics and Properties of Matter',                                       units: 2 },
    { code: 'PHY119',  title: 'Physics Practical I',                                                      units: 1 },
  ],
  electives: [],
  university: [
    { code: 'CST111',  title: 'Use of Library, Study Skills & ICT I',                                    units: 2 },
    { code: 'GST111',  title: 'Communication in English I',                                               units: 2 },
  ],
  nuc: [
    { code: 'EDS111',  title: 'Entrepreneurial Development Studies I',                                    units: 1 },
    { code: 'TMC111',  title: 'Total Man Concept I',                                                      units: 1 },
    { code: 'TMC112',  title: 'Total Man Concept – Sports I',                                             units: 0 },
  ],
}

// ── 100 Omega (Level 100, Second Semester) ────────────────────────────────────
// Previous scores: PREV_CIT121,PREV_CIT141,PREV_CSC121,PREV_CSC125,PREV_MAT121,PREV_MAT122,
//                 PREV_PHY121,PREV_PHY122,PREV_PHY129,PREV_CST121,PREV_GST121,PREV_GST122,
//                 PREV_EDS121,PREV_TMC121,PREV_TMC122
export const COURSES_100_OMEGA = {
  core: [
    { code: 'CIT121',  title: 'Microsoft Office Specialist (MS Excel)',                                   units: 0 },
    { code: 'CIT141',  title: 'COMPTIA II',                                                               units: 0 },
    { code: 'CSC121',  title: 'Introduction to Problem Solving',                                          units: 2 },
    { code: 'CSC125',  title: 'Operating System I',                                                       units: 2 },
    { code: 'MAT121',  title: 'Calculus',                                                                 units: 3 },
    { code: 'MAT122',  title: 'Introduction to Vector Analysis',                                          units: 2 },
    { code: 'PHY121',  title: 'Electricity and Magnetism I',                                              units: 3 },
    { code: 'PHY122',  title: 'Atomic and Nuclear Physics',                                               units: 2 },
    { code: 'PHY129',  title: 'Physics Practical II',                                                     units: 1 },
  ],
  electives: [],
  university: [
    { code: 'CST121',  title: 'Use of Library, Study Skills & ICT II',                                   units: 2 },
    { code: 'GST121',  title: 'Communication in English II',                                              units: 2 },
    { code: 'GST122',  title: 'Communication in French',                                                  units: 2 },
  ],
  nuc: [
    { code: 'EDS121',  title: 'Entrepreneurial Development Studies II',                                   units: 1 },
    { code: 'TMC121',  title: 'Introduction to the Total Man Concept II',                                 units: 1 },
    { code: 'TMC122',  title: 'Total Man Concept – Sports II',                                            units: 0 },
  ],
}

// ── 200 Alpha (Level 200, First Semester) ─────────────────────────────────────
// Elective options: ACC111, ECN111, MAT213, MAT214, MAT215
export const COURSES_200_ALPHA = {
  core: [
    { code: 'CIT211',  title: 'Java Foundations Certified Junior Associate',                              units: 0 },
    { code: 'CSC211',  title: 'Computer Programming I',                                                   units: 3 },
    { code: 'CSC213',  title: 'Structured Programming',                                                   units: 3 },
    { code: 'CSC214',  title: 'High Performance Computing & Database Management I',                       units: 3 },
    { code: 'CSC216',  title: 'Foundations of Sequential and Parallel Programming',                       units: 3 },
    { code: 'MAT212',  title: 'Mathematical Methods I',                                                   units: 3 },
    { code: 'PHY232',  title: 'Electric Circuit and Electronics',                                         units: 3 },
  ],
  electiveOptions: [
    { code: 'ACC111',  title: 'Principles of Accounting I',                                               units: 2 },
    { code: 'ECN111',  title: 'Introduction to Economics I',                                              units: 3 },
    { code: 'MAT213',  title: 'Differential Equations I',                                                 units: 3 },
    { code: 'MAT214',  title: 'Linear Algebra I',                                                         units: 2 },
    { code: 'MAT215',  title: 'Probability Distribution I',                                               units: 3 },
  ],
  university: [
    { code: 'GST211',  title: 'Logic, Philosophy and Human Existence',                                    units: 2 },
  ],
  nuc: [
    { code: 'DLD111',  title: 'Foundations of Leadership Development',                                    units: 0 },
    { code: 'EDS211',  title: 'Entrepreneurial Development Studies III',                                  units: 1 },
    { code: 'TMC211',  title: 'Total Man Concept III',                                                    units: 1 },
    { code: 'TMC212',  title: 'Total Man Concept – Sports III',                                           units: 0 },
  ],
}

// ── 200 Omega (Level 200, Second Semester) ────────────────────────────────────
// Elective options: CSC226, MAT225, MAT226, MAT229, MIS221
export const COURSES_200_OMEGA = {
  core: [
    { code: 'CSC221',  title: 'Computer Programming II',                                                  units: 3 },
    { code: 'CSC223',  title: 'Computer Hardware',                                                        units: 3 },
    { code: 'CSC224',  title: 'Introduction to Computational Biology',                                    units: 2 },
    { code: 'CSC225',  title: 'Operating Systems',                                                        units: 3 },
    { code: 'CSC227',  title: 'Computer Architecture and Organization I',                                 units: 2 },
  ],
  electiveOptions: [
    { code: 'CSC226',  title: 'Statistical Methods',                                                      units: 2 },
    { code: 'MAT225',  title: 'Abstract Algebra',                                                         units: 3 },
    { code: 'MAT226',  title: 'Regression and Analysis of Variance',                                      units: 3 },
    { code: 'MAT229',  title: 'Linear Algebra II',                                                        units: 2 },
    { code: 'MIS221',  title: 'Introduction to Management Information System',                            units: 3 },
  ],
  university: [
    { code: 'GST221',  title: 'Nigerian People and Culture',                                              units: 2 },
    { code: 'GST222',  title: 'Peace and Conflict Studies',                                               units: 2 },
  ],
  nuc: [
    { code: 'CIT221',  title: 'Oracle Database: SQL Fundamentals',                                        units: 0 },
    { code: 'CIT224',  title: 'SAP TERP10 – Integration of Business Processes II',                       units: 0 },
    { code: 'DLD121',  title: 'Leadership Pathways',                                                      units: 0 },
    { code: 'EDS221',  title: 'Entrepreneurial Development Studies IV',                                   units: 1 },
    { code: 'TMC221',  title: 'Total Man Concept IV',                                                     units: 1 },
    { code: 'TMC222',  title: 'Total Man Concept – Sports IV',                                            units: 0 },
  ],
}

// ── 300 Alpha (Level 300, First Semester) ─────────────────────────────────────
// Elective options: CIS319, CSC314, CSC319
export const COURSES_300_ALPHA = {
  core: [
    { code: 'CSC310',  title: 'Internet Programming',                                                     units: 3 },
    { code: 'CSC312',  title: 'Fundamentals of Data Structures',                                          units: 3 },
    { code: 'CSC313',  title: 'Object-Oriented Programming',                                              units: 3 },
    { code: 'CSC316',  title: 'Research Methods',                                                         units: 2 },
    { code: 'CSC317',  title: 'Systems Analysis and Design',                                              units: 2 },
    { code: 'CSC318',  title: 'Compiler Construction I',                                                  units: 3 },
  ],
  electiveOptions: [
    { code: 'CIS319',  title: 'Statistical Computing',                                                    units: 2 },
    { code: 'CSC314',  title: 'Theory of Computing',                                                      units: 2 },
    { code: 'CSC319',  title: 'Operations Research',                                                      units: 2 },
  ],
  university: [
    { code: 'GST311',  title: 'History and Philosophy of Science',                                        units: 2 },
  ],
  nuc: [
    { code: 'CIT310',  title: 'Cyber Security Specialist – Application Security',                         units: 0 },
    { code: 'EDS311',  title: 'Entrepreneurial Development Studies V',                                    units: 1 },
    { code: 'TMC311',  title: 'Total Man Concept V',                                                      units: 1 },
    { code: 'TMC312',  title: 'Total Man Concept – Sports V',                                             units: 0 },
  ],
}

// ── 400 Alpha (Level 400, First Semester) ─────────────────────────────────────
// Elective options: CSC436, MIS415
export const COURSES_400_ALPHA = {
  core: [
    { code: 'CSC411',  title: 'Software Engineering',                                                     units: 3 },
    { code: 'CSC413',  title: 'Algorithms and Complexity Analysis',                                       units: 3 },
    { code: 'CSC415',  title: 'Artificial Intelligence',                                                  units: 3 },
    { code: 'CSC416',  title: 'Discrete Structure',                                                       units: 3 },
    { code: 'CSC431',  title: 'Computational Science and Numerical Methods',                              units: 3 },
    { code: 'CSC433',  title: 'Computer Graphics and Animation',                                          units: 2 },
  ],
  electiveOptions: [
    { code: 'CSC436',  title: 'Compiler Construction II',                                                 units: 2 },
    { code: 'MIS415',  title: 'Project Management',                                                       units: 2 },
  ],
  university: [],
  nuc: [
    { code: 'DLD211',  title: 'Leadership and Developmental Studies',                                     units: 0 },
    { code: 'EDS411',  title: 'Entrepreneurial Development Studies VII',                                  units: 1 },
    { code: 'TMC411',  title: 'Total Man Concept VII',                                                    units: 1 },
    { code: 'TMC412',  title: 'Total Man Concept – Sports VII',                                           units: 0 },
  ],
}

// ── 400 Omega (Level 400, Second Semester) ────────────────────────────────────
// Elective options: CSC442, CSC443, CSC444, CSC446
export const COURSES_400_OMEGA = {
  core: [
    { code: 'CIS421',  title: 'Computer Security',                                                        units: 2 },
    { code: 'CSC423',  title: 'Organization of Programming Languages',                                    units: 3 },
    { code: 'CSC424',  title: 'Computer Networks/Communication',                                          units: 3 },
    { code: 'CSC425',  title: 'Computer Architecture and Organization II',                                units: 3 },
    { code: 'CSC429',  title: 'Project',                                                                  units: 6 },
    { code: 'CSC441',  title: 'Human-Computer Interface (HCI)',                                           units: 2 },
  ],
  electiveOptions: [
    { code: 'CSC442',  title: 'Computational Biology & Interdisciplinary Topics',                         units: 2 },
    { code: 'CSC443',  title: 'Modeling & Simulations',                                                   units: 2 },
    { code: 'CSC444',  title: 'Computer System Performance Evaluation',                                   units: 2 },
    { code: 'CSC446',  title: 'Distributed Computing Systems',                                            units: 2 },
  ],
  university: [],
  nuc: [
    { code: 'DLD221',  title: 'Leadership Dynamics',                                                      units: 0 },
    { code: 'EDS421',  title: 'Entrepreneurial Development Studies VIII',                                 units: 1 },
    { code: 'TMC421',  title: 'Total Man Concept VIII',                                                   units: 1 },
    { code: 'TMC422',  title: 'Total Man Concept – Sports VIII',                                          units: 0 },
    { code: 'TTG222',  title: 'Leadership Dynamics',                                                      units: 0 },
  ],
}

// ── Lookup helper ─────────────────────────────────────────────────────────────
/**
 * getCourseSet(level, semester)
 * Returns the course set for the given level (100/200/300/400) and
 * semester ('Alpha'/'Omega'), or null if the combination is invalid
 * (e.g. 300 Omega = SIWES, not in model).
 *
 * Semester mapping used in the form:
 *   'First'  → Alpha
 *   'Second' → Omega
 */
export function getCourseSet(level, semester) {
  const key = `${level}_${semester === 'First' ? 'Alpha' : 'Omega'}`
  const map = {
    '100_Alpha': COURSES_100_ALPHA,
    '100_Omega': COURSES_100_OMEGA,
    '200_Alpha': COURSES_200_ALPHA,
    '200_Omega': COURSES_200_OMEGA,
    '300_Alpha': COURSES_300_ALPHA,
    '400_Alpha': COURSES_400_ALPHA,
    '400_Omega': COURSES_400_OMEGA,
  }
  return map[key] ?? null
}

/**
 * is100Alpha(level, semester) — special case where Entry_Academic_Score
 * replaces previous course scores.
 */
export function is100Alpha(level, semester) {
  return Number(level) === 100 && semester === 'First'
}

/**
 * isSIWES(level, semester) — 300 Omega is excluded from the model.
 */
export function isSIWES(level, semester) {
  return Number(level) === 300 && semester === 'Second'
}

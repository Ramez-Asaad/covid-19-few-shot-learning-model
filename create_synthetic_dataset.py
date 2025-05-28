import json
import random
from datetime import datetime, timedelta
import logging
import numpy as np
from faker import Faker

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Faker for more realistic names
fake = Faker()

# Sample data for generating synthetic papers
CATEGORIES = [
    'Treatment',
    'Vaccine Development',
    'Epidemiology',
    'Clinical Diagnosis',
    'Immunology',
    'Public Health',
    'Virology'
]

INSTITUTIONS = [
    'Harvard Medical School',
    'Johns Hopkins University',
    'Stanford University School of Medicine',
    'Oxford University',
    'Massachusetts General Hospital',
    'National Institutes of Health',
    'Centers for Disease Control and Prevention',
    'Mayo Clinic',
    'University of California San Francisco',
    'Pasteur Institute',
    'Yale School of Medicine',
    'Cleveland Clinic',
    'Imperial College London',
    'Karolinska Institute',
    'University of Toronto',
    'Beijing University',
    'Seoul National University',
    'Singapore General Hospital',
    'Max Planck Institute',
    'Robert Koch Institute'
]

JOURNALS = [
    'Nature Medicine',
    'The Lancet',
    'JAMA',
    'New England Journal of Medicine',
    'Science',
    'Cell',
    'BMJ',
    'Clinical Infectious Diseases',
    'Emerging Infectious Diseases',
    'Vaccine'
]

KEYWORDS = {
    'Treatment': [
        'therapeutic', 'treatment', 'drug', 'medication', 'therapy',
        'clinical trial', 'antiviral', 'remdesivir', 'dexamethasone',
        'monoclonal antibodies', 'hospitalization', 'patient care',
        'therapeutic intervention', 'drug efficacy', 'adverse effects',
        'treatment outcome', 'standard of care', 'clinical management'
    ],
    'Vaccine Development': [
        'vaccine', 'immunization', 'antibody', 'immune response',
        'clinical trial', 'mRNA', 'booster', 'efficacy', 'safety',
        'neutralizing antibodies', 'vaccine platform', 'adjuvant',
        'immunogenicity', 'vaccine candidate', 'phase trial',
        'protective immunity', 'vaccine safety', 'antibody response'
    ],
    'Epidemiology': [
        'transmission', 'spread', 'outbreak', 'population',
        'contact tracing', 'R0', 'infection rate', 'mortality',
        'case fatality rate', 'epidemiological model', 'surveillance',
        'disease burden', 'risk factor', 'demographic', 'incidence',
        'prevalence', 'superspreading', 'cluster analysis'
    ],
    'Clinical Diagnosis': [
        'diagnosis', 'testing', 'PCR', 'symptoms', 'screening',
        'detection', 'biomarker', 'diagnostic', 'rapid test',
        'false negative', 'sensitivity', 'specificity', 'CT scan',
        'clinical presentation', 'laboratory findings', 'diagnostic accuracy',
        'point-of-care', 'molecular diagnosis'
    ],
    'Immunology': [
        'immune system', 'cytokine', 'T cells', 'B cells', 'antibodies',
        'innate immunity', 'adaptive immunity', 'inflammatory response',
        'immunopathology', 'autoimmunity', 'immune regulation',
        'cellular immunity', 'humoral immunity', 'immunological memory',
        'cytokine storm', 'immune evasion', 'host response'
    ],
    'Public Health': [
        'public health', 'prevention', 'intervention', 'policy',
        'social distancing', 'mask wearing', 'health system',
        'healthcare workers', 'community transmission', 'quarantine',
        'isolation', 'health disparities', 'public awareness',
        'health education', 'risk communication', 'health policy',
        'preventive measures', 'population health'
    ],
    'Virology': [
        'viral structure', 'genome sequence', 'mutation', 'variant',
        'viral load', 'viral shedding', 'pathogenesis', 'replication',
        'spike protein', 'ACE2 receptor', 'viral entry', 'strain',
        'viral evolution', 'host cell', 'viral tropism',
        'genetic diversity', 'viral dynamics', 'molecular structure'
    ]
}

TITLE_TEMPLATES = {
    'Treatment': [
        "Clinical Outcomes of {treatment} in COVID-19 Patients: A {study_type}",
        "Effectiveness of {treatment} for Treating COVID-19: {study_type}",
        "Comparative Analysis of {treatment} versus Standard Care in COVID-19 Management",
        "Real-world Evidence for {treatment} in COVID-19 Treatment",
        "Safety and Efficacy of {treatment} in Hospitalized COVID-19 Patients",
        "{treatment} for COVID-19: Results from a {study_type}",
        "Treatment of Severe COVID-19 with {treatment}: {location} Experience",
        "Optimal Timing of {treatment} Administration in COVID-19 Patients",
        "Risk-Benefit Assessment of {treatment} in COVID-19 Treatment",
        "Clinical Benefits of Early {treatment} Intervention in COVID-19"
    ],
    'Vaccine Development': [
        "Safety and Immunogenicity of {vaccine_type} COVID-19 Vaccine: Phase {phase} Trial Results",
        "Durability of Immune Response Following {vaccine_type} Vaccination",
        "Development and Validation of {vaccine_type} COVID-19 Vaccine",
        "Antibody Response to {vaccine_type} COVID-19 Vaccine in {population}",
        "Comparative Analysis of {vaccine_type} Vaccines Against COVID-19",
        "Long-term Follow-up of {vaccine_type} Vaccine Recipients",
        "Booster Dose Effects of {vaccine_type} COVID-19 Vaccine",
        "Cross-protection of {vaccine_type} Vaccine Against SARS-CoV-2 Variants",
        "Immune Response Kinetics Following {vaccine_type} Vaccination",
        "Real-world Effectiveness of {vaccine_type} COVID-19 Vaccine"
    ]
}

def generate_authors(num_authors=None):
    """Generate a realistic list of authors with affiliations."""
    if num_authors is None:
        # Slightly increase the range for more variety
        num_authors = random.randint(3, 10)
    
    authors = []
    # Select primary institution and some related ones
    primary_institution = random.choice(INSTITUTIONS)
    related_institutions = random.sample([i for i in INSTITUTIONS if i != primary_institution], 
                                      min(num_authors - 1, len(INSTITUTIONS) - 1))
    all_institutions = [primary_institution] + related_institutions
    
    for i in range(num_authors):
        # Higher chance of using primary institution for first authors
        if i < 2:
            affiliation = primary_institution
        else:
            affiliation = random.choice(all_institutions)
            
        author = {
            'name': fake.name(),
            'affiliation': affiliation,
            'email': fake.email()
        }
        authors.append(author)
    
    return authors

def generate_abstract(category, keywords):
    """Generate a more natural-looking abstract with proper structure."""
    background = random.choice([
        f"The COVID-19 pandemic continues to present significant challenges in {category.lower()} and healthcare management.",
        f"Understanding the role of {category.lower()} in COVID-19 remains crucial for effective pandemic response.",
        f"Recent advances in COVID-19 {category.lower()} have opened new avenues for research and intervention.",
        f"The emergence of new SARS-CoV-2 variants necessitates ongoing research in {category.lower()}.",
        f"Global efforts to combat COVID-19 through {category.lower()} continue to evolve.",
        f"The dynamic nature of SARS-CoV-2 highlights the importance of {category.lower()} research."
    ])
    
    selected_keywords = random.sample(keywords, min(4, len(keywords)))
    methods = f"In this {random.choice(['prospective', 'retrospective', 'observational', 'multicenter', 'longitudinal', 'cross-sectional'])} study, we {random.choice(['investigated', 'evaluated', 'analyzed', 'examined', 'assessed', 'explored'])} the role of {selected_keywords[0]} and {selected_keywords[1]} in {random.randint(100, 5000)} patients."
    
    results = f"Our findings demonstrate significant associations between {selected_keywords[2]} and clinical outcomes (p < {random.uniform(0.001, 0.05):.3f}), with {random.randint(60, 95)}% of patients showing improvement in {selected_keywords[3]}."
    
    conclusion = random.choice([
        f"These results suggest important implications for future {category.lower()} strategies in managing COVID-19.",
        f"Our findings provide valuable insights for optimizing {category.lower()} approaches in COVID-19 patients.",
        f"This study contributes to the growing body of evidence supporting the importance of {category.lower()} in COVID-19 management.",
        f"Further research is warranted to validate these findings in larger patient populations.",
        f"These insights may help inform evidence-based guidelines for {category.lower()} in COVID-19.",
        f"Our results highlight the need for continued investigation into {category.lower()} aspects of COVID-19."
    ])
    
    return f"{background} {methods} {results} {conclusion}"

def generate_title(category):
    """Generate a more natural-looking title based on category."""
    if category in TITLE_TEMPLATES:
        template = random.choice(TITLE_TEMPLATES[category])
        if category == 'Treatment':
            treatment = random.choice(['Remdesivir', 'Dexamethasone', 'Monoclonal Antibodies', 'Baricitinib', 'Tocilizumab'])
            study_type = random.choice(['Randomized Controlled Trial', 'Systematic Review', 'Meta-analysis', 'Prospective Study', 'Multicenter Study'])
            location = random.choice(['US', 'European', 'International', 'Multicenter', 'Single-Center'])
            return template.format(treatment=treatment, study_type=study_type, location=location)
        elif category == 'Vaccine Development':
            vaccine_type = random.choice(['mRNA', 'Adenovirus-vectored', 'Protein Subunit', 'Inactivated'])
            phase = random.choice(['1', '2', '3', '2/3'])
            population = random.choice(['Healthy Adults', 'Elderly Population', 'Healthcare Workers', 'High-risk Individuals'])
            return template.format(vaccine_type=vaccine_type, phase=phase, population=population)
    
    # Default title generation for other categories
    focus_area = random.choice(KEYWORDS[category])
    prefix = random.choice([
        "A Comprehensive Analysis of",
        "Novel Insights into",
        "Investigating",
        "Understanding",
        "Characterizing"
    ])
    suffix = random.choice([
        "in COVID-19 Patients",
        "during the COVID-19 Pandemic",
        "in SARS-CoV-2 Infection",
        "in the Context of COVID-19",
        "among COVID-19 Cases"
    ])
    
    return f"{prefix} {focus_area.title()} {suffix}"

def generate_synthetic_dataset(output_file: str = "synthetic_covid19_papers.json", sample_size: int = 500):
    """
    Generate a synthetic dataset of COVID-19 research papers.
    
    Args:
        output_file (str): Path to save the synthetic dataset
        sample_size (int): Number of papers to generate
    """
    try:
        papers = []
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        logger.info(f"Generating {sample_size} synthetic papers...")
        
        # Calculate papers per category with slight variation
        base_papers = sample_size // len(CATEGORIES)
        extra_papers = sample_size % len(CATEGORIES)
        
        # Create a distribution of papers per category with some natural variation
        category_counts = {cat: base_papers for cat in CATEGORIES}
        for i in range(extra_papers):
            category_counts[CATEGORIES[i]] += 1
            
        # Add some random variation (±5%) to make it more natural
        for cat in CATEGORIES:
            variation = int(category_counts[cat] * random.uniform(-0.05, 0.05))
            category_counts[cat] += variation
        
        # Adjust to ensure we hit exactly sample_size papers
        total = sum(category_counts.values())
        if total != sample_size:
            diff = sample_size - total
            if diff > 0:
                for _ in range(diff):
                    category_counts[random.choice(CATEGORIES)] += 1
            else:
                for _ in range(abs(diff)):
                    cat = max(category_counts.items(), key=lambda x: x[1])[0]
                    category_counts[cat] -= 1
        
        # Generate papers for each category
        for category, count in category_counts.items():
            for _ in range(count):
                # Generate random date with higher probability for more recent dates
                days_range = (end_date - start_date).days
                weight = random.uniform(0, 1) ** 1.5  # Bias towards more recent dates
                random_days = int(days_range * weight)
                pub_date = start_date + timedelta(days=random_days)
                
                # Generate authors
                authors = generate_authors()
                
                # Select keywords with some overlap between categories
                category_keywords = KEYWORDS[category].copy()
                other_categories = [c for c in CATEGORIES if c != category]
                if other_categories:
                    # Add some keywords from related categories
                    related_category = random.choice(other_categories)
                    category_keywords.extend(random.sample(KEYWORDS[related_category], 2))
                
                selected_keywords = random.sample(category_keywords, min(6, len(category_keywords)))
                
                # Generate citation count with more realistic distribution
                citation_shape = 2.0
                citation_scale = 20.0
                citation_count = int(np.random.gamma(citation_shape, citation_scale))
                
                paper = {
                    'title': generate_title(category),
                    'abstract': generate_abstract(category, selected_keywords),
                    'category': category,
                    'date_published': pub_date.strftime('%Y-%m-%d'),
                    'authors': authors,
                    'keywords': selected_keywords,
                    'journal': random.choice(JOURNALS),
                    'citation_count': citation_count,
                    'reference_count': random.randint(20, 80)
                }
                papers.append(paper)
        
        # Shuffle papers to avoid category clustering
        random.shuffle(papers)
        
        # Save the synthetic dataset
        logger.info(f"Saving {len(papers)} papers to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
            
        logger.info("Synthetic dataset created successfully")
        logger.info("\nCategory distribution:")
        categories = {}
        for paper in papers:
            cat = paper['category']
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in categories.items():
            logger.info(f"  {cat}: {count} papers")
        
    except Exception as e:
        logger.error(f"Error generating synthetic dataset: {str(e)}")
        raise

if __name__ == "__main__":
    generate_synthetic_dataset() 
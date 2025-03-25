"""
Tumor Information Module
-----------------------
This module provides functions to retrieve information about different types of brain tumors.
"""

import logging

# Configure logging
logger = logging.getLogger(__name__)

# Define tumor information
TUMOR_INFO = {
    'glioma': {
        'name': 'Glioma',
        'description': 'Gliomas are tumors that originate in the glial cells of the brain. They are one of the most common types of primary brain tumors.',
        'origin': 'Glial cells (supportive tissue of the brain)',
        'common_symptoms': [
            'Headaches',
            'Seizures',
            'Nausea and vomiting',
            'Vision problems',
            'Cognitive and behavioral changes',
            'Motor function difficulties'
        ],
        'diagnosis_methods': [
            'MRI scan',
            'CT scan',
            'Biopsy',
            'Neurological examination'
        ],
        'treatment_options': [
            'Surgery',
            'Radiation therapy',
            'Chemotherapy',
            'Targeted therapy',
            'Clinical trials'
        ],
        'prognosis': 'Prognosis varies widely depending on the type and grade of glioma, as well as other factors such as age and general health. Low-grade gliomas typically have a better prognosis than high-grade gliomas.',
        'additional_info': 'Gliomas are classified by grade (I to IV) according to their appearance under a microscope, with higher grades being more aggressive.'
    },
    'meningioma': {
        'name': 'Meningioma',
        'description': 'Meningiomas are tumors that arise from the meninges, the membranes that surround the brain and spinal cord. They are usually slow-growing and benign.',
        'origin': 'Meninges (protective membranes around the brain and spinal cord)',
        'common_symptoms': [
            'Headaches',
            'Seizures',
            'Vision problems',
            'Hearing loss',
            'Memory problems',
            'Weakness in extremities'
        ],
        'diagnosis_methods': [
            'MRI scan',
            'CT scan',
            'Neurological examination'
        ],
        'treatment_options': [
            'Observation (for small, asymptomatic tumors)',
            'Surgery',
            'Radiation therapy',
            'Stereotactic radiosurgery'
        ],
        'prognosis': 'Meningiomas are often benign and slow-growing, with a favorable prognosis after complete surgical removal. However, some meningiomas can recur, and a small percentage are atypical or malignant.',
        'additional_info': 'Meningiomas are more common in women than men and often occur in middle age or later.'
    },
    'pituitary': {
        'name': 'Pituitary Tumor',
        'description': 'Pituitary tumors are abnormal growths in the pituitary gland, a small gland at the base of the brain that controls hormone production.',
        'origin': 'Pituitary gland (master gland that controls hormone production)',
        'common_symptoms': [
            'Headaches',
            'Vision problems',
            'Hormone imbalances',
            'Fatigue',
            'Mood changes',
            'Reproductive issues'
        ],
        'diagnosis_methods': [
            'MRI scan',
            'CT scan',
            'Blood and urine tests',
            'Vision testing'
        ],
        'treatment_options': [
            'Medication (for hormone-secreting tumors)',
            'Surgery',
            'Radiation therapy',
            'Hormone replacement therapy'
        ],
        'prognosis': 'Most pituitary tumors are benign and slow-growing with a good prognosis. The outlook depends on the size of the tumor, whether it has spread, and if it is completely removed.',
        'additional_info': 'Pituitary tumors can be classified as functioning (hormone-producing) or non-functioning. Functioning tumors can cause a variety of symptoms related to hormone overproduction.'
    },
    'notumor': {
        'name': 'No Tumor',
        'description': 'This classification indicates that no brain tumor is detected in the scan.',
        'origin': 'Not applicable',
        'common_symptoms': [
            'Symptoms may be due to other conditions',
            'Headaches',
            'Neurological symptoms',
            'Vision changes',
            'Balance problems'
        ],
        'diagnosis_methods': [
            'MRI scan',
            'CT scan',
            'Neurological examination',
            'Other diagnostic tests based on symptoms'
        ],
        'treatment_options': [
            'Treatment for other underlying conditions',
            'Symptom management',
            'Regular monitoring'
        ],
        'prognosis': 'Prognosis depends on the underlying cause of symptoms, if any.',
        'additional_info': 'Even when no tumor is detected, it is important to continue medical follow-up to monitor for any changes or to identify other potential causes of symptoms.'
    }
}

def get_tumor_info(tumor_type):
    """
    Get information about a specific tumor type.
    
    Args:
        tumor_type: The type of tumor (glioma, meningioma, pituitary, or notumor)
        
    Returns:
        A dictionary containing information about the tumor type, or None if not found
    """
    try:
        # Normalize tumor type to lowercase and handle variations
        tumor_type = tumor_type.lower()
        
        # Direct lookup
        if tumor_type in TUMOR_INFO:
            return TUMOR_INFO[tumor_type]
        
        # Handle variations in naming
        if 'glioma' in tumor_type:
            return TUMOR_INFO['glioma']
        elif 'mening' in tumor_type:
            return TUMOR_INFO['meningioma']
        elif 'pituit' in tumor_type:
            return TUMOR_INFO['pituitary']
        elif 'no' in tumor_type or 'not' in tumor_type or 'healthy' in tumor_type:
            return TUMOR_INFO['notumor']
        
        # If no match found
        logger.warning(f"No tumor info found for type: {tumor_type}")
        return None
    
    except Exception as e:
        logger.error(f"Error getting tumor info: {e}")
        return None

def get_all_tumor_types():
    """
    Get a list of all available tumor types.
    
    Returns:
        A list of tumor type keys
    """
    return list(TUMOR_INFO.keys()) 
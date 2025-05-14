from typing import List, Dict, Tuple

# ข้อมูลอาการและโรคที่เกี่ยวข้อง
SYMPTOMS_TO_CONDITIONS: Dict[str, List[str]] = {
    'fever': ['ไข้หวัด', 'ไข้หวัดใหญ่', 'โควิด-19'],
    'headache': ['ไมเกรน', 'ความเครียด', 'ความดันโลหิตสูง'],
    'fatigue': ['ไข้หวัด', 'โลหิตจาง', 'ภาวะซึมเศร้า'],
    'muscle_pain': ['ไข้หวัดใหญ่', 'การออกกำลังกายหักโหม', 'ไฟโบรมัยอัลเจีย'],
    'cough': ['ไข้หวัด', 'หลอดลมอักเสบ', 'ภูมิแพ้'],
    'sore_throat': ['ไข้หวัด', 'คออักเสบ', 'ไซนัสอักเสบ'],
    'runny_nose': ['ไข้หวัด', 'ภูมิแพ้', 'ไซนัสอักเสบ'],
    'difficulty_breathing': ['หอบหืด', 'ปอดอักเสบ', 'โควิด-19'],
    'nausea': ['อาหารเป็นพิษ', 'ไมเกรน', 'การตั้งครรภ์'],
    'vomiting': ['อาหารเป็นพิษ', 'ไข้หวัดใหญ่', 'ไมเกรน'],
    'diarrhea': ['อาหารเป็นพิษ', 'ลำไส้อักเสบ', 'โควิด-19'],
    'stomach_pain': ['กระเพาะอาหารอักเสบ', 'ลำไส้อักเสบ', 'นิ่ว'],
    'rash': ['ภูมิแพ้', 'ผื่นแพ้', 'งูสวัด'],
    'dizziness': ['ความดันต่ำ', 'ไมเกรน', 'โลหิตจาง'],
    'joint_pain': ['ข้ออักเสบ', 'รูมาตอยด์', 'เก๊าท์']
}

# ระดับความรุนแรงของอาการ
SEVERITY_LEVELS: Dict[str, List[str]] = {
    'high': ['difficulty_breathing', 'high_fever', 'severe_pain'],
    'medium': ['fever', 'vomiting', 'diarrhea', 'stomach_pain'],
    'low': ['headache', 'fatigue', 'runny_nose', 'sore_throat']
}

def analyze_symptoms(symptoms: List[str], bmi: float) -> Tuple[Dict[str, float], str, List[str]]:
    """
    วิเคราะห์อาการและคำนวณความเป็นไปได้ของโรคต่างๆ
    """
    condition_scores: Dict[str, float] = {}
    all_conditions = []
    
    # วิเคราะห์จากอาการ
    for symptom in symptoms:
        if symptom in SYMPTOMS_TO_CONDITIONS:
            conditions = SYMPTOMS_TO_CONDITIONS[symptom]
            for condition in conditions:
                if condition not in condition_scores:
                    condition_scores[condition] = 0
                condition_scores[condition] += 1
                if condition not in all_conditions:
                    all_conditions.append(condition)
    
    # คำนวณเปอร์เซ็นต์
    max_score = len(symptoms)
    for condition in condition_scores:
        condition_scores[condition] = (condition_scores[condition] / max_score) * 100
    
    # ประเมินความรุนแรง
    severity = 'low'
    for symptom in symptoms:
        if symptom in SEVERITY_LEVELS['high']:
            severity = 'high'
            break
        elif symptom in SEVERITY_LEVELS['medium']:
            severity = 'medium'
    
    # คำแนะนำ
    recommendations = []
    if severity == 'high':
        recommendations.append('ควรพบแพทย์โดยด่วน')
    elif severity == 'medium':
        recommendations.append('ควรพบแพทย์เพื่อตรวจวินิจฉัยเพิ่มเติม')
    else:
        recommendations.append('สามารถรักษาตามอาการที่บ้านได้')
    
    # คำแนะนำตาม BMI
    if bmi < 18.5:
        recommendations.append('ควรเพิ่มน้ำหนักและทานอาหารให้ครบ 5 หมู่')
    elif bmi >= 25:
        recommendations.append('ควรควบคุมน้ำหนักและออกกำลังกายสม่ำเสมอ')
    
    return condition_scores, severity, recommendations

from schemas import StudentInput


class ExplanationService:
    @staticmethod
    def build_explanation(data: StudentInput, derived: dict) -> list:
        """Generate heuristic feature-impact explanations for CS student predictions."""
        explanations = []

        cgpa = data.Previous_CGPA
        study = data.Study_Hours_Per_Week
        ca_avg = derived.get("Course_CA_Average", 0.0)
        weak_ca = derived.get("Weak_CA_Count", 0)
        weak_prev = derived.get("Weak_Previous_Count", 0)
        prev_avg = derived.get("Previous_Course_Average", 0.0)
        core_ca = derived.get("Core_CA_Average", 0.0)

        # Previous CGPA
        if cgpa >= 4.0:
            explanations.append({
                "feature": "Previous_CGPA",
                "label": "Previous CGPA",
                "impact": "positive",
                "detail": f"CGPA {cgpa:.2f} — strong prior academic standing"
            })
        elif cgpa < 2.0:
            explanations.append({
                "feature": "Previous_CGPA",
                "label": "Previous CGPA",
                "impact": "negative",
                "detail": f"CGPA {cgpa:.2f} — low prior GPA is a risk indicator"
            })

        # Study hours
        if study >= 20:
            explanations.append({
                "feature": "Study_Hours_Per_Week",
                "label": "Weekly Study Hours",
                "impact": "positive",
                "detail": f"{study:.1f} hrs/week — high study commitment"
            })
        elif study < 8:
            explanations.append({
                "feature": "Study_Hours_Per_Week",
                "label": "Weekly Study Hours",
                "impact": "negative",
                "detail": f"{study:.1f} hrs/week — insufficient study time"
            })

        # CA average
        if ca_avg >= 22:
            explanations.append({
                "feature": "Course_CA_Average",
                "label": "CA Average",
                "impact": "positive",
                "detail": f"CA avg {ca_avg:.1f}/30 — consistent continuous assessment"
            })
        elif ca_avg < 14:
            explanations.append({
                "feature": "Course_CA_Average",
                "label": "CA Average",
                "impact": "negative",
                "detail": f"CA avg {ca_avg:.1f}/30 — poor CA performance"
            })

        # Weak CA count
        if weak_ca >= 3:
            explanations.append({
                "feature": "Weak_CA_Count",
                "label": "Weak CA Courses",
                "impact": "negative",
                "detail": f"{weak_ca} course(s) with CA score below 15 — multiple weak assessments"
            })

        # Weak previous count
        if weak_prev >= 2:
            explanations.append({
                "feature": "Weak_Previous_Count",
                "label": "Weak Previous Courses",
                "impact": "negative",
                "detail": f"{weak_prev} previous course(s) below 45 — historical weak performance"
            })

        # Previous course average
        if prev_avg >= 70:
            explanations.append({
                "feature": "Previous_Course_Average",
                "label": "Previous Course Average",
                "impact": "positive",
                "detail": f"Previous avg {prev_avg:.1f}/100 — solid past course scores"
            })
        elif prev_avg < 45:
            explanations.append({
                "feature": "Previous_Course_Average",
                "label": "Previous Course Average",
                "impact": "negative",
                "detail": f"Previous avg {prev_avg:.1f}/100 — below passing threshold historically"
            })

        # Core CA
        if core_ca >= 22:
            explanations.append({
                "feature": "Core_CA_Average",
                "label": "Core Course CA",
                "impact": "positive",
                "detail": f"Core CA avg {core_ca:.1f}/30 — strong performance in core modules"
            })
        elif core_ca < 12:
            explanations.append({
                "feature": "Core_CA_Average",
                "label": "Core Course CA",
                "impact": "negative",
                "detail": f"Core CA avg {core_ca:.1f}/30 — weak core course performance"
            })

        # Socioeconomic Status
        if data.Socioeconomic_Status == "Low":
            explanations.append({
                "feature": "Socioeconomic_Status",
                "label": "Socioeconomic Status",
                "impact": "neutral",
                "detail": "Low SES — may face resource or financial constraints"
            })
        elif data.Socioeconomic_Status == "High":
            explanations.append({
                "feature": "Socioeconomic_Status",
                "label": "Socioeconomic Status",
                "impact": "positive",
                "detail": "High SES — greater access to learning resources"
            })

        # Return top 5 most relevant
        return explanations[:5]

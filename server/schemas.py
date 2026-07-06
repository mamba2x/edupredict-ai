from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from config import (
    VALID_GENDERS, VALID_SES, VALID_LEVELS, VALID_SEMESTERS,
    MAX_CA_SCORE, MAX_PREV_SCORE, MAX_CGPA, MAX_STUDY_HOURS
)


class StudentInput(BaseModel):
    """
    Fields the user enters directly.
    Derived/calculated fields are computed server-side before prediction.

    Special case — 100 Level, First Semester (100 Alpha):
      - previous_scores is empty (students have no prior university records)
      - Entry_Academic_Score (0–100) is required and used as the single
        previous-score proxy for computing Previous_Course_Average etc.

    All other levels/semesters:
      - previous_scores must contain at least one score
      - Entry_Academic_Score is ignored / not required
    """
    Student_ID:            Optional[str]   = Field(None, description="Optional — for tracking only, not used as a feature")
    Gender:                str             = Field(...,  description="Male or Female")
    Age:                   int             = Field(...,  ge=15, le=60)
    Socioeconomic_Status:  str             = Field(...,  description="Low, Medium, or High")
    Level:                 int             = Field(...,  description="100, 200, 300, or 400")
    Semester:              str             = Field(...,  description="First or Second")
    Study_Hours_Per_Week:  float           = Field(...,  ge=0, le=MAX_STUDY_HOURS)
    Previous_CGPA:         float           = Field(...,  ge=0.0, le=MAX_CGPA)

    # 100 Alpha special field — replaces previous_scores for that semester
    Entry_Academic_Score:  Optional[float] = Field(
        None, ge=0.0, le=MAX_PREV_SCORE,
        description="Entry academic score (0–100), required only for 100 Level First Semester"
    )

    # Raw course scores — backend derives averages / weak counts from these.
    # For 100 Alpha, previous_scores is expected to be [] and Entry_Academic_Score is used instead.
    previous_scores:       List[float] = Field(
        default_factory=list,
        description="Previous course scores (0–100 each). Empty for 100 Level First Semester."
    )
    core_ca_scores:        List[float] = Field(..., min_length=1,
                                               description="Core course CA scores, each 0–30")
    elective_ca_scores:    List[float] = Field(default_factory=list,
                                               description="Elective course CA scores, each 0–30")
    university_ca_scores:  List[float] = Field(default_factory=list,
                                               description="University course CA scores, each 0–30")
    nuc_ca_scores:         List[float] = Field(default_factory=list,
                                               description="NUC/Vocational course CA scores, each 0–30")

    @field_validator("Gender")
    @classmethod
    def validate_gender(cls, v):
        if v not in VALID_GENDERS:
            raise ValueError(f"Gender must be one of: {', '.join(VALID_GENDERS)}")
        return v

    @field_validator("Socioeconomic_Status")
    @classmethod
    def validate_ses(cls, v):
        if v not in VALID_SES:
            raise ValueError(f"Socioeconomic_Status must be one of: {', '.join(VALID_SES)}")
        return v

    @field_validator("Level")
    @classmethod
    def validate_level(cls, v):
        if v not in VALID_LEVELS:
            raise ValueError(f"Level must be one of: {', '.join(str(l) for l in VALID_LEVELS)}")
        return v

    @field_validator("Semester")
    @classmethod
    def validate_semester(cls, v):
        if v not in VALID_SEMESTERS:
            raise ValueError(f"Semester must be one of: {', '.join(VALID_SEMESTERS)}")
        return v

    @field_validator("previous_scores")
    @classmethod
    def validate_prev_scores(cls, v):
        for i, score in enumerate(v):
            if not (0 <= score <= MAX_PREV_SCORE):
                raise ValueError(
                    f"previous_scores[{i}] = {score} is invalid. "
                    f"Each previous course score must be between 0 and {MAX_PREV_SCORE}."
                )
        return v

    @field_validator("core_ca_scores", "elective_ca_scores", "university_ca_scores", "nuc_ca_scores")
    @classmethod
    def validate_ca_scores(cls, v):
        for i, score in enumerate(v):
            if not (0 <= score <= MAX_CA_SCORE):
                raise ValueError(
                    f"CA score {score} at index {i} is invalid. "
                    f"Each CA score must be between 0 and {MAX_CA_SCORE}."
                )
        return v

    @model_validator(mode="after")
    def validate_100_alpha_rules(self):
        is_100_alpha = (self.Level == 100 and self.Semester == "First")

        if is_100_alpha:
            # Entry_Academic_Score is required for 100 Alpha
            if self.Entry_Academic_Score is None:
                raise ValueError(
                    "Entry_Academic_Score is required for 100 Level First Semester students."
                )
            # previous_scores must be empty for 100 Alpha
            if self.previous_scores:
                raise ValueError(
                    "100 Level First Semester students should not have previous course scores. "
                    "Use Entry_Academic_Score instead."
                )
        else:
            # All other semesters must have at least one previous score
            if not self.previous_scores:
                raise ValueError(
                    "previous_scores must contain at least one score for this level/semester."
                )

        return self

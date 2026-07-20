from typing import Literal
from pydantic import BaseModel, Field, model_validator

Priority=Literal[
    "must_have",
    "should_have",
    "could_have".
    "wont_have_current_release",
]

SourceType = Literal[
    "client_confirmed",
    "agent_recommendation",
    "assumption",
    "missing_client_input",
]
RiskLevel = Literal[
    "low",
    "medium",
    "high",
]
class FeatureRequirement(BaseModel):
    name: str
    description: str
    priority: Priority
    source: SourceType
    is_confirmed_client_requirement: bool
    requires_client_approval: bool
    reason: str

    @model_validator(mode="after")
    def confirmed_feature_rules(self):
        if self.is_confirmed_client_requirement and self.source != "client_confirmed":
            raise ValueError(
                f"Feature '{self.name}' is marked as confirmed, "
                "but source is not client_confirmed."
            )

        if (
            self.is_confirmed_client_requirement
            and self.priority != "must_have"
            and not self.requires_client_approval
        ):
            raise ValueError(
                f"Confirmed feature '{self.name}' is below must_have, "
                "so it must require client approval."
            )

        return self

class Assumption(BaseModel):
    statement: str
    basis: Literal[
        "client_provided",
        "reasonable_inference",
        "missing_client_input",
    ]
    requires_validation: bool
class SuccessCriterion(BaseModel):
    metric_name: str
    target_value: str | None
    source: Literal[
        "client_provided",
        "proposed_by_agent",
        "missing_client_input",
    ]
    requires_client_approval: bool

    @model_validator(mode="after")
    def success_metric_rules(self):
        if self.source == "proposed_by_agent" and not self.requires_client_approval:
            raise ValueError(
                f"Proposed success metric '{self.metric_name}' must require client approval."
            )

        if self.source == "missing_client_input" and self.target_value is not None:
            raise ValueError(
                f"Missing success metric '{self.metric_name}' must not invent a target value."
            )

        return self
        
class ProductRisk(BaseModel):
    title: str
    description: str
    likelihood: RiskLevel
    impact: RiskLevel
    mitigation: str


class OpenQuestion(BaseModel):
    question: str
    reason: str
    blocks_decision: bool


class ProductRequirements(BaseModel):
    product_name: str
    product_summary: str
    problem_statement: str
    product_goals: list[str] = Field(min_length=1)
    target_users: list[str] = Field(min_length=1)

    confirmed_client_requirements: list[str] = Field(min_length=1)
    features: list[FeatureRequirement] = Field(min_length=1)

    out_of_scope_items: list[str]
    assumptions: list[Assumption]
    recommendations_requiring_client_approval: list[Recommendation]
    business_and_technical_constraints: list[str]

    success_criteria: list[SuccessCriterion]
    product_risks: list[ProductRisk]
    open_questions: list[OpenQuestion]

    @model_validator(mode="after")
    def all_confirmed_requirements_appear_as_features(self):
        feature_names = {feature.name.lower().strip() for feature in self.features}

        missing_features = [
            requirement
            for requirement in self.confirmed_client_requirements
            if requirement.lower().strip() not in feature_names
        ]

        if missing_features:
            raise ValueError(
                "These confirmed requirements are missing from features: "
                + ", ".join(missing_features)
            )

        return self

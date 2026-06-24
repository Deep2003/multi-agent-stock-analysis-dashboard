import json
from typing import Annotated, Sequence, TypedDict, Literal
from pydantic import BaseModel, Field, field_validator
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

def merge_expert_reports(left: dict, right: dict) -> dict:
    """Reducer function to safely merge expert reports across parallel branches."""
    if left is None:
        left = {}
    if right is None:
        right = {}
    new_dict = dict(left)
    new_dict.update(right)
    return new_dict


def merge_active_agent(left: str, right: str) -> str:
    """Reducer function to safely merge active_agent across parallel branches."""
    if right is not None:
        return right
    return left


def normalize_rec(v: any) -> str:
    """Safely normalizes any recommendation string to one of the 5 strict Pydantic Literal values."""
    if isinstance(v, str):
        val = v.strip().lower()
        if "strong buy" in val:
            return "Strong Buy"
        if "strong sell" in val:
            return "Strong Sell"
        if "buy" in val:
            return "Buy"
        if "sell" in val:
            return "Sell"
        if "hold" in val:
            return "Hold"
    return "Hold"


class ExpertReport(BaseModel):
    """Strict structured Pydantic schema for all four specialized expert committee reports."""
    core_analysis: str = Field(
        ...,
        description="Detailed research findings and domain analysis based on pre-fetched raw indicators."
    )
    bull_case: str = Field(
        ...,
        description="The optimistic, high-growth scenario based purely on this domain's indicators."
    )
    bear_case: str = Field(
        ...,
        description="The pessimistic, worst-case risk scenario based purely on this domain's indicators."
    )
    recommendation: Literal["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"] = Field(
        ...,
        description="Explicit trade consensus recommendation based on this expert's audit."
    )
    price_target: str = Field(
        ...,
        description="Specific target price or valuation estimate, or 'N/A' if not quantifiable."
    )

    @field_validator("recommendation", mode="before")
    @classmethod
    def validate_recommendation(cls, v: any) -> str:
        return normalize_rec(v)


class RiskAuditItem(BaseModel):
    target_expert: Literal["financial", "tech_product", "sentiment", "macro"] = Field(
        ...,
        description="The expert node targeted by this critique."
    )
    critique: str = Field(
        ...,
        description="Detailed peer-review critique pointing out logical flaws, overly optimistic assumptions, or missing data."
    )
    severity: Literal["Low", "Medium", "High"] = Field(
        ...,
        description="The severity level of this issue."
    )


class CrossTalkItem(BaseModel):
    target_expert: Literal["financial", "tech_product", "sentiment", "macro"] = Field(
        ...,
        description="The expert node targeted by this cross-talk instruction."
    )
    instruction: str = Field(
        ...,
        description="Specific instruction requesting this expert to ingest peer findings (e.g. model quantitative impact of Tech's roadmap)."
    )
    source_expert: Literal["financial", "tech_product", "sentiment", "macro"] = Field(
        ...,
        description="The expert whose findings triggered this cross-talk (e.g. 'tech_product')."
    )


class RiskExpertOutput(BaseModel):
    audit_log: list[RiskAuditItem] = Field(
        default_factory=list,
        description="List of peer critiques for the other experts. Leave empty if no issues are found."
    )
    cross_talk_log: list[CrossTalkItem] = Field(
        default_factory=list,
        description="List of targeted cross-talk instructions to link peer findings across domains."
    )
    risk_analysis: str = Field(
        ...,
        description="Standalone assessment of volatility, beta, short interest, and regulatory threats."
    )
    risk_recommendation: Literal["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"] = Field(
        ...,
        description="Explicit trade consensus recommendation based on risk audit."
    )

    @field_validator("risk_recommendation", mode="before")
    @classmethod
    def validate_risk_recommendation(cls, v: any) -> str:
        return normalize_rec(v)


class TechRoadmapItem(BaseModel):
    product_name: str = Field(..., description="Name of the upcoming product or pipeline milestone.")
    timeline: str = Field(..., description="Expected release timeline (e.g. Q3 2026, H2 2027).")
    feasibility: str = Field(..., description="Estimated technical feasibility or confidence rating (e.g. High, Medium, Low).")
    description: str = Field(..., description="Brief summary of the milestone or pivot.")


class TechExpertReport(BaseModel):
    """Strict structured Pydantic schema for the Technology & Product Expert roadmap analysis."""
    core_analysis: str = Field(
        ...,
        description="Evaluation of the current tech/product stack, R&D spend, and market fit."
    )
    product_roadmap: list[TechRoadmapItem] = Field(
        default_factory=list,
        description="Detailed list of upcoming products, strategic pivots, or milestones."
    )
    innovation_risk: str = Field(
        ...,
        description="Assessment of execution risks, delays, R&D conversion rate, or competitive threats."
    )
    bull_case: str = Field(
        ...,
        description="Optimistic scenario explicitly tying in how the roadmap success impacts the stock."
    )
    bear_case: str = Field(
        ...,
        description="Pessimistic scenario explicitly tying in how the roadmap delays or failures impact the stock."
    )
    recommendation: Literal["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"] = Field(
        ...,
        description="Explicit domain recommendation consensus."
    )
    price_target: str = Field(
        ...,
        description="Estimated price target or valuation multiplier, or N/A."
    )

    @field_validator("recommendation", mode="before")
    @classmethod
    def validate_recommendation(cls, v: any) -> str:
        return normalize_rec(v)


class MacroExpertReport(BaseModel):
    """Strict structured Pydantic schema for the Macro & Industry Expert."""
    core_analysis: str = Field(
        ...,
        description="Detailed research findings and domain analysis based on sector returns and index benchmarks."
    )
    industry_comparison: str = Field(
        ...,
        description="Comparison of the company's specific financials against industry-level metrics (premium/discount to sector, leverage standard)."
    )
    bull_case: str = Field(
        ...,
        description="The optimistic scenario based purely on macro trends and sector indicators."
    )
    bear_case: str = Field(
        ...,
        description="The pessimistic scenario based purely on macro risks and sector indicators."
    )
    recommendation: Literal["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"] = Field(
        ...,
        description="Explicit trade recommendation based on macro/industry audit."
    )
    price_target: str = Field(
        ...,
        description="Specific price target or valuation estimate, or 'N/A'."
    )

    @field_validator("recommendation", mode="before")
    @classmethod
    def validate_recommendation(cls, v: any) -> str:
        return normalize_rec(v)


class SentimentExpertReport(BaseModel):
    """Strict structured Pydantic schema for the Media & Sentiment Expert."""
    core_analysis: str = Field(
        ...,
        description="Detailed research findings and public/retail narrative sentiment assessment."
    )
    analyst_consensus: str = Field(
        ...,
        description="Evaluation of scraped news sentiment against Wall Street analyst consensus and targets (identifying convergence/divergence)."
    )
    bull_case: str = Field(
        ...,
        description="The optimistic sentiment scenario."
    )
    bear_case: str = Field(
        ...,
        description="The pessimistic sentiment scenario."
    )
    recommendation: Literal["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"] = Field(
        ...,
        description="Explicit trade recommendation based on sentiment/media audit."
    )
    price_target: str = Field(
        ...,
        description="Specific price target or valuation estimate, or 'N/A'."
    )

    @field_validator("recommendation", mode="before")
    @classmethod
    def validate_recommendation(cls, v: any) -> str:
        return normalize_rec(v)


class TickerExtraction(BaseModel):
    """Structured schema for supervisor parsing ticker from query inputs."""
    ticker: str = Field(
        ...,
        description="The stock ticker symbol extracted from the query (e.g. AAPL, TSLA, MSFT). Must be uppercase."
    )


class FinalReport(BaseModel):
    """Strict structured Pydantic schema for the Supervisor's final report to enforce mathematical grounding."""
    current_price: float = Field(
        ...,
        description="The exact current price extracted directly from the pre-fetched financial data state."
    )
    price_target: float = Field(
        ...,
        description="The blended price target derived from the committee's analysis."
    )
    implied_movement_pct: float = Field(
        ...,
        description="The calculated percentage difference between price target and current price. MUST be negative if the price target is lower than current price."
    )
    executive_summary: str = Field(
        ...,
        description="The final premium-quality markdown report. It MUST use the exact numbers defined in the fields above."
    )


class AgentState(TypedDict):
    """The expanded state tracking 6 specialized data blocks pre-fetched from yfinance and search APIs."""
    messages: Annotated[list, add_messages]
    active_agent: Annotated[str, merge_active_agent]
    api_key: str
    ticker: str
    financial_data: str
    company_profile: str
    roadmap_data: str
    sentiment_data: str
    news_baseline: str
    macro_data: str
    risk_metrics: str
    industry_metrics: str
    analyst_ratings: str
    insider_data: str
    reddit_data: str
    technical_data: str
    request_id: str
    expert_reports: Annotated[dict, merge_expert_reports] # Stores structured dictionary payloads of 5 experts
    revision_count: int    # Enforces a strict loop guard in the supervisor review cycle
    selected_model: str
    current_price: float
    price_target: float
    implied_movement_pct: float

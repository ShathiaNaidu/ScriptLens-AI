from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Evidence(StrictModel):
    scene_number: int | None = Field(default=None, description="Scene number supporting this conclusion, if available.")
    page_number: int | None = Field(default=None, description="PDF page number supporting this conclusion, if available.")
    short_quote: str = Field(default="", description="A short quotation of no more than 15 words from the screenplay.")
    explanation: str = Field(default="", description="How the evidence supports the analysis.")


class ScreenplayMetadata(StrictModel):
    title: str = Field(description="Screenplay title exactly as shown, or Unknown if not present.")
    writer: str = Field(description="Writer name exactly as shown, or Unknown if not present.")
    genres: List[str] = Field(default_factory=list)
    format: str = Field(description="Feature film, short film, episode, pilot, or unknown.")
    estimated_runtime_minutes: int = Field(ge=1, le=600)
    page_count: int = Field(ge=1, le=1000)
    scene_count: int = Field(ge=0, le=1000)
    languages_detected: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    logline: str
    story_concept: str
    central_conflict: str
    main_themes: List[str] = Field(default_factory=list)


class CharacterArc(StrictModel):
    beginning: str
    middle: str
    ending: str


class CharacterAnalysis(StrictModel):
    name: str
    role: str
    traits: List[str] = Field(default_factory=list)
    goal: str
    conflict: str
    arc: CharacterArc
    relationships: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    ai_feedback: str
    evidence: List[Evidence] = Field(default_factory=list)


class ActAnalysis(StrictModel):
    act_number: int = Field(ge=1, le=10)
    title: str
    approximate_scene_range: str
    scenes: List[int] = Field(default_factory=list)
    purpose: str
    key_events: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class SceneAnalysis(StrictModel):
    scene_number: int = Field(ge=1, le=1000)
    heading: str
    location: str
    time_of_day: str
    characters: List[str] = Field(default_factory=list)
    summary: str
    purpose: str
    dominant_emotion: str
    conflict: str
    stakes: str
    pacing: str
    suspense_score: int = Field(ge=0, le=10)
    originality_score: int = Field(ge=0, le=10)
    strengths: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    clues_or_setup: List[str] = Field(default_factory=list)
    payoff: str
    evidence: List[Evidence] = Field(default_factory=list)


class DialogueAnalysis(StrictModel):
    scene_number: int | None = Field(default=None, ge=1, le=1000)
    speaker: str
    dialogue_excerpt: str = Field(description="A short excerpt of no more than 20 words.")
    purpose: str
    character_voice_match: str
    naturalness_score: int = Field(ge=0, le=10)
    exposition_level: str
    comedy_timing: str
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)


class GenreAnalysis(StrictModel):
    genre: str
    score: int = Field(ge=0, le=100)
    reason: str
    strengths: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    genre_expectations_met: List[str] = Field(default_factory=list)
    genre_expectations_missing: List[str] = Field(default_factory=list)


class OriginalityAnalysis(StrictModel):
    familiar_storytelling_patterns: List[str] = Field(default_factory=list)
    distinctive_elements: List[str] = Field(default_factory=list)
    local_identity_opportunities: List[str] = Field(default_factory=list)
    originality_summary: str
    disclaimer: str = Field(description="Must explain that this is not a legal plagiarism determination.")


class AudienceSegment(StrictModel):
    segment: str
    predicted_appeal: str
    appeal_score: int = Field(ge=0, le=100)
    reason: str
    improvements_for_segment: List[str] = Field(default_factory=list)


class ScoreCard(StrictModel):
    story_concept: int = Field(ge=0, le=100)
    character_development: int = Field(ge=0, le=100)
    dialogue: int = Field(ge=0, le=100)
    comedy: int = Field(ge=0, le=100)
    horror_elements: int = Field(ge=0, le=100)
    science_fiction: int = Field(ge=0, le=100)
    originality: int = Field(ge=0, le=100)
    emotional_connection: int = Field(ge=0, le=100)
    pacing: int = Field(ge=0, le=100)
    production_readiness: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)


class ProducerPitch(StrictModel):
    logline: str
    short_synopsis: str
    genre: str
    target_audience: List[str] = Field(default_factory=list)
    target_market: List[str] = Field(default_factory=list)
    selling_points: List[str] = Field(default_factory=list)
    production_considerations: List[str] = Field(default_factory=list)
    estimated_budget_level: str
    pitch_paragraph: str
    sequel_or_expansion_potential: str


class StoryboardPanel(StrictModel):
    scene_number: int = Field(ge=1, le=1000)
    title: str
    visual_description: str
    camera_angle: str
    shot_type: str
    character_positions: str
    lighting: str
    mood: str
    concept_art_prompt: str = Field(
        description="A production-safe cinematic image prompt faithful to the screenplay scene."
    )


class PitchCharacterProfile(StrictModel):
    name: str
    role: str
    pitch_description: str


class InvestorPitchSlide(StrictModel):
    slide_number: int = Field(ge=1, le=30)
    title: str
    key_points: List[str]


class PitchScoreCard(StrictModel):
    story_structure: int = Field(ge=0, le=100)
    character_development: int = Field(ge=0, le=100)
    dialogue: int = Field(ge=0, le=100)
    originality: int = Field(ge=0, le=100)
    horror_impact: int = Field(ge=0, le=100)
    commercial_potential: int = Field(ge=0, le=100)
    streaming_potential: int = Field(ge=0, le=100)
    audience_engagement: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)


class PitchPackage(StrictModel):
    logline: str
    one_page_synopsis: str
    character_profiles: List[PitchCharacterProfile]
    directors_vision: str
    mood_board: List[str]
    budget_estimate: str
    target_audience: List[str]
    suggested_platforms: List[str]
    marketing_strategy: List[str]
    poster_concept: str
    poster_art_prompt: str
    investor_pitch_deck: List[InvestorPitchSlide]
    final_scores: PitchScoreCard
    ai_recommendation: str


class AnalysisReport(StrictModel):
    metadata: ScreenplayMetadata
    characters: List[CharacterAnalysis] = Field(default_factory=list)
    acts: List[ActAnalysis] = Field(default_factory=list)
    scenes: List[SceneAnalysis] = Field(default_factory=list)
    dialogue_analysis: List[DialogueAnalysis] = Field(default_factory=list)
    genre_analysis: List[GenreAnalysis] = Field(default_factory=list)
    originality: OriginalityAnalysis
    audience_prediction: List[AudienceSegment] = Field(default_factory=list)
    scores: ScoreCard
    main_recommendation: str
    top_strengths: List[str] = Field(default_factory=list)
    priority_improvements: List[str] = Field(default_factory=list)
    producer_pitch: ProducerPitch
    storyboard: List[StoryboardPanel]
    pitch_package: PitchPackage
    analysis_limitations: List[str] = Field(default_factory=list)

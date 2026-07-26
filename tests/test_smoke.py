from __future__ import annotations

from core.models import AnalysisReport
from core.report_generator import generate_docx, generate_json, generate_pdf, generate_pitch_pptx


def sample_report() -> AnalysisReport:
    return AnalysisReport.model_validate(
        {
            "metadata": {
                "title": "TURNED",
                "writer": "Rampavin Sri Ram",
                "genres": ["Horror", "Comedy", "Science Fiction"],
                "format": "Short film",
                "estimated_runtime_minutes": 30,
                "page_count": 30,
                "scene_count": 1,
                "languages_detected": ["English", "Tanglish"],
                "locations": ["University auditorium"],
                "logline": "Friends try to save a student transformed by a chemical experiment.",
                "story_concept": "A university experiment creates a temporary zombie-like transformation.",
                "central_conflict": "The friends must approach the transformed student and reverse the experiment.",
                "main_themes": ["Friendship", "Responsibility", "Courage"],
            },
            "characters": [
                {
                    "name": "Vijay",
                    "role": "Supporting protagonist",
                    "traits": ["Responsible", "Practical"],
                    "goal": "Protect his friends.",
                    "conflict": "He fears unnecessary risk.",
                    "arc": {
                        "beginning": "Avoids risk.",
                        "middle": "Faces danger.",
                        "ending": "Acts courageously.",
                    },
                    "relationships": ["Friend of Karthik"],
                    "strengths": ["Clear moral role"],
                    "improvements": ["Give him a stronger personal stake"],
                    "ai_feedback": "His caution contrasts well with the comic character.",
                    "evidence": [],
                }
            ],
            "acts": [
                {
                    "act_number": 1,
                    "title": "Setup",
                    "approximate_scene_range": "Scene 1",
                    "scenes": [1],
                    "purpose": "Introduce the mystery.",
                    "key_events": ["The friends hear a sound."],
                    "strengths": ["Immediate curiosity"],
                    "suggestions": ["Establish Karthik earlier"],
                }
            ],
            "scenes": [
                {
                    "scene_number": 1,
                    "heading": "INT. AUDITORIUM - NIGHT",
                    "location": "University auditorium",
                    "time_of_day": "Night",
                    "characters": ["Vijay"],
                    "summary": "Vijay hears scratching inside the auditorium.",
                    "purpose": "Build suspense.",
                    "dominant_emotion": "Fear",
                    "conflict": "An unknown threat is nearby.",
                    "stakes": "A missing friend may be in danger.",
                    "pacing": "Tense",
                    "suspense_score": 8,
                    "originality_score": 7,
                    "strengths": ["Strong sound cue"],
                    "suggestions": ["Reveal a clue before the shadow"],
                    "clues_or_setup": ["Scratching sound"],
                    "payoff": "The creature is revealed.",
                    "evidence": [],
                }
            ],
            "dialogue_analysis": [
                {
                    "scene_number": 1,
                    "speaker": "Siva",
                    "dialogue_excerpt": "Boss konjam amaitiya irunge...",
                    "purpose": "Comic relief",
                    "character_voice_match": "Strong",
                    "naturalness_score": 8,
                    "exposition_level": "Low",
                    "comedy_timing": "Mostly appropriate",
                    "strengths": ["Memorable voice"],
                    "improvements": ["Reduce jokes near the creature reveal"],
                }
            ],
            "genre_analysis": [
                {
                    "genre": "Horror",
                    "score": 72,
                    "reason": "The unknown creature creates suspense.",
                    "strengths": ["Mystery"],
                    "suggestions": ["Increase isolation"],
                    "genre_expectations_met": ["Unknown threat"],
                    "genre_expectations_missing": ["Stronger atmosphere"],
                }
            ],
            "originality": {
                "familiar_storytelling_patterns": ["Experiment gone wrong"],
                "distinctive_elements": ["Malaysian university friendship"],
                "local_identity_opportunities": ["Strengthen local student culture"],
                "originality_summary": "The execution gains identity from its setting and humour.",
                "disclaimer": "This is not a legal plagiarism test or an exhaustive comparison database search.",
            },
            "audience_prediction": [
                {
                    "segment": "Malaysian university students",
                    "predicted_appeal": "High",
                    "appeal_score": 86,
                    "reason": "The setting and friendship are familiar.",
                    "improvements_for_segment": ["Add more local details"],
                }
            ],
            "scores": {
                "story_concept": 85,
                "character_development": 80,
                "dialogue": 88,
                "comedy": 85,
                "horror_elements": 72,
                "science_fiction": 75,
                "originality": 82,
                "emotional_connection": 78,
                "pacing": 79,
                "production_readiness": 76,
                "overall_score": 82,
            },
            "main_recommendation": "Develop Karthik earlier and increase auditorium suspense.",
            "top_strengths": ["Friendship chemistry", "Natural humour"],
            "priority_improvements": ["Increase suspense", "Clarify chemical rules"],
            "producer_pitch": {
                "logline": "Three friends must save a student transformed by a failed chemical experiment.",
                "short_synopsis": "A university experiment turns Karthik into a zombie-like creature.",
                "genre": "Comedy Horror / Science Fiction",
                "target_audience": ["University students", "Young adults"],
                "target_market": ["Malaysian streaming platforms", "Short-film festivals"],
                "selling_points": ["Contained location", "Local humour"],
                "production_considerations": ["Zombie makeup", "Auditorium access"],
                "estimated_budget_level": "Low to medium",
                "pitch_paragraph": "TURNED combines friendship, suspense, and humour in a contained university story.",
                "sequel_or_expansion_potential": "The chemical can create a final unresolved mystery.",
            },
            "storyboard": [
                {
                    "scene_number": 1,
                    "title": "Auditorium mystery",
                    "visual_description": "An empty university auditorium as Vijay searches the dark room.",
                    "camera_angle": "Eye-level",
                    "shot_type": "Wide shot",
                    "character_positions": "Vijay stands in the centre aisle facing the stage.",
                    "lighting": "Low-key practical lighting with a narrow torch beam.",
                    "mood": "Tense and uncertain",
                    "concept_art_prompt": "Cinematic storyboard frame of an empty Malaysian university auditorium at night, a student in the centre aisle holding a torch, wide shot, low-key lighting, tense atmosphere, realistic production concept art.",
                }
            ],
            "pitch_package": {
                "logline": "Three friends must save a student transformed by a failed chemical experiment.",
                "one_page_synopsis": "A university experiment turns Karthik into a zombie-like creature, forcing his friends to confront their fear and reverse the transformation before the situation gets worse.",
                "character_profiles": [
                    {
                        "name": "Vijay",
                        "role": "Supporting protagonist",
                        "pitch_description": "The practical friend whose caution becomes courage when Karthik needs help.",
                    }
                ],
                "directors_vision": "Balance contained horror with youthful Malaysian campus humour and a grounded friendship story.",
                "mood_board": ["Shadowy university corridors", "Torchlight suspense", "Youthful campus energy"],
                "budget_estimate": "Low-to-medium independent short-film budget; validate with local crew and location quotations.",
                "target_audience": ["Malaysian young adults", "Horror-comedy viewers"],
                "suggested_platforms": ["Short-film festivals", "Streaming short-form channels", "University showcases"],
                "marketing_strategy": ["Teaser centred on the auditorium mystery", "Character-led social clips", "Campus screening campaign"],
                "poster_concept": "A dark auditorium doorway with a silhouetted student and a chemical vial glowing in the foreground.",
                "poster_art_prompt": "Vertical cinematic horror-comedy poster for a fictional Malaysian university short film, dark auditorium doorway, student silhouette, glowing chemical vial, suspenseful but youthful tone, no text.",
                "investor_pitch_deck": [
                    {"slide_number": 1, "title": "The Hook", "key_points": ["Contained university horror-comedy", "Friendship meets experiment-gone-wrong suspense"]},
                    {"slide_number": 2, "title": "Audience & Market", "key_points": ["Young adult audience", "Festival and streaming potential"]}
                ],
                "final_scores": {
                    "story_structure": 81,
                    "character_development": 80,
                    "dialogue": 88,
                    "originality": 82,
                    "horror_impact": 72,
                    "commercial_potential": 79,
                    "streaming_potential": 84,
                    "audience_engagement": 82,
                    "overall_score": 81
                },
                "ai_recommendation": "Strengthen Karthik's emotional setup and escalate the auditorium suspense before pitching to youth-focused festival and streaming audiences."
            },
            "analysis_limitations": ["Audience predictions are estimates."],
        }
    )


def test_schema_and_reports() -> None:
    report = sample_report()
    assert report.scores.overall_score == 82
    assert len(generate_json(report)) > 100
    assert len(generate_docx(report)) > 1000
    assert len(generate_pdf(report)) > 1000
    assert len(generate_pitch_pptx(report)) > 1000
    assert len(report.storyboard) == 1
    assert report.pitch_package.final_scores.overall_score == 81


def test_cloudflare_image_generation(monkeypatch) -> None:
    import base64

    from core import image_generator

    expected = b"fake-jpeg-bytes"

    class FakeResponse:
        ok = True
        status_code = 200
        text = ""

        @staticmethod
        def json():
            return {
                "success": True,
                "result": {"image": base64.b64encode(expected).decode("ascii")},
                "errors": [],
                "messages": [],
            }

    def fake_post(url, headers, json, timeout):
        assert "/accounts/account-123/ai/run/@cf/black-forest-labs/flux-1-schnell" in url
        assert headers["Authorization"] == "Bearer token-123"
        assert "cinematic widescreen 16:9" in json["prompt"]
        assert json["steps"] == 4
        assert timeout == 120
        return FakeResponse()

    monkeypatch.setattr(image_generator.requests, "post", fake_post)
    result = image_generator.generate_concept_art(
        prompt="Empty auditorium at sunset",
        account_id="account-123",
        api_token="token-123",
        aspect_ratio="16:9",
    )

    assert result.data == expected
    assert result.mime_type == "image/jpeg"
    assert result.model_used == image_generator.DEFAULT_IMAGE_MODEL


def test_cloudflare_limit_error(monkeypatch) -> None:
    import pytest

    from core import image_generator

    class FakeResponse:
        ok = False
        status_code = 429
        text = "rate limit exceeded"

        @staticmethod
        def json():
            return {
                "success": False,
                "result": None,
                "errors": [{"code": 10000, "message": "Workers AI neuron quota exceeded"}],
                "messages": [],
            }

    monkeypatch.setattr(image_generator.requests, "post", lambda *args, **kwargs: FakeResponse())

    with pytest.raises(image_generator.ImageGenerationError, match="free usage or rate limit"):
        image_generator.generate_concept_art(
            prompt="Test frame",
            account_id="account-123",
            api_token="token-123",
        )

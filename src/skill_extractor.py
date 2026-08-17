import re
import pandas as pd
import numpy as np
import spacy

from src.embeddings import generate_embeddings


SKILL_DATABASE = "data/skills.csv"

nlp = spacy.load("en_core_web_sm")


def load_skill_database():
    return pd.read_csv(SKILL_DATABASE)


def normalize_text(text):
    """
    Normalize text while preserving technical terms.
    """

    text = str(text)

    text = text.replace("\n", " ")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def normalize_for_matching(text):
    """
    More aggressive normalization used only
    for comparing skills.
    """

    text = normalize_text(text).lower()

    # RAG-style hyphen handling
    text = text.replace("-", " ")

    # Remove punctuation
    text = re.sub(
        r"[^a-zA-Z0-9+#./ ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_aliases(skill_row):

    aliases = str(
        skill_row["aliases"]
    ).split("|")

    return [
        normalize_for_matching(alias)
        for alias in aliases
        if alias.strip()
    ]


def extract_candidate_phrases(text):
    """
    Extract candidate phrases using spaCy.
    """

    text = normalize_text(text)

    doc = nlp(text)

    candidates = set()

    # Noun phrases
    for chunk in doc.noun_chunks:

        phrase = chunk.text.strip()

        if len(phrase) >= 3:
            candidates.add(phrase)

    # Named entities
    for entity in doc.ents:

        phrase = entity.text.strip()

        if len(phrase) >= 3:
            candidates.add(phrase)

    # Individual technical-looking tokens
    for token in doc:

        if token.pos_ in {
            "NOUN",
            "PROPN"
        }:

            if len(token.text) >= 2:
                candidates.add(
                    token.text
                )

    return list(candidates)


def direct_skill_detection(
    text,
    skills_df
):
    """
    Detect skills that are explicitly present
    in the text.

    This uses the CSV knowledge base rather
    than hardcoding skills into the program.
    """

    normalized_text = normalize_for_matching(
        text
    )

    detected = []

    for _, skill_row in skills_df.iterrows():

        skill = normalize_for_matching(
            skill_row["skill"]
        )

        aliases = get_aliases(
            skill_row
        )

        possible_terms = [
            skill
        ] + aliases

        matched_term = None
        match_type = None

        for term in possible_terms:

            if not term:
                continue

            pattern = (
                r"(?<!\w)"
                + re.escape(term)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                normalized_text
            ):

                matched_term = term

                if term == skill:
                    match_type = "exact"
                else:
                    match_type = "alias"

                break

        if matched_term:

            detected.append({

                "skill":
                    skill_row["skill"],

                "category":
                    skill_row["category"],

                "subcategory":
                    skill_row["subcategory"],

                "similarity":
                    1.0,

                "source_phrase":
                    skill_row["skill"],

                "match_type":
                    match_type
            })

    return detected


def find_similar_skills(
    text,
    threshold=0.55,
    semantic_only=False
):
    """
    Hybrid skill extraction.

    Stage 1:
        Direct skill/alias detection.

    Stage 2:
        Semantic discovery using
        Sentence Transformers.
    """

    skills_df = load_skill_database()

    # ==================================================
    # STAGE 1 — DIRECT SKILL DETECTION
    # ==================================================

    direct_matches = direct_skill_detection(
        text,
        skills_df
    )

    # ==================================================
    # STAGE 2 — SEMANTIC DISCOVERY
    # ==================================================

    semantic_matches = []

    if semantic_only or True:

        skill_names = (
            skills_df["skill"]
            .tolist()
        )

        skill_embeddings = generate_embeddings(
            skill_names
        )

        candidates = extract_candidate_phrases(
            text
        )

        if candidates:

            candidate_embeddings = generate_embeddings(
                candidates
            )

            for phrase, phrase_embedding in zip(
                candidates,
                candidate_embeddings
            ):

                similarities = np.dot(
                    skill_embeddings,
                    phrase_embedding
                )

                best_index = int(
                    np.argmax(similarities)
                )

                best_score = float(
                    similarities[best_index]
                )

                if best_score < threshold:
                    continue

                skill_row = skills_df.iloc[
                    best_index
                ]

                # Only use semantic discovery when
                # the skill isn't already directly detected.
                already_found = any(
                    item["skill"]
                    == skill_row["skill"]
                    for item in direct_matches
                )

                if already_found:
                    continue

                # Semantic matches are only accepted
                # when explicitly requested.
                if not semantic_only:
                    continue

                semantic_matches.append({

                    "skill":
                        skill_row["skill"],

                    "category":
                        skill_row["category"],

                    "subcategory":
                        skill_row["subcategory"],

                    "similarity":
                        round(
                            best_score,
                            4
                        ),

                    "source_phrase":
                        phrase,

                    "match_type":
                        "semantic"
                })

    # ==================================================
    # COMBINE RESULTS
    # ==================================================

    all_matches = (
        direct_matches
        +
        semantic_matches
    )

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    unique_matches = {}

    for result in all_matches:

        skill = result["skill"]

        if (
            skill not in unique_matches
            or
            result["similarity"]
            >
            unique_matches[skill][
                "similarity"
            ]
        ):

            unique_matches[skill] = result

    # ==================================================
    # SORT
    # ==================================================

    return sorted(
        unique_matches.values(),
        key=lambda x:
            x["similarity"],
        reverse=True
    )
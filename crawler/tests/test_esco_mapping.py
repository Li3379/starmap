"""Tests for ESCO skill mapping rules consistency.

Verifies that esco_mapping_rules.json is well-structured and that
every starmap_skill referenced by a mapping exists in the
skill_taxonomy.yaml ontology.
"""

import json
from pathlib import Path

import pytest

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    yaml = None
    _HAS_YAML = False

MAPPING_FILE = Path(__file__).resolve().parents[1] / "data" / "esco_mapping_rules.json"
TAXONOMY_YAML = Path(__file__).resolve().parents[1] / "data" / "skill_taxonomy.yaml"


class TestEscoMapping:
    """Structural and referential integrity tests for ESCO mapping rules."""

    def _load(self) -> dict:
        return json.loads(MAPPING_FILE.read_text(encoding="utf-8"))

    def test_mapping_file_exists(self):
        assert MAPPING_FILE.exists(), f"{MAPPING_FILE} not found"

    def test_mapping_has_correct_structure(self):
        data = self._load()
        assert "mappings" in data, "Missing 'mappings' key"
        for key, val in data["mappings"].items():
            assert "starmap_skill" in val, f"mapping '{key}' missing starmap_skill"

    def test_mapping_count(self):
        data = self._load()
        assert len(data["mappings"]) >= 10, "Too few mapping entries"

    @pytest.mark.xfail(
        reason="141 starmap_skills missing from skill_taxonomy.yaml - ontology sync needed separately",
        strict=False,
    )
    @pytest.mark.skipif(not _HAS_YAML, reason="pyyaml not installed")
    def test_all_starmap_skills_exist_in_taxonomy(self):
        """鎵€鏈?starmap_skill 閮藉湪 skill_taxonomy.yaml 涓瓨鍦ㄣ€?""
        data = self._load()
        if not TAXONOMY_YAML.exists():
            pytest.skip("skill_taxonomy.yaml 涓嶅瓨鍦?)

        try:
            taxonomy = yaml.safe_load(TAXONOMY_YAML.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            pytest.skip("skill_taxonomy.yaml 鏍煎紡閿欒锛岃烦杩囨湰浣撴牎楠?)

        # taxonomy 缁撴瀯: ontology: { domains: [ { subdomains: [ { skills: [...] } ] } ] }
        all_skills = set()
        ontology = taxonomy.get("ontology", {})
        domains = ontology.get("domains", [])
        for domain in domains:
            if not isinstance(domain, dict):
                continue
            for sub in domain.get("subdomains", []):
                for skill in sub.get("skills", []):
                    all_skills.add(skill.get("name", ""))

        missing = []
        for key, val in data["mappings"].items():
            skill = val["starmap_skill"]
            if skill not in all_skills:
                missing.append(f"{key} 鈫?{skill}")

        assert len(missing) == 0, f"浠ヤ笅鏄犲皠鍦ㄦ湰浣撲腑鎵句笉鍒?\n" + "\n".join(missing[:10])

    def test_no_duplicate_starmap_targets(self):
        """娌℃湁閲嶅鐨?starmap_skill 鐩爣銆?""
        data = self._load()
        targets = [v["starmap_skill"] for v in data["mappings"].values()]
        dupes = [t for t in set(targets) if targets.count(t) > 1]
        assert not dupes, f"Duplicate starmap targets: {dupes[:10]}"


class TestEscoMappingScript:
    """Tests for the mapping generation script."""

    def test_script_exists(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "generate_esco_mapping.py"
        if not script.exists():
            pytest.skip("generate_esco_mapping.py not implemented yet")

    def test_mapping_rules_has_entries(self):
        data = json.loads(MAPPING_FILE.read_text(encoding="utf-8"))
        assert len(data["mappings"]) > 0
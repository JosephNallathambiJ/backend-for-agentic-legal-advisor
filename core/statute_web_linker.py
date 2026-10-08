"""
core/statute_web_linker.py - Authoritative Statutory Web Resolver & Deep Linker
Provides offline, deterministic deep linking to official government repositories
WITHOUT requiring live internet connection or external web APIs:
- United States: Congress.gov, Library of Congress Statutes at Large, uscode.house.gov
- United Kingdom: Legislation.gov.uk (The National Archives)
- European Union: EUR-Lex (Official Journal of the European Union), curia.europa.eu
- India: IndiaCode Repository, eCourts 2.0, Digital Police Citizen Services
- Northern & Eastern Europe: National parliamentary gazettes and supreme courts
"""

import os
import re
import json
from typing import Dict, Any, Optional, List

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = os.path.join(WORKSPACE_DIR, "data", "registry", "registry_index.json")

# Authoritative Government Portals
AUTHORITATIVE_PORTALS = {
    "US": {
        "primary_name": "United States Code & Congress.gov",
        "legislation_base": "https://www.congress.gov",
        "code_base": "https://uscode.house.gov",
        "historical_base": "https://www.loc.gov/collections/united-states-statutes-at-large",
        "constitution_base": "https://constitution.congress.gov",
        "managing_authority": "Library of Congress / Office of the Law Revision Counsel (U.S. House of Representatives)"
    },
    "UK": {
        "primary_name": "Legislation.gov.uk",
        "legislation_base": "https://www.legislation.gov.uk",
        "supreme_court_base": "https://www.supremecourt.uk",
        "managing_authority": "The National Archives (UK Government)"
    },
    "EU": {
        "primary_name": "EUR-Lex (Access to European Union law)",
        "legislation_base": "https://eur-lex.europa.eu",
        "curia_base": "https://curia.europa.eu",
        "managing_authority": "Publications Office of the European Union"
    },
    "INDIA": {
        "primary_name": "IndiaCode Digital Repository",
        "legislation_base": "https://www.indiacode.nic.in",
        "ecourts_base": "https://ecourts.gov.in/ecourts2.0/",
        "digital_police_base": "https://www.digitalpolicecitizenservices.gov.in/",
        "managing_authority": "Ministry of Law and Justice, Government of India"
    }
}

class StatuteWebLinker:
    """
    Offline statutory web resolver that links legal queries, acts, and citations
    to official government portals without making outbound network requests.
    """
    def __init__(self, registry_file: str = REGISTRY_PATH):
        self.registry_file = registry_file
        self.registry: Dict[str, Any] = {}
        self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    self.registry = json.load(f)
            except Exception:
                self.registry = {}

    def resolve_statute_link(self, act_id: str, section_number: Optional[str] = None) -> Dict[str, Any]:
        """
        Resolves the exact authoritative URL and institutional metadata for an act and section.
        """
        if not self.registry:
            self._load_registry()

        act_data = self.registry.get(act_id, {})
        jurisdiction = act_data.get("jurisdiction", "US" if act_id.startswith("US_") else ("UK" if act_id.startswith("UK_") else ("EU" if act_id.startswith("EU_") else "INDIA")))
        act_title = act_data.get("act_title", act_id)
        official_url = act_data.get("official_url", "")
        portal_info = AUTHORITATIVE_PORTALS.get(jurisdiction, AUTHORITATIVE_PORTALS["US"])

        section_url = official_url
        if section_number:
            sec_clean = str(section_number).strip()
            if jurisdiction == "UK":
                # Pattern on legislation.gov.uk: https://www.legislation.gov.uk/ukpga/{year}/{number}/section/{sec}
                act_num = act_data.get("act_number", "")
                year = act_data.get("year", "")
                c_match = re.search(r"c\.\s*(\d+)", act_num)
                if c_match and year:
                    section_url = f"https://www.legislation.gov.uk/ukpga/{year}/{c_match.group(1)}/section/{sec_clean}"
                else:
                    section_url = f"{official_url}#section-{sec_clean}"
            elif jurisdiction == "EU":
                # Pattern on EUR-Lex ELI: https://eur-lex.europa.eu/eli/reg/{year}/{number}/art_{sec}/oj
                if "eli/reg/" in official_url or "eli/dir/" in official_url:
                    base_eli = official_url.rstrip("/oj")
                    section_url = f"{base_eli}/art_{sec_clean}/oj"
                else:
                    section_url = f"{official_url}#art_{sec_clean}"
            elif jurisdiction == "US":
                if "constitution.congress.gov" in official_url:
                    section_url = f"{official_url}/browse/"
                elif "uscode.house.gov" in official_url:
                    section_url = f"{official_url}#sec_{sec_clean}"
                else:
                    section_url = f"{official_url}#section_{sec_clean}"
            else:
                section_url = f"{official_url}#section_{sec_clean}"

        return {
            "act_id": act_id,
            "act_title": act_title,
            "jurisdiction": jurisdiction,
            "section_number": section_number,
            "official_act_url": official_url or portal_info.get("legislation_base", ""),
            "official_section_url": section_url or official_url,
            "portal_name": portal_info.get("primary_name", "Official Gazette"),
            "managing_authority": portal_info.get("managing_authority", "National Government"),
            "is_airgapped_link": True
        }

    def link_citations_in_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Scans a text for statutory citations across US, UK, EU, and India,
        returning their resolved official government URLs.
        """
        if not self.registry:
            self._load_registry()

        found_links = []
        for act_id, meta in self.registry.items():
            aliases = meta.get("aliases", [])
            for alias in aliases:
                if len(alias) >= 3 and re.search(r"\b" + re.escape(alias) + r"\b", text, re.IGNORECASE):
                    # Try to extract section nearby
                    sec_match = re.search(r"\b(?:section|sec\.?|s\.|article|art\.?)\s*([0-9]+[A-Z0-9\-_.:]*)", text, re.IGNORECASE)
                    sec_num = sec_match.group(1) if sec_match else None
                    info = self.resolve_statute_link(act_id, sec_num)
                    if not any(f["act_id"] == act_id for f in found_links):
                        found_links.append(info)
                    break

        return found_links

    def format_citation_footnote(self, act_id: str, section_number: Optional[str] = None) -> str:
        """
        Returns a formatted markdown citation string linking to the official database.
        """
        link_info = self.resolve_statute_link(act_id, section_number)
        sec_label = f" § {section_number}" if section_number else ""
        return f"[{link_info['act_title']}{sec_label}]({link_info['official_section_url']}) ({link_info['portal_name']})"

statute_linker = StatuteWebLinker()

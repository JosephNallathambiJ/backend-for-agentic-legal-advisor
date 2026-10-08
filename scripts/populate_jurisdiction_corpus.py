#!/usr/bin/env python3
"""
scripts/populate_all_jurisdictions.py - Comprehensive Multi-Jurisdiction Legal Populator
Builds and populates authoritative datasets across 22 jurisdictions:
- Northern & Eastern Europe (18 countries: Belarus +375, Bulgaria +359, Czech Republic +420,
  Denmark +45, Estonia +372, Finland +358, Hungary +36, Iceland +354, Ireland +353, Latvia +371,
  Lithuania +370, Norway +47, Poland +48, Romania +40, Russia +7, Slovakia +421, Sweden +46, Ukraine +380)
- United States (13 acts: US Constitution 1787, Title 18 USC, UCC Art 2, Civil Rights Act 1964,
  Sherman Act 1890, Copyright Act 1976, Title 28 USC, Title 11 Bankruptcy, Title 35 Patents,
  Securities Exchange Act 1934, ADA 1990, FOIA 1966, APA 1946)
- United Kingdom (12 acts: Theft Act 1968, Contracts Act 1999, Consumer Rights 2015,
  Human Rights 1998, Fraud Act 2006, Data Protection Act 2018, Companies Act 2006,
  Sale of Goods 1979, Equality Act 2010, Arbitration Act 1996, PACE 1984, Bribery Act 2010)
- European Union (12 instruments: GDPR 2016/679, AI Act 2024/1689, DSA 2022/2065, DMA 2022/1925,
  TFEU 2012, Charter of Fundamental Rights, TEU 2016, E-Commerce Directive 2000/31,
  MiCA 2023/1114, Data Governance Act 2022/868, Copyright DSM 2019/790, CSDDD 2024/1760)
- India (876 Central Acts: BNS 2023, BNSS 2023, BSA 2023, ICA 1872, CPC 1908, IT Act 2000, etc.)
"""

import os
import sys
import json
import sqlite3
import hashlib
import pandas as pd
from typing import Dict, List, Any

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
CSV_DIR = os.path.join(DATA_DIR, "csv")
CORPUS_DIR = os.path.join(DATA_DIR, "legal_corpus")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
REGISTRY_DIR = os.path.join(DATA_DIR, "registry")
REGISTRY_FILE = os.path.join(REGISTRY_DIR, "registry_index.json")
SQLITE_DB = os.path.join(CACHE_DIR, "legal_cache.sqlite")

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(CORPUS_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(REGISTRY_DIR, exist_ok=True)

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

NE_EUROPE_CORPUS = [
    {
        "country": "Belarus",
        "dial_code": "+375",
        "jurisdiction": "BELARUS",
        "act_id": "BY_CONST_1994",
        "act_title": "Constitution of the Republic of Belarus (1994, as amended)",
        "short_title": "Belarus Constitution",
        "year": 1994,
        "act_number": "1994 Const. as amended",
        "enactment_date": "15-Mar-1994",
        "official_url": "https://pravo.by",
        "legislation_portal": "https://pravo.by",
        "supreme_court_portal": "https://court.gov.by",
        "constitutional_court_portal": "https://kc.gov.by",
        "aliases": ["belarus constitution", "constitution of belarus", "pravo.by", "by const"],
        "sections": [
            {
                "section_number": "1",
                "title": "State Sovereignty and Rule of Law",
                "text": "The Republic of Belarus is a unitary, democratic, social state governed by the rule of law. The Republic of Belarus exercises supreme control and absolute authority over the whole of its territory and independently administers its internal and foreign policy."
            },
            {
                "section_number": "21",
                "title": "Supreme Goal of the State",
                "text": "Ensuring the rights and liberties of citizens of the Republic of Belarus is the supreme goal of the State. The State guarantees the rights and liberties of citizens of Belarus that are enshrined in the Constitution and the laws."
            },
            {
                "section_number": "25",
                "title": "Personal Liberty and Inviolability",
                "text": "The State guarantees the personal freedom, inviolability and dignity of the individual. The restriction or deprivation of personal freedom is permissible only in the instances and under the procedure specified by law. No one shall be subjected to torture or to cruel, inhuman or degrading treatment or punishment."
            }
        ]
    },
    {
        "country": "Bulgaria",
        "dial_code": "+359",
        "jurisdiction": "BULGARIA",
        "act_id": "BG_CONST_1991",
        "act_title": "Constitution of the Republic of Bulgaria (1991)",
        "short_title": "Bulgarian Constitution",
        "year": 1991,
        "act_number": "DV 56/1991",
        "enactment_date": "12-Jul-1991",
        "official_url": "https://dv.parliament.bg",
        "legislation_portal": "https://dv.parliament.bg",
        "supreme_court_portal": "https://www.vks.bg",
        "constitutional_court_portal": "https://www.constcourt.bg",
        "aliases": ["bulgarian constitution", "constitution of bulgaria", "bg constitution", "dv parliament"],
        "sections": [
            {
                "section_number": "4",
                "title": "Rule of Law and International Norms",
                "text": "The Republic of Bulgaria shall be a state governed by the rule of law. It shall be governed by the Constitution and the laws of the country. The Republic of Bulgaria shall participate in the building and development of the European Union."
            },
            {
                "section_number": "5",
                "title": "Supremacy of the Constitution",
                "text": "The Constitution shall be the supreme law. No law or other normative act shall contravene it. The provisions of the Constitution shall apply directly. International treaties which have been ratified, promulgated and have entered into force shall be part of domestic law."
            },
            {
                "section_number": "31",
                "title": "Presumption of Innocence and Due Process",
                "text": "Anyone charged with a crime shall be brought before a judicial authority within 24 hours. Anyone charged with a crime shall be considered innocent until proven guilty by a final verdict of the court. No one shall be forced to confess guilt."
            }
        ]
    },
    {
        "country": "Czech Republic",
        "dial_code": "+420",
        "jurisdiction": "CZECH_REPUBLIC",
        "act_id": "CZ_CONST_1993",
        "act_title": "Constitution of the Czech Republic (Act No. 1/1993 Coll.)",
        "short_title": "Czech Constitution",
        "year": 1993,
        "act_number": "Act No. 1/1993 Coll.",
        "enactment_date": "16-Dec-1992",
        "official_url": "https://www.zakonyprolidi.cz",
        "legislation_portal": "https://www.zakonyprolidi.cz",
        "supreme_court_portal": "https://www.nsoud.cz",
        "constitutional_court_portal": "https://www.usoud.cz",
        "aliases": ["czech constitution", "constitution of the czech republic", "ustava cr", "act 1/1993 coll"],
        "sections": [
            {
                "section_number": "1",
                "title": "Democratic State Governed by the Rule of Law",
                "text": "The Czech Republic is a sovereign, unitary, and democratic state governed by the rule of law, founded on respect for the rights and freedoms of humans and citizens."
            },
            {
                "section_number": "9",
                "title": "Substantive Core of the Constitution",
                "text": "Any changes to the essential requirements of a democratic state governed by the rule of law are impermissible. Legal norms may not be interpreted in a way that eliminates or threatens the foundations of the democratic state."
            },
            {
                "section_number": "81",
                "title": "Independence of Judicial Power",
                "text": "The judicial power shall be exercised in the name of the Republic by independent courts. In performing their duties, judges shall be independent and bound solely by law and international treaties."
            }
        ]
    },
    {
        "country": "Denmark",
        "dial_code": "+45",
        "jurisdiction": "DENMARK",
        "act_id": "DK_CONST_1953",
        "act_title": "The Constitutional Act of Denmark (Danmarks Riges Grundlov)",
        "short_title": "Danish Constitution",
        "year": 1953,
        "act_number": "Grundlov nr. 169/1953",
        "enactment_date": "05-Jun-1953",
        "official_url": "https://www.retsinformation.dk",
        "legislation_portal": "https://www.retsinformation.dk",
        "supreme_court_portal": "https://domstol.dk/hoejesteret",
        "constitutional_court_portal": "https://domstol.dk",
        "aliases": ["danish constitution", "constitution of denmark", "grundloven", "danmarks riges grundlov"],
        "sections": [
            {
                "section_number": "3",
                "title": "Tripartite Division of State Powers",
                "text": "The legislative power shall be vested in the King and the Folketing conjointly. The executive power shall be vested in the King. The judicial power shall be vested in the courts of justice."
            },
            {
                "section_number": "71",
                "title": "Personal Liberty and Judicial Oversight",
                "text": "Personal liberty shall be inviolable. No Danish subject shall in any manner whatever be deprived of his liberty on account of his political or religious convictions or because of his descent. Any person taken into custody shall be brought before a judge within 24 hours."
            },
            {
                "section_number": "77",
                "title": "Freedom of Speech and Ban on Censorship",
                "text": "Any person shall be at liberty to publish his ideas in print, in writing, and in speech, subject to his being held responsible in a court of law. Censorship and other preventive measures shall never again be introduced."
            }
        ]
    },
    {
        "country": "Estonia",
        "dial_code": "+372",
        "jurisdiction": "ESTONIA",
        "act_id": "EE_CONST_1992",
        "act_title": "The Constitution of the Republic of Estonia (Eesti Vabariigi põhiseadus)",
        "short_title": "Estonian Constitution",
        "year": 1992,
        "act_number": "RT 1992, 26, 349",
        "enactment_date": "28-Jun-1992",
        "official_url": "https://www.riigiteataja.ee",
        "legislation_portal": "https://www.riigiteataja.ee",
        "supreme_court_portal": "https://www.riigikohus.ee",
        "constitutional_court_portal": "https://www.riigikohus.ee",
        "aliases": ["estonian constitution", "constitution of estonia", "pohiseadus", "riigi teataja"],
        "sections": [
            {
                "section_number": "1",
                "title": "Inherent Sovereignty and Indivisibility",
                "text": "Estonia is an independent and sovereign democratic republic wherein supreme political authority is vested in the people. The independence and sovereignty of Estonia are timeless and inalienable."
            },
            {
                "section_number": "12",
                "title": "Equality Before the Law and Non-Discrimination",
                "text": "Everyone is equal before the law. No one may be discriminated against on the basis of nationality, race, colour, sex, language, origin, religion, political or other opinion, property or social status, or other circumstances."
            },
            {
                "section_number": "20",
                "title": "Inviolability of Personal Liberty",
                "text": "Everyone has the right to liberty and security of person. No one may be deprived of their liberty except in the cases and pursuant to procedure provided by law. No one may be held in custody for more than 48 hours without permission of a court."
            }
        ]
    },
    {
        "country": "Finland",
        "dial_code": "+358",
        "jurisdiction": "FINLAND",
        "act_id": "FI_CONST_1999",
        "act_title": "The Constitution of Finland (Suomen perustuslaki 731/1999)",
        "short_title": "Finnish Constitution",
        "year": 1999,
        "act_number": "Perustuslaki 731/1999",
        "enactment_date": "11-Jun-1999",
        "official_url": "https://www.finlex.fi",
        "legislation_portal": "https://www.finlex.fi",
        "supreme_court_portal": "https://korkeinoikeus.fi",
        "constitutional_court_portal": "https://oikeus.fi",
        "aliases": ["finnish constitution", "constitution of finland", "perustuslaki", "finlex"],
        "sections": [
            {
                "section_number": "1",
                "title": "Constitutional Order and EU Membership",
                "text": "Finland is a sovereign republic. The constitution of Finland guarantees the inviolability of human dignity and the freedom and rights of the individual and promotes justice in society. Finland is a Member State of the European Union."
            },
            {
                "section_number": "21",
                "title": "Protection Under the Law and Fair Trial",
                "text": "Everyone has the right to have their case dealt with appropriately and without undue delay by an independent and impartial court of law or other authority. The publicity of proceedings, the right to be heard, the right to receive a reasoned decision and the right of appeal shall be guaranteed by an Act."
            },
            {
                "section_number": "106",
                "title": "Primacy of the Constitution",
                "text": "If, in a matter being tried by a court of law, the application of an Act would be in evident conflict with the Constitution, the court of law shall give primacy to the provision in the Constitution."
            }
        ]
    },
    {
        "country": "Hungary",
        "dial_code": "+36",
        "jurisdiction": "HUNGARY",
        "act_id": "HU_CONST_2011",
        "act_title": "The Fundamental Law of Hungary (Magyarország Alaptörvénye)",
        "short_title": "Fundamental Law of Hungary",
        "year": 2011,
        "act_number": "Alaptörvény 2011/43",
        "enactment_date": "25-Apr-2011",
        "official_url": "https://njt.hu",
        "legislation_portal": "https://njt.hu",
        "supreme_court_portal": "https://kuria-birosag.hu",
        "constitutional_court_portal": "https://alkotmanybirosag.hu",
        "aliases": ["hungarian constitution", "fundamental law of hungary", "alaptorveny", "kuria"],
        "sections": [
            {
                "section_number": "ArtB",
                "title": "Democratic State Governed by the Rule of Law",
                "text": "Hungary shall be an independent, democratic state governed by the rule of law. The source of public power shall be the people, exercising their power through elected representatives or directly."
            },
            {
                "section_number": "ArtII",
                "title": "Inviolability of Human Dignity",
                "text": "Human dignity shall be inviolable. Every human being shall have the right to life and human dignity; embryonic and foetal life shall be protected from the moment of conception."
            },
            {
                "section_number": "ArtIV",
                "title": "Liberty and Personal Security",
                "text": "Everyone shall have the right to liberty and security of the person. No one shall be deprived of liberty except for reasons and pursuant to procedure specified by law. Anyone suspected of committing a criminal offence and held in detention shall be brought before a court within the shortest possible time."
            }
        ]
    },
    {
        "country": "Iceland",
        "dial_code": "+354",
        "jurisdiction": "ICELAND",
        "act_id": "IS_CONST_1944",
        "act_title": "The Constitution of the Republic of Iceland (Stjórnarskrá lýðveldisins Íslands No. 33/1944)",
        "short_title": "Icelandic Constitution",
        "year": 1944,
        "act_number": "Lög nr. 33/1944",
        "enactment_date": "17-Jun-1944",
        "official_url": "https://www.althingi.is/lagasafn/",
        "legislation_portal": "https://www.althingi.is/lagasafn/",
        "supreme_court_portal": "https://www.haestirettur.is",
        "constitutional_court_portal": "https://www.domstolar.is",
        "aliases": ["icelandic constitution", "constitution of iceland", "stjornarskrain", "althingi"],
        "sections": [
            {
                "section_number": "1",
                "title": "Republic and Democratic Form of Government",
                "text": "Iceland is a republic with a parliamentary government."
            },
            {
                "section_number": "67",
                "title": "Protection Against Deprivation of Liberty",
                "text": "No one may be deprived of their liberty except as permitted by law. Anyone arrested shall be brought before a judge without undue delay, and if not released forthwith, the judge shall within 24 hours issue a reasoned ruling on detention."
            },
            {
                "section_number": "70",
                "title": "Right to Fair Hearing and Independent Court",
                "text": "Everyone shall be entitled to a fair and public hearing within a reasonable time by an independent and impartial court for the determination of his rights and obligations or of any criminal charge against him."
            }
        ]
    },
    {
        "country": "Ireland",
        "dial_code": "+353",
        "jurisdiction": "IRELAND",
        "act_id": "IE_CONST_1937",
        "act_title": "Constitution of Ireland (Bunreacht na hÉireann 1937)",
        "short_title": "Irish Constitution",
        "year": 1937,
        "act_number": "Bunreacht na hÉireann 1937",
        "enactment_date": "01-Jul-1937",
        "official_url": "https://www.irishstatutebook.ie",
        "legislation_portal": "https://www.irishstatutebook.ie",
        "supreme_court_portal": "https://www.supremecourt.ie",
        "constitutional_court_portal": "https://www.courts.ie",
        "aliases": ["irish constitution", "constitution of ireland", "bunreacht na heireann", "irish statute book"],
        "sections": [
            {
                "section_number": "Art34.Sec1",
                "title": "Administration of Justice in Public Courts",
                "text": "Justice shall be administered in courts established by law by judges appointed in the manner provided by this Constitution, and, save in such special and limited cases as may be prescribed by law, shall be administered in public."
            },
            {
                "section_number": "Art40.Sec1",
                "title": "Fundamental Rights: Equality Before the Law",
                "text": "All citizens shall, as human persons, be held equal before the law. This shall not be held to mean that the State shall not in its enactments have due regard to differences of capacity, physical and moral, and of social function."
            },
            {
                "section_number": "Art40.Sec4",
                "title": "Personal Liberty and Habeas Corpus",
                "text": "No citizen shall be deprived of his personal liberty save in accordance with law. Upon complaint being made by or on behalf of any person that he is being unlawfully detained, the High Court shall forthwith inquire into the grounds of detention."
            }
        ]
    },
    {
        "country": "Latvia",
        "dial_code": "+371",
        "jurisdiction": "LATVIA",
        "act_id": "LV_CONST_1922",
        "act_title": "The Constitution of the Republic of Latvia (Latvijas Republikas Satversme 1922)",
        "short_title": "Latvian Constitution (Satversme)",
        "year": 1922,
        "act_number": "Satversme 1922",
        "enactment_date": "15-Feb-1922",
        "official_url": "https://likumi.lv",
        "legislation_portal": "https://likumi.lv",
        "supreme_court_portal": "https://www.at.gov.lv",
        "constitutional_court_portal": "https://www.satv.tiesa.gov.lv",
        "aliases": ["latvian constitution", "constitution of latvia", "satversme", "likumi.lv"],
        "sections": [
            {
                "section_number": "1",
                "title": "Democratic Republic State Foundation",
                "text": "Latvia is an independent democratic republic."
            },
            {
                "section_number": "92",
                "title": "Right to Fair Trial and Defense",
                "text": "Everyone has the right to defend their rights and lawful interests in a fair court. Everyone shall be presumed innocent until their guilt is established in accordance with law. Everyone has the right to the assistance of an attorney."
            },
            {
                "section_number": "94",
                "title": "Freedom and Inviolability of Person",
                "text": "Everyone has the right to freedom and inviolability of person. No one may be deprived of or restricted in their freedom except in accordance with law."
            }
        ]
    },
    {
        "country": "Lithuania",
        "dial_code": "+370",
        "jurisdiction": "LITHUANIA",
        "act_id": "LT_CONST_1992",
        "act_title": "The Constitution of the Republic of Lithuania (Lietuvos Respublikos Konstitucija 1992)",
        "short_title": "Lithuanian Constitution",
        "year": 1992,
        "act_number": "Konstitucija 1992",
        "enactment_date": "25-Oct-1992",
        "official_url": "https://e-seimas.lrs.lt",
        "legislation_portal": "https://e-seimas.lrs.lt",
        "supreme_court_portal": "https://www.lat.lt",
        "constitutional_court_portal": "https://www.lrkt.lt",
        "aliases": ["lithuanian constitution", "constitution of lithuania", "lr konstitucija", "seimas"],
        "sections": [
            {
                "section_number": "1",
                "title": "Independent Democratic Republic",
                "text": "The State of Lithuania shall be an independent democratic republic."
            },
            {
                "section_number": "20",
                "title": "Inviolability of Human Freedom",
                "text": "Human freedom shall be inviolable. No one may be arbitrarily detained or held in custody. No one may be deprived of freedom except on such grounds and in accordance with such procedures as established by law. A person detained shall be brought before a court within 48 hours."
            },
            {
                "section_number": "31",
                "title": "Presumption of Innocence and Right to Counsel",
                "text": "Every person shall be presumed innocent until proved guilty according to the procedure established by law and until declared guilty by a court judgment that has come into force. A person suspected of committing a crime shall be guaranteed the right to defense from the moment of arrest."
            }
        ]
    },
    {
        "country": "Norway",
        "dial_code": "+47",
        "jurisdiction": "NORWAY",
        "act_id": "NO_CONST_1814",
        "act_title": "The Constitution of the Kingdom of Norway (Kongeriket Norges Grunnlov 1814)",
        "short_title": "Norwegian Constitution",
        "year": 1814,
        "act_number": "Grunnloven 1814",
        "enactment_date": "17-May-1814",
        "official_url": "https://lovdata.no",
        "legislation_portal": "https://lovdata.no",
        "supreme_court_portal": "https://www.domstol.no/en/supremecourt/",
        "constitutional_court_portal": "https://www.domstol.no",
        "aliases": ["norwegian constitution", "constitution of norway", "grunnloven", "lovdata"],
        "sections": [
            {
                "section_number": "Art2",
                "title": "Values of Human Rights and Democracy",
                "text": "The value foundation shall remain our Christian and humanist heritage. This Constitution shall ensure democracy, the rule of law and human rights."
            },
            {
                "section_number": "Art94",
                "title": "Protection Against Arbitrary Deprivation of Liberty",
                "text": "No one may be taken into custody or otherwise deprived of their liberty except in the cases and in the manner determined by law. Anyone arrested shall be brought before a judge within the shortest possible time."
            },
            {
                "section_number": "Art95",
                "title": "Right to Fair Trial by Independent Courts",
                "text": "Everyone has the right to have their case determined by an independent and impartial court within a reasonable time. The authorities of the state shall ensure the independence and impartiality of the courts and the judges."
            }
        ]
    },
    {
        "country": "Poland",
        "dial_code": "+48",
        "jurisdiction": "POLAND",
        "act_id": "PL_CONST_1997",
        "act_title": "The Constitution of the Republic of Poland (Konstytucja Rzeczypospolitej Polskiej 1997)",
        "short_title": "Polish Constitution",
        "year": 1997,
        "act_number": "Dz.U. 1997 nr 78 poz. 483",
        "enactment_date": "02-Apr-1997",
        "official_url": "https://isap.sejm.gov.pl",
        "legislation_portal": "https://isap.sejm.gov.pl",
        "supreme_court_portal": "https://www.sn.pl",
        "constitutional_court_portal": "https://trybunal.gov.pl",
        "aliases": ["polish constitution", "constitution of poland", "konstytucja rp", "sejm", "trybunal"],
        "sections": [
            {
                "section_number": "2",
                "title": "Democratic State Governed by the Rule of Law",
                "text": "The Republic of Poland shall be a democratic state ruled by law and implementing the principles of social justice."
            },
            {
                "section_number": "7",
                "title": "Principle of Legalism",
                "text": "The organs of public authority shall function on the basis of, and within the limits of, the law."
            },
            {
                "section_number": "41",
                "title": "Personal Inviolability and Liberty",
                "text": "Personal inviolability and security shall be ensured to everyone. Any deprivation or limitation of liberty may be imposed only in accordance with principles and under procedures specified by statute. Anyone detained shall be informed immediately of the reasons for detention and brought before a court within 48 hours."
            },
            {
                "section_number": "45",
                "title": "Right to Fair and Public Hearing",
                "text": "Everyone shall have the right to a fair and public hearing of his case, without undue delay, before a competent, impartial and independent court."
            }
        ]
    },
    {
        "country": "Romania",
        "dial_code": "+40",
        "jurisdiction": "ROMANIA",
        "act_id": "RO_CONST_1991",
        "act_title": "Constitution of Romania (Constituția României 1991)",
        "short_title": "Romanian Constitution",
        "year": 1991,
        "act_number": "M.Of. nr. 767/2003",
        "enactment_date": "21-Nov-1991",
        "official_url": "http://legislatie.just.ro",
        "legislation_portal": "http://legislatie.just.ro",
        "supreme_court_portal": "https://www.iccj.ro",
        "constitutional_court_portal": "https://www.ccr.ro",
        "aliases": ["romanian constitution", "constitution of romania", "constitutia romaniei", "iccj", "ccr"],
        "sections": [
            {
                "section_number": "1",
                "title": "State of Law and Democratic Republic",
                "text": "Romania is a sovereign, independent, unitary, and indivisible National State. Romania is a democratic and social state governed by the rule of law, in which human dignity, the citizens' rights and freedoms, the free development of human personality, justice and political pluralism represent supreme values."
            },
            {
                "section_number": "21",
                "title": "Free Access to Justice",
                "text": "Every person is entitled to bring cases before the courts for the defense of their rights, liberties and lawful interests. The exercise of this right may not be restricted by any law. Parties have the right to a fair trial and to the solution of cases within a reasonable term."
            },
            {
                "section_number": "23",
                "title": "Individual Freedom and Detention Oversight",
                "text": "Individual freedom and personal security are inviolable. Search, detention or arrest of a person shall be permitted only in the cases and under the procedure provided by law. Custody cannot exceed 24 hours. Pre-trial detention may be ordered only by a judge."
            }
        ]
    },
    {
        "country": "Russia",
        "dial_code": "+7",
        "jurisdiction": "RUSSIA",
        "act_id": "RU_CONST_1993",
        "act_title": "Constitution of the Russian Federation (Конституция Российской Федерации 1993)",
        "short_title": "Russian Constitution",
        "year": 1993,
        "act_number": "RG 237/1993",
        "enactment_date": "12-Dec-1993",
        "official_url": "http://pravo.gov.ru",
        "legislation_portal": "http://pravo.gov.ru",
        "supreme_court_portal": "https://www.vsrf.ru",
        "constitutional_court_portal": "https://ksrf.ru",
        "aliases": ["russian constitution", "constitution of russia", "konstitutsiya rf", "pravo.gov.ru"],
        "sections": [
            {
                "section_number": "1",
                "title": "Democratic Federative Rule of Law State",
                "text": "The Russian Federation — Russia is a democratic federative law-governed state with a republican form of government."
            },
            {
                "section_number": "2",
                "title": "Human Being and Rights as Supreme Value",
                "text": "The human being, his rights and freedoms are the supreme value. Recognition, observance and protection of the rights and freedoms of human and citizen shall be the obligation of the State."
            },
            {
                "section_number": "22",
                "title": "Right to Freedom and Personal Inviolability",
                "text": "Everyone shall have the right to freedom and personal inviolability. Arrest, detention and remanding in custody shall be permissible only under a judicial decision. Prior to a judicial decision, no person may be detained for a period exceeding 48 hours."
            },
            {
                "section_number": "49",
                "title": "Presumption of Innocence",
                "text": "Everyone accused of committing a crime shall be considered innocent until his guilt is proved in accordance with federal law and established by the legally valid verdict of a court."
            }
        ]
    },
    {
        "country": "Slovakia",
        "dial_code": "+421",
        "jurisdiction": "SLOVAKIA",
        "act_id": "SK_CONST_1992",
        "act_title": "Constitution of the Slovak Republic (Ústava Slovenskej republiky No. 460/1992 Coll.)",
        "short_title": "Slovak Constitution",
        "year": 1992,
        "act_number": "Zákon č. 460/1992 Zb.",
        "enactment_date": "01-Sep-1992",
        "official_url": "https://www.s-slov-lex.sk",
        "legislation_portal": "https://www.s-slov-lex.sk",
        "supreme_court_portal": "https://www.nsud.sk",
        "constitutional_court_portal": "https://www.ustavnysud.sk",
        "aliases": ["slovak constitution", "constitution of slovakia", "ustava sr", "slov-lex"],
        "sections": [
            {
                "section_number": "1",
                "title": "Sovereignty and Constitutional Order",
                "text": "The Slovak Republic is a sovereign, democratic state governed by the rule of law. It shall not be bound to any ideology or religion."
            },
            {
                "section_number": "17",
                "title": "Personal Freedom and Detention Limits",
                "text": "Personal freedom shall be guaranteed. No one may be prosecuted or deprived of freedom otherwise than for reasons and in a manner provided by law. A person taken into custody shall be brought before a court within 48 hours."
            },
            {
                "section_number": "46",
                "title": "Right to Judicial and Other Legal Protection",
                "text": "Everyone may claim their right in the manner established by law before an independent and impartial court, or before another body of the Slovak Republic in cases specified by law."
            }
        ]
    },
    {
        "country": "Sweden",
        "dial_code": "+46",
        "jurisdiction": "SWEDEN",
        "act_id": "SE_CONST_1974",
        "act_title": "The Instrument of Government (Regeringsformen 1974:152 - Constitution of Sweden)",
        "short_title": "Swedish Constitution (Regeringsformen)",
        "year": 1974,
        "act_number": "SFS 1974:152",
        "enactment_date": "28-Feb-1974",
        "official_url": "https://rkrattsbaser.gov.se",
        "legislation_portal": "https://rkrattsbaser.gov.se",
        "supreme_court_portal": "https://www.hogstadomstolen.se",
        "constitutional_court_portal": "https://www.domstol.se",
        "aliases": ["swedish constitution", "constitution of sweden", "regeringsformen", "sfs 1974:152", "domstol"],
        "sections": [
            {
                "section_number": "1:1",
                "title": "Democracy and Sovereignty of the People",
                "text": "All public power in Sweden proceeds from the people. Swedish democracy is founded on the free formation of opinion and on universal and equal suffrage. It is realised through a representative and parliamentary form of government and through local self-government."
            },
            {
                "section_number": "2:8",
                "title": "Protection Against Deprivation of Liberty",
                "text": "Everyone shall be protected in their relations with the public institutions against any deprivation of personal liberty. Swedish citizens shall also in other respects be guaranteed freedom of movement within the Realm and freedom to depart the Realm."
            },
            {
                "section_number": "2:11",
                "title": "Right to Public Trial and Prohibition of Retroactivity",
                "text": "A trial shall be conducted openly and publicly. A trial shall be conducted fairly and within a reasonable time. No court may be established on account of a specific act already committed, nor for a specific dispute. No penalty or other penal sanction may be imposed for an act which was not subject to a penal sanction at the time it was committed."
            }
        ]
    },
    {
        "country": "Ukraine",
        "dial_code": "+380",
        "jurisdiction": "UKRAINE",
        "act_id": "UA_CONST_1996",
        "act_title": "Constitution of Ukraine (Конституція України 1996)",
        "short_title": "Ukrainian Constitution",
        "year": 1996,
        "act_number": "VVR 1996 No. 30 art. 141",
        "enactment_date": "28-Jun-1996",
        "official_url": "https://zakon.rada.gov.ua",
        "legislation_portal": "https://zakon.rada.gov.ua",
        "supreme_court_portal": "https://supreme.court.gov.ua",
        "constitutional_court_portal": "https://ccu.gov.ua",
        "aliases": ["ukrainian constitution", "constitution of ukraine", "konstytutsiya ukrayiny", "rada.gov.ua"],
        "sections": [
            {
                "section_number": "1",
                "title": "Sovereign and Democratic State",
                "text": "Ukraine is a sovereign and independent, democratic, social, law-governed state."
            },
            {
                "section_number": "8",
                "title": "Rule of Law and Constitutional Supremacy",
                "text": "In Ukraine, the principle of the rule of law is recognized and effective. The Constitution of Ukraine has the highest legal force. Laws and other normative legal acts shall be adopted on the basis of the Constitution of Ukraine and conform to it. The norms of the Constitution are directly applicable."
            },
            {
                "section_number": "29",
                "title": "Right to Freedom and Personal Inviolability",
                "text": "Every person has the right to freedom and personal inviolability. No one may be arrested or held in custody other than pursuant to a reasoned court decision and only on the grounds and in accordance with procedure established by law. In case of urgent necessity, detention cannot exceed 72 hours."
            },
            {
                "section_number": "62",
                "title": "Presumption of Innocence and Exclusion of Illegal Evidence",
                "text": "A person shall be presumed innocent of committing a crime and shall not be subjected to criminal punishment until guilt is proved through legal procedure and established by a court verdict of guilty. An accusation shall not be based on illegally obtained evidence."
            }
        ]
    }
]

US_CORPUS = [
    {
        "act_id": "US_CONST_1787",
        "act_title": "Constitution of the United States of America (1787)",
        "short_title": "US Constitution",
        "year": 1787,
        "act_number": "U.S. Const. (1787)",
        "enactment_date": "17-Sep-1787",
        "official_url": "https://constitution.congress.gov",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "us constitution",
            "united states constitution",
            "constitution of the united states",
            "u.s. const."
        ],
        "sections": [
            {
                "section_number": "Art1.Sec1",
                "title": "Legislative Powers Vested in Congress",
                "text": "All legislative Powers herein granted shall be vested in a Congress of the United States, which shall consist of a Senate and House of Representatives."
            },
            {
                "section_number": "Art1.Sec8",
                "title": "Powers of Congress: Taxation, Commerce, General Welfare",
                "text": "The Congress shall have Power To lay and collect Taxes, Duties, Imposts and Excises, to pay the Debts and provide for the common Defence and general Welfare of the United States; To regulate Commerce with foreign Nations, and among the several States."
            },
            {
                "section_number": "Art2.Sec1",
                "title": "Executive Power Vested in the President",
                "text": "The executive Power shall be vested in a President of the United States of America. He shall hold his Office during the Term of four Years."
            },
            {
                "section_number": "Art3.Sec2",
                "title": "Judicial Power and Jurisdiction",
                "text": "The judicial Power shall extend to all Cases, in Law and Equity, arising under this Constitution, the Laws of the United States, and Treaties made, or which shall be made, under their Authority."
            },
            {
                "section_number": "Amend1",
                "title": "Freedom of Religion, Speech, Press, Assembly, and Petition",
                "text": "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances."
            },
            {
                "section_number": "Amend4",
                "title": "Search and Seizure Protections",
                "text": "The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, but upon probable cause, supported by Oath or affirmation, and particularly describing the place to be searched, and the persons or things to be seized."
            },
            {
                "section_number": "Amend5",
                "title": "Grand Jury, Double Jeopardy, Self-Incrimination, Due Process",
                "text": "No person shall be held to answer for a capital, or otherwise infamous crime, unless on a presentment or indictment of a Grand Jury; nor shall any person be subject for the same offence to be twice put in jeopardy of life or limb; nor shall be compelled in any criminal case to be a witness against himself, nor be deprived of life, liberty, or property, without due process of law."
            },
            {
                "section_number": "Amend14",
                "title": "Citizenship Rights, Due Process, and Equal Protection",
                "text": "No State shall make or enforce any law which shall abridge the privileges or immunities of citizens of the United States; nor shall any State deprive any person of life, liberty, or property, without due process of law; nor deny to any person within its jurisdiction the equal protection of the laws."
            }
        ]
    },
    {
        "act_id": "US_TITLE_18",
        "act_title": "United States Code Title 18 \u2014 Crimes and Criminal Procedure",
        "short_title": "Title 18 U.S.C.",
        "year": 1948,
        "act_number": "Title 18 U.S.C. (62 Stat. 683)",
        "enactment_date": "25-Jun-1948",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title18&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "title 18",
            "18 usc",
            "18 u.s.c.",
            "title 18 usc",
            "federal criminal code"
        ],
        "sections": [
            {
                "section_number": "641",
                "title": "Public money, property or records (Theft of Government Property)",
                "text": "Whoever embezzles, steals, purloins, or knowingly converts to his use or the use of another, or without authority, sells, conveys or disposes of any record, voucher, money, or thing of value of the United States or of any department or agency thereof shall be fined under this title or imprisoned not more than ten years, or both."
            },
            {
                "section_number": "1001",
                "title": "Statements or entries generally (False Statements to Federal Agencies)",
                "text": "Except as otherwise provided in this section, whoever, in any matter within the jurisdiction of the executive, legislative, or judicial branch of the Government of the United States, knowingly and willfully falsifies, conceals, or covers up by any trick, scheme, or device a material fact or makes any materially false, fictitious, or fraudulent statement or representation shall be fined under this title, imprisoned not more than 5 years."
            },
            {
                "section_number": "1341",
                "title": "Frauds and swindles (Mail Fraud)",
                "text": "Whoever, having devised or intending to devise any scheme or artifice to defraud, or for obtaining money or property by means of false or fraudulent pretenses, representations, or promises, places in any post office or authorized depository for mail matter, any matter or thing whatever to be sent or delivered by the Postal Service, shall be fined under this title or imprisoned not more than 20 years, or both."
            },
            {
                "section_number": "1343",
                "title": "Fraud by wire, radio, or television (Wire Fraud)",
                "text": "Whoever, having devised or intending to devise any scheme or artifice to defraud, transmits or causes to be transmitted by means of wire, radio, or television communication in interstate or foreign commerce, any writings, signs, signals, pictures, or sounds for the purpose of executing such scheme or artifice, shall be fined under this title or imprisoned not more than 20 years, or both."
            },
            {
                "section_number": "1503",
                "title": "Influencing or injuring officer or juror generally (Obstruction of Justice)",
                "text": "Whoever corruptly, or by threats or force, or by any threatening letter or communication, endeavors to influence, intimidate, or impede any grand or petit juror, or officer in or of any court of the United States, in the discharge of his duty, or corruptly or by threats or force, or by any threatening letter or communication, influences, obstructs, or impedes, or endeavors to influence, obstruct, or impede, the due administration of justice, shall be punished."
            },
            {
                "section_number": "1956",
                "title": "Laundering of monetary instruments (Money Laundering)",
                "text": "Whoever, knowing that the property involved in a financial transaction represents the proceeds of some form of unlawful activity, conducts or attempts to conduct such a financial transaction which in fact involves the proceeds of specified unlawful activity with the intent to promote the carrying on of specified unlawful activity, shall be sentenced to a fine or imprisonment for not more than twenty years, or both."
            }
        ]
    },
    {
        "act_id": "US_JUDICIARY_TITLE_28",
        "act_title": "United States Code Title 28 \u2014 Judiciary and Judicial Procedure",
        "short_title": "Title 28 U.S.C.",
        "year": 1948,
        "act_number": "Title 28 U.S.C. (62 Stat. 869)",
        "enactment_date": "25-Jun-1948",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title28&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "title 28",
            "28 usc",
            "28 u.s.c.",
            "federal judiciary act"
        ],
        "sections": [
            {
                "section_number": "1331",
                "title": "Federal question jurisdiction",
                "text": "The district courts shall have original jurisdiction of all civil actions arising under the Constitution, laws, or treaties of the United States."
            },
            {
                "section_number": "1332",
                "title": "Diversity of citizenship; amount in controversy; costs",
                "text": "The district courts shall have original jurisdiction of all civil actions where the matter in controversy exceeds the sum or value of $75,000, exclusive of interest and costs, and is between citizens of different States."
            }
        ]
    },
    {
        "act_id": "US_UCC_ART_2",
        "act_title": "Uniform Commercial Code \u2014 Article 2: Sales",
        "short_title": "UCC Article 2",
        "year": 1951,
        "act_number": "U.C.C. Article 2 (ALI/ULC)",
        "enactment_date": "01-Jan-1951",
        "official_url": "https://www.law.cornell.edu/ucc/2",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "ucc",
            "ucc article 2",
            "uniform commercial code",
            "ucc art 2"
        ],
        "sections": [
            {
                "section_number": "2-106",
                "title": "Definitions: Contract; Agreement; Contract for Sale; Sale; Present Sale",
                "text": "In this Article unless the context otherwise requires 'contract' and 'agreement' are limited to those relating to the present or future sale of goods. 'Contract for sale' includes both a present sale of goods and a contract to sell goods at a future time. A 'sale' consists in the passing of title from the seller to the buyer for a price."
            },
            {
                "section_number": "2-201",
                "title": "Formal Requirements; Statute of Frauds",
                "text": "Except as otherwise provided in this section a contract for the sale of goods for the price of $500 or more is not enforceable by way of action or defense unless there is some writing sufficient to indicate that a contract for sale has been made between the parties and signed by the party against whom enforcement is sought or by his authorized agent or broker."
            },
            {
                "section_number": "2-206",
                "title": "Offer and Acceptance in Formation of Contract",
                "text": "Unless otherwise unambiguously indicated by the language or circumstances an offer to make a contract shall be construed as inviting acceptance in any manner and by any medium reasonable in the circumstances."
            },
            {
                "section_number": "2-302",
                "title": "Unconscionable Contract or Clause",
                "text": "If the court as a matter of law finds the contract or any clause of the contract to have been unconscionable at the time it was made the court may refuse to enforce the contract, or it may enforce the remainder of the contract without the unconscionable clause, or it may so limit the application of any unconscionable clause as to avoid any unconscionable result."
            },
            {
                "section_number": "2-314",
                "title": "Implied Warranty: Merchantability; Usage of Trade",
                "text": "Unless excluded or modified, a warranty that the goods shall be merchantable is implied in a contract for their sale if the seller is a merchant with respect to goods of that kind. Goods to be merchantable must be at least such as are fit for the ordinary purposes for which such goods are used."
            },
            {
                "section_number": "2-713",
                "title": "Buyer's Damages for Non-Delivery or Repudiation",
                "text": "The measure of damages for non-delivery or repudiation by the seller is the difference between the market price at the time when the buyer learned of the breach and the contract price together with any incidental and consequential damages provided in this Article, but less expenses saved in consequence of the seller's breach."
            },
            {
                "section_number": "2-719",
                "title": "Contractual Modification or Limitation of Remedy",
                "text": "The agreement may provide for remedies in addition to or in substitution for those provided in this Article and may limit or alter the measure of damages recoverable under this Article, as by limiting the buyer's remedies to return of the goods and repayment of the price or to repair and replacement of non-conforming goods or parts."
            }
        ]
    },
    {
        "act_id": "US_CIVIL_RIGHTS_1964",
        "act_title": "Civil Rights Act of 1964 (Pub. L. 88-352, Title 42 U.S.C.)",
        "short_title": "Civil Rights Act of 1964",
        "year": 1964,
        "act_number": "Pub. L. 88-352 (78 Stat. 241)",
        "enactment_date": "02-Jul-1964",
        "official_url": "https://www.congress.gov/bill/88th-congress/house-bill/7152",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "civil rights act",
            "civil rights act 1964",
            "title vii",
            "title 42 usc 2000e"
        ],
        "sections": [
            {
                "section_number": "201",
                "title": "Prohibition against discrimination in places of public accommodation",
                "text": "All persons shall be entitled to the full and equal enjoyment of the goods, services, facilities, privileges, advantages, and accommodations of any place of public accommodation, as defined in this section, without discrimination or segregation on the ground of race, color, religion, or national origin."
            },
            {
                "section_number": "703",
                "title": "Unlawful employment practices (Title VII)",
                "text": "It shall be an unlawful employment practice for an employer to fail or refuse to hire or to discharge any individual, or otherwise to discriminate against any individual with respect to his compensation, terms, conditions, or privileges of employment, because of such individual's race, color, religion, sex, or national origin."
            }
        ]
    },
    {
        "act_id": "US_VOTING_RIGHTS_1965",
        "act_title": "Voting Rights Act of 1965 (Pub. L. 89-110, Title 52 U.S.C.)",
        "short_title": "Voting Rights Act of 1965",
        "year": 1965,
        "act_number": "Pub. L. 89-110 (79 Stat. 437)",
        "enactment_date": "06-Aug-1965",
        "official_url": "https://www.congress.gov/bill/89th-congress/senate-bill/1564",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "voting rights act",
            "voting rights act 1965",
            "vra 1965"
        ],
        "sections": [
            {
                "section_number": "2",
                "title": "Denial or abridgement of right to vote on account of race or color through voting qualification or prerequisite",
                "text": "No voting qualification or prerequisite to voting or standard, practice, or procedure shall be imposed or applied by any State or political subdivision in a manner which results in a denial or abridgement of the right of any citizen of the United States to vote on account of race or color."
            },
            {
                "section_number": "5",
                "title": "Preclearance requirements for alterations of voting qualifications",
                "text": "Whenever a State or political subdivision covered by the Act shall enact or seek to administer any voting qualification or prerequisite to voting, such State or subdivision may institute an action for a declaratory judgment that such qualification does not have the purpose and will not have the effect of denying or abridging the right to vote on account of race."
            }
        ]
    },
    {
        "act_id": "US_SHERMAN_1890",
        "act_title": "Sherman Antitrust Act of 1890 (Title 15 U.S.C. Sections 1-7)",
        "short_title": "Sherman Antitrust Act",
        "year": 1890,
        "act_number": "26 Stat. 209 (Title 15 U.S.C.)",
        "enactment_date": "02-Jul-1890",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title15/chapter1&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "sherman act",
            "sherman antitrust act",
            "sherman act 1890",
            "15 usc 1"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Trusts, etc., in restraint of trade illegal; penalty",
                "text": "Every contract, combination in the form of trust or otherwise, or conspiracy, in restraint of trade or commerce among the several States, or with foreign nations, is declared to be illegal. Every person who shall make any contract or engage in any combination or conspiracy hereby declared to be illegal shall be deemed guilty of a felony."
            },
            {
                "section_number": "2",
                "title": "Monopolizing trade a felony; penalty",
                "text": "Every person who shall monopolize, or attempt to monopolize, or combine or conspire with any other person or persons, to monopolize any part of the trade or commerce among the several States, or with foreign nations, shall be deemed guilty of a felony."
            }
        ]
    },
    {
        "act_id": "US_CLAYTON_1914",
        "act_title": "Clayton Antitrust Act of 1914 (Title 15 U.S.C. Section 12 et seq.)",
        "short_title": "Clayton Antitrust Act",
        "year": 1914,
        "act_number": "Pub. L. 63-212 (38 Stat. 730)",
        "enactment_date": "15-Oct-1914",
        "official_url": "https://www.congress.gov/bill/63rd-congress/house-bill/15657",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "clayton act",
            "clayton antitrust act",
            "15 usc 18"
        ],
        "sections": [
            {
                "section_number": "7",
                "title": "Acquisition by one corporation of stock of another lessening competition",
                "text": "No person engaged in commerce or in any activity affecting commerce shall acquire, directly or indirectly, the whole or any part of the stock or other share capital or assets of another person where the effect of such acquisition may be substantially to lessen competition, or to tend to create a monopoly."
            }
        ]
    },
    {
        "act_id": "US_FTC_ACT_1914",
        "act_title": "Federal Trade Commission Act (Title 15 U.S.C. Section 45 et seq.)",
        "short_title": "FTC Act",
        "year": 1914,
        "act_number": "Pub. L. 63-203 (38 Stat. 717)",
        "enactment_date": "26-Sep-1914",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title15/chapter2/subchapter1&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "ftc act",
            "federal trade commission act",
            "15 usc 45"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Unfair methods of competition unlawful; prevention by Commission",
                "text": "Unfair methods of competition in or affecting commerce, and unfair or deceptive acts or practices in or affecting commerce, are hereby declared unlawful. The Commission is hereby empowered and directed to prevent persons, partnerships, or corporations from using unfair methods of competition."
            }
        ]
    },
    {
        "act_id": "US_SECURITIES_1933",
        "act_title": "Securities Act of 1933 (Title 15 U.S.C. Section 77a et seq.)",
        "short_title": "Securities Act of 1933",
        "year": 1933,
        "act_number": "Pub. L. 73-22 (48 Stat. 74)",
        "enactment_date": "27-May-1933",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title15/chapter2A&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "securities act of 1933",
            "1933 act",
            "securities act",
            "15 usc 77a"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Prohibitions relating to interstate commerce and the mails",
                "text": "Unless a registration statement is in effect as to a security, it shall be unlawful for any person, directly or indirectly, to make use of any means or instruments of transportation or communication in interstate commerce or of the mails to sell such security through the use or medium of any prospectus or otherwise."
            },
            {
                "section_number": "11",
                "title": "Civil liabilities on account of false registration statement",
                "text": "In case any part of the registration statement, when such part became effective, contained an untrue statement of a material fact or omitted to state a material fact required to be stated therein or necessary to make the statements therein not misleading, any person acquiring such security may sue."
            }
        ]
    },
    {
        "act_id": "US_SECURITIES_EXCHANGE_1934",
        "act_title": "Securities Exchange Act of 1934 (Title 15 U.S.C. Section 78a et seq.)",
        "short_title": "Securities Exchange Act of 1934",
        "year": 1934,
        "act_number": "48 Stat. 881 (Title 15 U.S.C.)",
        "enactment_date": "06-Jun-1934",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title15/chapter2B&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "securities exchange act",
            "1934 act",
            "exchange act",
            "rule 10b-5",
            "15 usc 78j"
        ],
        "sections": [
            {
                "section_number": "10(b)",
                "title": "Employment of manipulative and deceptive devices",
                "text": "It shall be unlawful for any person, directly or indirectly, by the use of any means or instrumentality of interstate commerce or of the mails, or of any facility of any national securities exchange, to use or employ, in connection with the purchase or sale of any security, any manipulative or deceptive device or contrivance."
            }
        ]
    },
    {
        "act_id": "US_COPYRIGHT_1976",
        "act_title": "Copyright Act of 1976 (Title 17 U.S.C.)",
        "short_title": "Copyright Act of 1976",
        "year": 1976,
        "act_number": "Pub. L. 94-553 (Title 17 U.S.C.)",
        "enactment_date": "19-Oct-1976",
        "official_url": "https://www.congress.gov/bill/94th-congress/senate-bill/22",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "copyright act",
            "copyright act 1976",
            "title 17 usc",
            "17 usc 106"
        ],
        "sections": [
            {
                "section_number": "106",
                "title": "Exclusive rights in copyrighted works",
                "text": "Subject to sections 107 through 122, the owner of copyright under this title has the exclusive rights to do and to authorize any of the following: (1) to reproduce the copyrighted work in copies or phonorecords; (2) to prepare derivative works based upon the copyrighted work; (3) to distribute copies or phonorecords of the copyrighted work to the public by sale or other transfer of ownership."
            },
            {
                "section_number": "107",
                "title": "Limitations on exclusive rights: Fair use",
                "text": "Notwithstanding the provisions of sections 106 and 106A, the fair use of a copyrighted work, including such use by reproduction in copies or phonorecords or by any other means specified by that section, for purposes such as criticism, comment, news reporting, teaching, scholarship, or research, is not an infringement of copyright."
            }
        ]
    },
    {
        "act_id": "US_DMCA_1998",
        "act_title": "Digital Millennium Copyright Act of 1998 (Pub. L. 105-304)",
        "short_title": "DMCA 1998",
        "year": 1998,
        "act_number": "Pub. L. 105-304 (112 Stat. 2860)",
        "enactment_date": "28-Oct-1998",
        "official_url": "https://www.congress.gov/bill/105th-congress/house-bill/2281",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "dmca",
            "digital millennium copyright act",
            "17 usc 512"
        ],
        "sections": [
            {
                "section_number": "512",
                "title": "Limitations on liability relating to material online (Safe Harbor)",
                "text": "A service provider shall not be liable for monetary relief, or, except as provided in subsection (j), for injunctive or other equitable relief, for infringement of copyright by reason of the storage at the direction of a user of material that resides on a system or network controlled or operated by or for the service provider, if the service provider responds expeditiously to remove or disable access to material claimed to be infringing."
            },
            {
                "section_number": "1201",
                "title": "Circumvention of copyright protection systems",
                "text": "No person shall circumvent a technological measure that effectively controls access to a work protected under this title. No person shall manufacture, import, offer to the public, provide, or otherwise traffic in any technology, product, service, device, component, or part thereof that is primarily designed or produced for the purpose of circumventing protection."
            }
        ]
    },
    {
        "act_id": "US_PATENT_TITLE_35",
        "act_title": "United States Code Title 35 \u2014 Patents (Patent Act)",
        "short_title": "Title 35 U.S.C. Patents",
        "year": 1952,
        "act_number": "Pub. L. 82-593 (Title 35 U.S.C.)",
        "enactment_date": "19-Jul-1952",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title35&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "patent act",
            "title 35",
            "35 usc",
            "35 u.s.c.",
            "patent laws"
        ],
        "sections": [
            {
                "section_number": "101",
                "title": "Inventions patentable",
                "text": "Whoever invents or discovers any new and useful process, machine, manufacture, or composition of matter, or any new and useful improvement thereof, may obtain a patent therefor, subject to the conditions and requirements of this title."
            },
            {
                "section_number": "102",
                "title": "Conditions for patentability; novelty",
                "text": "A person shall be entitled to a patent unless the claimed invention was patented, described in a printed publication, or in public use, on sale, or otherwise available to the public before the effective filing date of the claimed invention."
            },
            {
                "section_number": "103",
                "title": "Conditions for patentability; non-obvious subject matter",
                "text": "A patent for a claimed invention may not be obtained, notwithstanding that the claimed invention is not identically disclosed as set forth in section 102, if the differences between the claimed invention and the prior art are such that the claimed invention as a whole would have been obvious before the effective filing date of the claimed invention to a person having ordinary skill in the art to which the claimed invention pertains."
            },
            {
                "section_number": "271",
                "title": "Infringement of patent",
                "text": "Except as otherwise provided in this title, whoever without authority makes, uses, offers to sell, or sells any patented invention, within the United States or imports into the United States any patented invention during the term of the patent therefor, infringes the patent."
            }
        ]
    },
    {
        "act_id": "US_LANHAM_ACT_1946",
        "act_title": "Lanham Trademark Act (Title 15 U.S.C. Section 1051 et seq.)",
        "short_title": "Lanham Act (Trademarks)",
        "year": 1946,
        "act_number": "Pub. L. 79-489 (60 Stat. 427)",
        "enactment_date": "05-Jul-1946",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title15/chapter22&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "lanham act",
            "trademark act",
            "15 usc 1114",
            "15 usc 1125"
        ],
        "sections": [
            {
                "section_number": "32",
                "title": "Remedies; infringement of registered marks",
                "text": "Any person who shall, without the consent of the registrant, use in commerce any reproduction, counterfeit, copy, or colorable imitation of a registered mark in connection with the sale, offering for sale, distribution, or advertising of any goods or services on or in connection with which such use is likely to cause confusion, or to cause mistake, or to deceive, shall be liable in a civil action."
            },
            {
                "section_number": "43(a)",
                "title": "False designations of origin and false descriptions forbidden",
                "text": "Any person who, on or in connection with any goods or services, uses in commerce any word, term, name, symbol, or device, or any false designation of origin, false or misleading description of fact, or false or misleading representation of fact, which is likely to cause confusion as to the affiliation, connection, or association of such person with another person, shall be liable in a civil action."
            }
        ]
    },
    {
        "act_id": "US_BANKRUPTCY_TITLE_11",
        "act_title": "United States Code Title 11 \u2014 Bankruptcy (Bankruptcy Code)",
        "short_title": "Title 11 U.S.C. Bankruptcy Code",
        "year": 1978,
        "act_number": "Pub. L. 95-598 (Title 11 U.S.C.)",
        "enactment_date": "06-Nov-1978",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title11&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "bankruptcy code",
            "title 11",
            "11 usc",
            "11 u.s.c.",
            "chapter 11",
            "chapter 7"
        ],
        "sections": [
            {
                "section_number": "362",
                "title": "Automatic stay",
                "text": "Except as provided in subsection (b) of this section, a petition filed under section 301, 302, or 303 of this title operates as a stay, applicable to all entities, of the commencement or continuation of a judicial, administrative, or other action or proceeding against the debtor that was or could have been commenced before the commencement of the case."
            },
            {
                "section_number": "727",
                "title": "Discharge",
                "text": "The court shall grant the debtor a discharge, unless the debtor is not an individual; the debtor, with intent to hinder, delay, or defraud a creditor or an officer of the estate charged with custody of property under this title, has transferred, removed, destroyed, mutilated, or concealed property of the debtor."
            },
            {
                "section_number": "1129",
                "title": "Confirmation of plan",
                "text": "The court shall confirm a plan only if all of the following requirements are met: The plan complies with the applicable provisions of this title. The proponent of the plan complies with the applicable provisions of this title. The plan has been proposed in good faith and not by any means forbidden by law."
            }
        ]
    },
    {
        "act_id": "US_ADA_1990",
        "act_title": "Americans with Disabilities Act of 1990 (Title 42 U.S.C. Section 12101 et seq.)",
        "short_title": "Americans with Disabilities Act (ADA)",
        "year": 1990,
        "act_number": "Pub. L. 101-336 (Title 42 U.S.C.)",
        "enactment_date": "26-Jul-1990",
        "official_url": "https://www.congress.gov/bill/101st-congress/senate-bill/933",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "ada",
            "americans with disabilities act",
            "ada 1990",
            "42 usc 12101"
        ],
        "sections": [
            {
                "section_number": "102",
                "title": "Discrimination prohibition in employment",
                "text": "No covered entity shall discriminate against a qualified individual on the basis of disability in regard to job application procedures, the hiring, advancement, or discharge of employees, employee compensation, job training, and other terms, conditions, and privileges of employment."
            },
            {
                "section_number": "302",
                "title": "Prohibition of discrimination by public accommodations",
                "text": "No individual shall be discriminated against on the basis of disability in the full and equal enjoyment of the goods, services, facilities, privileges, advantages, or accommodations of any place of public accommodation by any person who owns, leases, or operates a place of public accommodation."
            }
        ]
    },
    {
        "act_id": "US_FOIA_1966",
        "act_title": "Freedom of Information Act (5 U.S.C. Section 552)",
        "short_title": "Freedom of Information Act (FOIA)",
        "year": 1966,
        "act_number": "Pub. L. 89-487 (Title 5 U.S.C.)",
        "enactment_date": "04-Jul-1966",
        "official_url": "https://www.congress.gov/bill/89th-congress/senate-bill/1160",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "foia",
            "freedom of information act",
            "5 usc 552"
        ],
        "sections": [
            {
                "section_number": "552",
                "title": "Public information; agency rules, opinions, orders, records, and proceedings",
                "text": "Each agency shall make available to the public information as follows: Each agency shall separately state and currently publish in the Federal Register for the guidance of the public descriptions of its central and field organization and the established places at which the public may obtain information."
            }
        ]
    },
    {
        "act_id": "US_APA_1946",
        "act_title": "Administrative Procedure Act (Title 5 U.S.C. Section 551 et seq.)",
        "short_title": "Administrative Procedure Act (APA)",
        "year": 1946,
        "act_number": "Pub. L. 79-404 (Title 5 U.S.C.)",
        "enactment_date": "11-Jun-1946",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title5/part1/chapter5&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "apa",
            "administrative procedure act",
            "5 usc 551",
            "5 usc 706"
        ],
        "sections": [
            {
                "section_number": "553",
                "title": "Rule making",
                "text": "General notice of proposed rule making shall be published in the Federal Register, unless all persons subject thereto are named and either personally served or otherwise have actual notice thereof in accordance with law. The notice shall include a statement of the time, place, and nature of public rule making proceedings."
            },
            {
                "section_number": "706",
                "title": "Scope of review",
                "text": "To the extent necessary to decision and when presented, the reviewing court shall decide all relevant questions of law, interpret constitutional and statutory provisions, and determine the meaning or applicability of the terms of an agency action. The reviewing court shall hold unlawful and set aside agency action, findings, and conclusions found to be arbitrary, capricious, an abuse of discretion, or otherwise not in accordance with law."
            }
        ]
    },
    {
        "act_id": "US_FLSA_1938",
        "act_title": "Fair Labor Standards Act of 1938 (Title 29 U.S.C. Section 201 et seq.)",
        "short_title": "Fair Labor Standards Act (FLSA)",
        "year": 1938,
        "act_number": "Pub. L. 75-718 (52 Stat. 1060)",
        "enactment_date": "25-Jun-1938",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title29/chapter8&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "flsa",
            "fair labor standards act",
            "29 usc 201",
            "minimum wage act"
        ],
        "sections": [
            {
                "section_number": "6",
                "title": "Minimum wage",
                "text": "Every employer shall pay to each of his employees who in any workweek is engaged in commerce or in the production of goods for commerce, wages at the following rates: not less than the statutory minimum hourly wage established under federal law."
            },
            {
                "section_number": "7",
                "title": "Maximum hours and overtime compensation",
                "text": "Except as otherwise provided in this section, no employer shall employ any of his employees who in any workweek is engaged in commerce or in the production of goods for commerce, for a workweek longer than forty hours unless such employee receives compensation for his employment in excess of the hours above specified at a rate not less than one and one-half times the regular rate at which he is employed."
            }
        ]
    },
    {
        "act_id": "US_OSHA_1970",
        "act_title": "Occupational Safety and Health Act of 1970 (Title 29 U.S.C. Section 651 et seq.)",
        "short_title": "OSHA 1970",
        "year": 1970,
        "act_number": "Pub. L. 91-596 (84 Stat. 1590)",
        "enactment_date": "29-Dec-1970",
        "official_url": "https://www.congress.gov/bill/91st-congress/senate-bill/2193",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "osha",
            "occupational safety and health act",
            "29 usc 654"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Duties of employers and employees (General Duty Clause)",
                "text": "Each employer shall furnish to each of his employees employment and a place of employment which are free from recognized hazards that are causing or are likely to cause death or serious physical harm to his employees; and shall comply with occupational safety and health standards promulgated under this Act."
            }
        ]
    },
    {
        "act_id": "US_ERISA_1974",
        "act_title": "Employee Retirement Income Security Act of 1974 (Title 29 U.S.C. Section 1001 et seq.)",
        "short_title": "ERISA 1974",
        "year": 1974,
        "act_number": "Pub. L. 93-406 (88 Stat. 829)",
        "enactment_date": "02-Sep-1974",
        "official_url": "https://www.congress.gov/bill/93rd-congress/house-bill/2",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "erisa",
            "employee retirement income security act",
            "29 usc 1104"
        ],
        "sections": [
            {
                "section_number": "404",
                "title": "Fiduciary duties under employee benefit plans",
                "text": "A fiduciary shall discharge his duties with respect to a plan solely in the interest of the participants and beneficiaries and for the exclusive purpose of providing benefits to participants and their beneficiaries; and defraying reasonable expenses of administering the plan with the care, skill, prudence, and diligence under the circumstances then prevailing."
            }
        ]
    },
    {
        "act_id": "US_CLEAN_AIR_1970",
        "act_title": "Clean Air Act (Title 42 U.S.C. Section 7401 et seq.)",
        "short_title": "Clean Air Act",
        "year": 1970,
        "act_number": "Pub. L. 91-604 (84 Stat. 1676)",
        "enactment_date": "31-Dec-1970",
        "official_url": "https://www.congress.gov/bill/91st-congress/house-bill/17255",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "clean air act",
            "caa",
            "42 usc 7401"
        ],
        "sections": [
            {
                "section_number": "109",
                "title": "National primary and secondary ambient air quality standards",
                "text": "The Administrator shall publish proposed regulations prescribing a national primary ambient air quality standard and a national secondary ambient air quality standard for each air pollutant for which air quality criteria have been issued prior to such date."
            },
            {
                "section_number": "111",
                "title": "Standards of performance for new stationary sources",
                "text": "The Administrator shall publish a list of categories of stationary sources. He shall include a category of sources in such list if in his judgment it causes, or contributes significantly to, air pollution which may reasonably be anticipated to endanger public health or welfare."
            }
        ]
    },
    {
        "act_id": "US_CLEAN_WATER_1972",
        "act_title": "Clean Water Act (Title 33 U.S.C. Section 1251 et seq.)",
        "short_title": "Clean Water Act",
        "year": 1972,
        "act_number": "Pub. L. 92-500 (86 Stat. 816)",
        "enactment_date": "18-Oct-1972",
        "official_url": "https://www.congress.gov/bill/92nd-congress/senate-bill/2770",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "clean water act",
            "cwa",
            "33 usc 1311",
            "federal water pollution control act"
        ],
        "sections": [
            {
                "section_number": "301",
                "title": "Effluent limitations",
                "text": "Except as in compliance with this section and sections 302, 306, 307, 318, 402, and 404 of this Act, the discharge of any pollutant by any person shall be unlawful."
            },
            {
                "section_number": "404",
                "title": "Permits for dredged or fill material",
                "text": "The Secretary may issue permits, after notice and opportunity for public hearings for the discharge of dredged or fill material into the navigable waters at specified disposal sites."
            }
        ]
    },
    {
        "act_id": "US_CERCLA_1980",
        "act_title": "Comprehensive Environmental Response, Compensation, and Liability Act (Superfund)",
        "short_title": "CERCLA (Superfund)",
        "year": 1980,
        "act_number": "Pub. L. 96-510 (94 Stat. 2767)",
        "enactment_date": "11-Dec-1980",
        "official_url": "https://www.congress.gov/bill/96th-congress/house-bill/7020",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "cercla",
            "superfund",
            "42 usc 9607"
        ],
        "sections": [
            {
                "section_number": "107",
                "title": "Liability for release of hazardous substances",
                "text": "Notwithstanding any other provision or rule of law, and subject only to the defenses set forth in subsection (b) of this section, the owner and operator of a vessel or a facility, any person who at the time of disposal of any hazardous substance owned or operated any facility at which such hazardous substances were disposed of, shall be liable for all costs of removal or remedial action."
            }
        ]
    },
    {
        "act_id": "US_FDCA_1938",
        "act_title": "Federal Food, Drug, and Cosmetic Act (Title 21 U.S.C. Section 301 et seq.)",
        "short_title": "FD&C Act",
        "year": 1938,
        "act_number": "Pub. L. 75-717 (52 Stat. 1040)",
        "enactment_date": "25-Jun-1938",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title21/chapter9&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "fdca",
            "fd&c act",
            "food drug and cosmetic act",
            "21 usc 331"
        ],
        "sections": [
            {
                "section_number": "301",
                "title": "Prohibited acts",
                "text": "The following acts and the causing thereof are hereby prohibited: The introduction or delivery for introduction into interstate commerce of any food, drug, device, tobacco product, or cosmetic that is adulterated or misbranded."
            },
            {
                "section_number": "505",
                "title": "New drugs",
                "text": "No person shall introduce or deliver for introduction into interstate commerce any new drug, unless an approval of an application filed pursuant to subsection (b) or (j) is effective with respect to such drug."
            }
        ]
    },
    {
        "act_id": "US_CSA_1970",
        "act_title": "Controlled Substances Act (Title 21 U.S.C. Section 801 et seq.)",
        "short_title": "Controlled Substances Act (CSA)",
        "year": 1970,
        "act_number": "Pub. L. 91-513 (84 Stat. 1242)",
        "enactment_date": "27-Oct-1970",
        "official_url": "https://www.congress.gov/bill/91st-congress/house-bill/18583",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "controlled substances act",
            "csa",
            "21 usc 841"
        ],
        "sections": [
            {
                "section_number": "401",
                "title": "Prohibited acts A; penalties for manufacturing, distributing, or dispensing",
                "text": "Except as authorized by this subchapter, it shall be unlawful for any person knowingly or intentionally to manufacture, distribute, or dispense, or possess with intent to manufacture, distribute, or dispense, a controlled substance; or to create, distribute, or dispense, or possess with intent to distribute or dispense, a counterfeit substance."
            }
        ]
    },
    {
        "act_id": "US_FALSE_CLAIMS_1863",
        "act_title": "False Claims Act (Title 31 U.S.C. Section 3729 et seq.)",
        "short_title": "False Claims Act (FCA)",
        "year": 1863,
        "act_number": "12 Stat. 696 (Title 31 U.S.C.)",
        "enactment_date": "02-Mar-1863",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title31/subtitleIII/chapter37/subchapterIII&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "false claims act",
            "fca",
            "31 usc 3729",
            "lincoln law"
        ],
        "sections": [
            {
                "section_number": "3729",
                "title": "False claims liability; treble damages",
                "text": "Any person who knowingly presents, or causes to be presented, a false or fraudulent claim for payment or approval; or knowingly makes, uses, or causes to be made or used, a false record or statement material to a false or fraudulent claim, is liable to the United States Government for a civil penalty plus 3 times the amount of damages which the Government sustains."
            }
        ]
    },
    {
        "act_id": "US_BANK_SECRECY_1970",
        "act_title": "Bank Secrecy Act (Currency and Foreign Transactions Reporting Act, Title 31 U.S.C.)",
        "short_title": "Bank Secrecy Act (BSA)",
        "year": 1970,
        "act_number": "Pub. L. 91-508 (84 Stat. 1118)",
        "enactment_date": "26-Oct-1970",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title31/subtitleIV/chapter53/subchapterII&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "bank secrecy act",
            "bsa 1970",
            "31 usc 5313",
            "anti-money laundering act"
        ],
        "sections": [
            {
                "section_number": "5313",
                "title": "Reports on domestic coins and currency transactions",
                "text": "When a domestic financial institution is involved in a transaction for the payment, receipt, or transfer of United States coins or currency, in an amount, denomination, or amount and denomination, or under circumstances the Secretary prescribes by regulation, the institution and any other participant in the transaction the Secretary may prescribe shall file a report on the transaction at the time and in the way the Secretary prescribes."
            }
        ]
    },
    {
        "act_id": "US_DODD_FRANK_2010",
        "act_title": "Dodd-Frank Wall Street Reform and Consumer Protection Act (Pub. L. 111-203)",
        "short_title": "Dodd-Frank Act",
        "year": 2010,
        "act_number": "Pub. L. 111-203 (124 Stat. 1376)",
        "enactment_date": "21-Jul-2010",
        "official_url": "https://www.congress.gov/bill/111th-congress/house-bill/4173",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "dodd-frank",
            "dodd-frank act",
            "wall street reform"
        ],
        "sections": [
            {
                "section_number": "1021",
                "title": "Purpose and objectives of Consumer Financial Protection Bureau",
                "text": "The Bureau shall seek to implement and, where applicable, enforce Federal consumer financial law consistently for the purpose of ensuring that all consumers have access to fair, transparent, and competitive financial markets."
            },
            {
                "section_number": "1031",
                "title": "Prohibiting unfair, deceptive, or abusive acts or practices",
                "text": "The Bureau may take any action authorized under subtitle E to prevent a covered person or service provider from committing or engaging in an unfair, deceptive, or abusive act or practice under Federal law in connection with any transaction with a consumer for a consumer financial product or service."
            }
        ]
    },
    {
        "act_id": "US_COMMUNICATIONS_1934",
        "act_title": "Communications Act of 1934 & Communications Decency Act Section 230",
        "short_title": "Communications Act / Section 230",
        "year": 1934,
        "act_number": "48 Stat. 1064 (Title 47 U.S.C.)",
        "enactment_date": "19-Jun-1934",
        "official_url": "https://uscode.house.gov/view.xhtml?path=/prelim@title47/chapter5&edition=prelim",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "section 230",
            "cda 230",
            "communications act",
            "47 usc 230"
        ],
        "sections": [
            {
                "section_number": "230",
                "title": "Protection for private blocking and screening of offensive material (Section 230)",
                "text": "No provider or user of an interactive computer service shall be treated as the publisher or speaker of any information provided by another information content provider. No provider or user of an interactive computer service shall be held liable on account of any action voluntarily taken in good faith to restrict access to or availability of material that the provider or user considers to be obscene, lewd, lascivious, filthy, excessively violent, harassing, or otherwise objectionable."
            }
        ]
    },
    {
        "act_id": "US_HIPAA_1996",
        "act_title": "Health Insurance Portability and Accountability Act of 1996 (Pub. L. 104-191)",
        "short_title": "HIPAA 1996",
        "year": 1996,
        "act_number": "Pub. L. 104-191 (110 Stat. 1936)",
        "enactment_date": "21-Aug-1996",
        "official_url": "https://www.congress.gov/bill/104th-congress/house-bill/3103",
        "legislation_portal": "https://www.congress.gov",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.uscourts.gov",
        "aliases": [
            "hipaa",
            "health insurance portability and accountability act",
            "42 usc 1320d"
        ],
        "sections": [
            {
                "section_number": "1173",
                "title": "Standards for information transactions and data elements",
                "text": "The Secretary shall adopt standards for transactions, and data elements for such transactions, to enable health information to be exchanged electronically, that are appropriate for the financial and administrative transactions."
            },
            {
                "section_number": "1177",
                "title": "Wrongful disclosure of individually identifiable health information",
                "text": "A person who knowingly uses or causes to be used a unique health identifier, obtains individually identifiable health information relating to an individual, or discloses individually identifiable health information to another person, shall be punished as provided in subsection (b)."
            }
        ]
    }
]

UK_CORPUS = [
    {
        "act_id": "UK_THEFT_1968",
        "act_title": "Theft Act 1968 (c. 60)",
        "short_title": "Theft Act 1968",
        "year": 1968,
        "act_number": "1968 c. 60",
        "enactment_date": "26-Jul-1968",
        "official_url": "https://www.legislation.gov.uk/ukpga/1968/60/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "theft act",
            "theft act 1968",
            "uk theft act"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Basic definition of theft",
                "text": "A person is guilty of theft if he dishonestly appropriates property belonging to another with the intention of permanently depriving the other of it; and 'thief' and 'steal' shall be construed accordingly."
            },
            {
                "section_number": "2",
                "title": "'Dishonestly'",
                "text": "A person's appropriation of property belonging to another is not to be regarded as dishonest if he appropriates the property in the belief that he has in law the right to deprive the other of it, or in the belief that he would have the other's consent if the other knew of the appropriation and the circumstances of it."
            },
            {
                "section_number": "3",
                "title": "'Appropriates'",
                "text": "Any assumption by a person of the rights of an owner amounts to an appropriation, and this includes, where he has come by the property (innocently or not) without stealing it, any later assumption of a right to it by keeping or dealing with it as owner."
            },
            {
                "section_number": "7",
                "title": "Theft (Penalty)",
                "text": "A person guilty of theft shall on conviction on indictment be liable to imprisonment for a term not exceeding seven years."
            },
            {
                "section_number": "8",
                "title": "Robbery",
                "text": "A person is guilty of robbery if he steals, and immediately before or at the time of doing so, and in order to do so, he uses force on any person or puts or seeks to put any person in fear of being then and there subjected to force."
            },
            {
                "section_number": "9",
                "title": "Burglary",
                "text": "A person is guilty of burglary if he enters any building or part of a building as a trespasser and with intent to commit any such offence as is mentioned in subsection (2) below; or having entered any building or part of a building as a trespasser he steals or attempts to steal anything in the building or that part of it or inflicts or attempts to inflict on any person therein any grievous bodily harm."
            }
        ]
    },
    {
        "act_id": "UK_THEFT_1978",
        "act_title": "Theft Act 1978 (c. 31)",
        "short_title": "Theft Act 1978",
        "year": 1978,
        "act_number": "1978 c. 31",
        "enactment_date": "20-Jul-1978",
        "official_url": "https://www.legislation.gov.uk/ukpga/1978/31/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "theft act 1978",
            "making off without payment"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Making off without payment",
                "text": "A person who, knowing that payment on the spot for any goods supplied or service done is required or expected from him, dishonestly makes off without having paid as required or expected and with intent to avoid payment of the amount due shall be guilty of an offence."
            }
        ]
    },
    {
        "act_id": "UK_FRAUD_2006",
        "act_title": "Fraud Act 2006 (c. 35)",
        "short_title": "Fraud Act 2006",
        "year": 2006,
        "act_number": "2006 c. 35",
        "enactment_date": "08-Nov-2006",
        "official_url": "https://www.legislation.gov.uk/ukpga/2006/35/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "fraud act",
            "fraud act 2006",
            "uk fraud act"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Fraud",
                "text": "A person is guilty of fraud if he is in breach of any of the sections listed in subsection (2) (which provide for different ways of committing the offence): section 2 (fraud by false representation), section 3 (fraud by failing to disclose information), and section 4 (fraud by abuse of position)."
            },
            {
                "section_number": "2",
                "title": "Fraud by false representation",
                "text": "A person is in breach of this section if he dishonestly makes a false representation, and intends, by making the representation to make a gain for himself or another, or to cause loss to another or to expose another to a risk of loss."
            },
            {
                "section_number": "3",
                "title": "Fraud by failing to disclose information",
                "text": "A person is in breach of this section if he dishonestly fails to disclose to another person information which he is under a legal duty to disclose, and intends, by failing to disclose the information to make a gain for himself or another, or to cause loss to another."
            },
            {
                "section_number": "4",
                "title": "Fraud by abuse of position",
                "text": "A person is in breach of this section if he occupies a position in which he is expected to safeguard, or not to act against, the financial interests of another person, dishonestly abuses that position, and intends, by means of the abuse of that position, to make a gain for himself or another, or to cause loss to another."
            }
        ]
    },
    {
        "act_id": "UK_FORGERY_1981",
        "act_title": "Forgery and Counterfeiting Act 1981 (c. 45)",
        "short_title": "Forgery and Counterfeiting Act 1981",
        "year": 1981,
        "act_number": "1981 c. 45",
        "enactment_date": "27-Jul-1981",
        "official_url": "https://www.legislation.gov.uk/ukpga/1981/45/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "forgery act",
            "forgery and counterfeiting act 1981"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "The offence of forgery",
                "text": "A person is guilty of forgery if he makes a false instrument, with the intention that he or another shall use it to induce somebody to accept it as genuine, and by reason of so accepting it to do or not to do some act to his own or any other person's prejudice."
            }
        ]
    },
    {
        "act_id": "UK_PACE_1984",
        "act_title": "Police and Criminal Evidence Act 1984 (c. 60)",
        "short_title": "PACE 1984",
        "year": 1984,
        "act_number": "1984 c. 60",
        "enactment_date": "31-Oct-1984",
        "official_url": "https://www.legislation.gov.uk/ukpga/1984/60/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "pace",
            "pace 1984",
            "police and criminal evidence act"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Power of constable to stop and search persons, vehicles etc",
                "text": "A constable may exercise any power conferred by this section\u2014in any place to which at the time when he proposes to exercise the power the public or any section of the public has access, on payment or otherwise; and he may search any person or vehicle for stolen or prohibited articles."
            },
            {
                "section_number": "24",
                "title": "Arrest without warrant: constables",
                "text": "A constable may arrest without a warrant anyone who is in the act of committing an offence or whom the constable has reasonable grounds for suspecting to be in the act of committing an offence, or anyone whom the constable has reasonable grounds to suspect of being guilty of an offence."
            },
            {
                "section_number": "56",
                "title": "Right to have someone informed when arrested",
                "text": "Where a person has been arrested and is being held in custody in a police station or other premises, he shall be entitled, if he so requests, to have one friend or relative or other person told, without delay or, where some delay is necessary in the permitted circumstances, with no more delay than is so necessary, that he has been arrested."
            },
            {
                "section_number": "58",
                "title": "Access to legal advice",
                "text": "A person arrested and held in custody in a police station or other premises shall be entitled, if he so requests, to consult a solicitor privately at any time. A request under subsection (1) above and the time at which it was made shall be recorded in the custody record."
            }
        ]
    },
    {
        "act_id": "UK_CRIMINAL_JUSTICE_2003",
        "act_title": "Criminal Justice Act 2003 (c. 44)",
        "short_title": "Criminal Justice Act 2003",
        "year": 2003,
        "act_number": "2003 c. 44",
        "enactment_date": "20-Nov-2003",
        "official_url": "https://www.legislation.gov.uk/ukpga/2003/44/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "criminal justice act 2003",
            "cja 2003"
        ],
        "sections": [
            {
                "section_number": "98",
                "title": "'Bad character' evidence",
                "text": "References in this Chapter to evidence of a person's bad character are to evidence of, or of a disposition towards, misconduct on his part, other than evidence which has to do with the alleged facts of the offence with which the defendant is charged."
            },
            {
                "section_number": "142",
                "title": "Purposes of sentencing",
                "text": "Any court sentencing an offender is to have regard to the following purposes of sentencing: the punishment of offenders, the reduction of crime (including its reduction by deterrence), the reform and rehabilitation of offenders, the protection of the public, and the making of reparation by offenders to persons affected by their offences."
            }
        ]
    },
    {
        "act_id": "UK_HUMAN_RIGHTS_1998",
        "act_title": "Human Rights Act 1998 (c. 42)",
        "short_title": "Human Rights Act 1998",
        "year": 1998,
        "act_number": "1998 c. 42",
        "enactment_date": "09-Nov-1998",
        "official_url": "https://www.legislation.gov.uk/ukpga/1998/42/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "human rights act",
            "human rights act 1998",
            "uk human rights act",
            "hra 1998"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Interpretation of legislation",
                "text": "So far as it is possible to do so, primary legislation and subordinate legislation must be read and given effect in a way which is compatible with the Convention rights. This section applies to primary legislation and subordinate legislation whenever enacted."
            },
            {
                "section_number": "6",
                "title": "Acts of public authorities",
                "text": "It is unlawful for a public authority to act in a way which is incompatible with a Convention right. Subsection (1) does not apply to an act if as the result of one or more provisions of primary legislation, the authority could not have acted differently."
            }
        ]
    },
    {
        "act_id": "UK_DATA_PROTECTION_2018",
        "act_title": "Data Protection Act 2018 (c. 12)",
        "short_title": "Data Protection Act 2018",
        "year": 2018,
        "act_number": "2018 c. 12",
        "enactment_date": "23-May-2018",
        "official_url": "https://www.legislation.gov.uk/ukpga/2018/12/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "data protection act 2018",
            "dpa 2018",
            "uk dpa",
            "uk gdpr"
        ],
        "sections": [
            {
                "section_number": "35",
                "title": "The first data protection principle (Law enforcement processing)",
                "text": "The first data protection principle is that the processing of personal data for any of the law enforcement purposes must be lawful and fair. The processing of personal data for any of the law enforcement purposes is lawful only if and to the extent that it is based on law and either the data subject has given consent or the processing is necessary for the performance of a task."
            },
            {
                "section_number": "86",
                "title": "Right of access (Intelligence services processing)",
                "text": "An individual is entitled to obtain from the controller confirmation as to whether or not personal data concerning him or her is being processed, and where that is the case, to access the personal data and the information set out in subsection (2)."
            }
        ]
    },
    {
        "act_id": "UK_CONTRACTS_1999",
        "act_title": "Contracts (Rights of Third Parties) Act 1999 (c. 31)",
        "short_title": "Contracts (Rights of Third Parties) Act 1999",
        "year": 1999,
        "act_number": "1999 c. 31",
        "enactment_date": "11-Nov-1999",
        "official_url": "https://www.legislation.gov.uk/ukpga/1999/31/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.gov",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "contracts rights of third parties",
            "contracts act 1999",
            "third party rights"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Right of third party to enforce contractual term",
                "text": "Subject to the provisions of this Act, a person who is not a party to a contract (a 'third party') may in his own right enforce a term of the contract if the contract expressly provides that he may, or subject to subsection (2), the term purports to confer a benefit on him."
            },
            {
                "section_number": "2",
                "title": "Variation and rescission of contract",
                "text": "Subject to this section, where a third party has a right under section 1 to enforce a term of the contract, the parties to the contract may not, by agreement, rescind the contract, or vary it in such a way as to extinguish or alter his entitlement under that right, without his consent."
            }
        ]
    },
    {
        "act_id": "UK_CONSUMER_2015",
        "act_title": "Consumer Rights Act 2015 (c. 15)",
        "short_title": "Consumer Rights Act 2015",
        "year": 2015,
        "act_number": "2015 c. 15",
        "enactment_date": "26-Mar-2015",
        "official_url": "https://www.legislation.gov.uk/ukpga/2015/15/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "consumer rights act",
            "consumer rights act 2015",
            "cra 2015"
        ],
        "sections": [
            {
                "section_number": "9",
                "title": "Goods to be of satisfactory quality",
                "text": "Every contract to supply goods is to be treated as including a term that the quality of the goods is satisfactory. The quality of goods is satisfactory if they meet the standard that a reasonable person would consider satisfactory, taking account of any description of the goods, the price and all other relevant circumstances."
            },
            {
                "section_number": "10",
                "title": "Goods to be fit for particular purpose",
                "text": "Subsection (3) applies to a contract to supply goods if before the contract is made the consumer makes known to the trader (expressly or by implication) any particular purpose for which the consumer is contracting for the goods. The contract is to be treated as including a term that the goods are reasonably fit for that purpose."
            },
            {
                "section_number": "20",
                "title": "Right to reject",
                "text": "The short-term right to reject is an entitlement of the consumer to reject the goods and treat the contract as at an end. The consumer exercises the right by indicating to the trader that the consumer rejects the goods and treats the contract as at an end."
            },
            {
                "section_number": "49",
                "title": "Service to be performed with reasonable care and skill",
                "text": "Every contract to supply a service is to be treated as including a term that the trader must perform the service with reasonable care and skill."
            }
        ]
    },
    {
        "act_id": "UK_SALE_OF_GOODS_1979",
        "act_title": "Sale of Goods Act 1979 (c. 54)",
        "short_title": "Sale of Goods Act 1979",
        "year": 1979,
        "act_number": "1979 c. 54",
        "enactment_date": "06-Dec-1979",
        "official_url": "https://www.legislation.gov.uk/ukpga/1979/54/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "sale of goods act",
            "sale of goods act 1979",
            "sga 1979"
        ],
        "sections": [
            {
                "section_number": "12",
                "title": "Implied terms about title, etc",
                "text": "In a contract of sale, other than one to which subsection (3) applies, there is an implied term on the part of the seller that in the case of a sale he has a right to sell the goods, and in the case of an agreement to sell he will have such a right at the time when the property is to pass."
            },
            {
                "section_number": "13",
                "title": "Sale by description",
                "text": "Where there is a contract for the sale of goods by description, there is an implied term that the goods will correspond with the description."
            },
            {
                "section_number": "14",
                "title": "Implied terms about quality or fitness",
                "text": "Except as provided by this section and section 15 below and subject to any other enactment, there is no implied term about the quality or fitness for any particular purpose of goods supplied under a contract of sale. Where the seller sells goods in the course of a business, there is an implied term that the goods supplied under the contract are of satisfactory quality."
            }
        ]
    },
    {
        "act_id": "UK_SUPPLY_OF_GOODS_1982",
        "act_title": "Supply of Goods and Services Act 1982 (c. 29)",
        "short_title": "Supply of Goods and Services Act 1982",
        "year": 1982,
        "act_number": "1982 c. 29",
        "enactment_date": "13-Jul-1982",
        "official_url": "https://www.legislation.gov.uk/ukpga/1982/29/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "supply of goods and services act",
            "sgsa 1982"
        ],
        "sections": [
            {
                "section_number": "13",
                "title": "Implied term about care and skill",
                "text": "In a relevant contract for the supply of a service where the supplier is acting in the course of a business, there is an implied term that the supplier will carry out the service with reasonable care and skill."
            }
        ]
    },
    {
        "act_id": "UK_UCTA_1977",
        "act_title": "Unfair Contract Terms Act 1977 (c. 50)",
        "short_title": "Unfair Contract Terms Act 1977",
        "year": 1977,
        "act_number": "1977 c. 50",
        "enactment_date": "26-Oct-1977",
        "official_url": "https://www.legislation.gov.uk/ukpga/1977/50/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "ucta",
            "unfair contract terms act",
            "ucta 1977"
        ],
        "sections": [
            {
                "section_number": "2",
                "title": "Negligence liability",
                "text": "A person cannot by reference to any contract term or to a notice given to persons generally or to particular persons exclude or restrict his liability for death or personal injury resulting from negligence. In the case of other loss or damage, a person cannot so exclude or restrict his liability for negligence except in so far as the term or notice satisfies the requirement of reasonableness."
            },
            {
                "section_number": "3",
                "title": "Liability arising in contract",
                "text": "This section applies as between contracting parties where one of them deals on the other's written standard terms of business. As against that party, the other cannot by reference to any contract term when himself in breach of contract, exclude or restrict any liability of his in respect of the breach except in so far as the contract term satisfies the requirement of reasonableness."
            }
        ]
    },
    {
        "act_id": "UK_COMPANIES_2006",
        "act_title": "Companies Act 2006 (c. 46)",
        "short_title": "Companies Act 2006",
        "year": 2006,
        "act_number": "2006 c. 46",
        "enactment_date": "08-Nov-2006",
        "official_url": "https://www.legislation.gov.uk/ukpga/2006/46/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "companies act",
            "companies act 2006",
            "uk companies act"
        ],
        "sections": [
            {
                "section_number": "171",
                "title": "Duty to act within powers",
                "text": "A director of a company must\u2014(a) act in accordance with the company's constitution, and (b) only exercise powers for the purposes for which they are conferred."
            },
            {
                "section_number": "172",
                "title": "Duty to promote the success of the company",
                "text": "A director of a company must act in the way he considers, in good faith, would be most likely to promote the success of the company for the benefit of its members as a whole, and in doing so have regard (amongst other matters) to the likely consequences of any decision in the long term, the interests of the company's employees, and the need to foster the company's business relationships with suppliers, customers and others."
            }
        ]
    },
    {
        "act_id": "UK_INSOLVENCY_1986",
        "act_title": "Insolvency Act 1986 (c. 45)",
        "short_title": "Insolvency Act 1986",
        "year": 1986,
        "act_number": "1986 c. 45",
        "enactment_date": "25-Jul-1986",
        "official_url": "https://www.legislation.gov.uk/ukpga/1986/45/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "insolvency act",
            "insolvency act 1986",
            "wrongful trading"
        ],
        "sections": [
            {
                "section_number": "122",
                "title": "Circumstances in which company may be wound up by the court",
                "text": "A company may be wound up by the court if the company has by special resolution resolved that the company be wound up by the court, or the company is unable to pay its debts, or the court is of the opinion that it is just and equitable that the company should be wound up."
            },
            {
                "section_number": "214",
                "title": "Wrongful trading",
                "text": "Subject to subsection (3) below, if in the course of the winding up of a company it appears that subsection (2) of this section applies in relation to a person who is or has been a director of the company, the court, on the application of the liquidator, may declare that that person is to be liable to make such contribution (if any) to the company's assets as the court thinks proper."
            }
        ]
    },
    {
        "act_id": "UK_PARTNERSHIP_1890",
        "act_title": "Partnership Act 1890 (c. 39)",
        "short_title": "Partnership Act 1890",
        "year": 1890,
        "act_number": "1890 c. 39",
        "enactment_date": "14-Aug-1890",
        "official_url": "https://www.legislation.gov.uk/ukpga/1890/39/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "partnership act",
            "partnership act 1890"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Definition of partnership",
                "text": "Partnership is the relation which subsists between persons carrying on a business in common with a view of profit."
            },
            {
                "section_number": "5",
                "title": "Power of partner to bind the firm",
                "text": "Every partner is an agent of the firm and his other partners for the purpose of the business of the partnership; and the acts of every partner who does any act for carrying on in the usual way business of the kind carried on by the firm bind the firm and his partners."
            }
        ]
    },
    {
        "act_id": "UK_LLP_2000",
        "act_title": "Limited Liability Partnerships Act 2000 (c. 12)",
        "short_title": "Limited Liability Partnerships Act 2000",
        "year": 2000,
        "act_number": "2000 c. 12",
        "enactment_date": "20-Jul-2000",
        "official_url": "https://www.legislation.gov.uk/ukpga/2000/12/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "llp act",
            "limited liability partnerships act 2000"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Limited liability partnerships",
                "text": "There shall be a new form of legal entity to be known as a limited liability partnership. A limited liability partnership is a body corporate (with legal personality separate from that of its members) which is formed by being incorporated under this Act."
            }
        ]
    },
    {
        "act_id": "UK_ARBITRATION_1996",
        "act_title": "Arbitration Act 1996 (c. 23)",
        "short_title": "Arbitration Act 1996",
        "year": 1996,
        "act_number": "1996 c. 23",
        "enactment_date": "17-Jun-1996",
        "official_url": "https://www.legislation.gov.uk/ukpga/1996/23/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "arbitration act 1996",
            "uk arbitration act"
        ],
        "sections": [
            {
                "section_number": "9",
                "title": "Stay of legal proceedings",
                "text": "A party to an arbitration agreement against whom legal proceedings are brought (whether by way of claim or counterclaim) in respect of a matter which under the agreement is to be referred to arbitration may (upon notice to the other parties to the proceedings) apply to the court in which the proceedings have been brought to stay the proceedings so far as they concern that matter."
            },
            {
                "section_number": "45",
                "title": "Determination of preliminary point of law",
                "text": "Unless otherwise agreed by the parties, the court may on the application of a party to arbitral proceedings (upon notice to the other parties) determine any question of law arising in the course of the proceedings which the court is satisfied substantially affects the rights of one or more of the parties."
            },
            {
                "section_number": "68",
                "title": "Challenging the award: serious irregularity",
                "text": "A party to arbitral proceedings may (upon notice to the other parties and to the tribunal) apply to the court challenging an award in the proceedings on the ground of serious irregularity affecting the tribunal, the proceedings or the award."
            }
        ]
    },
    {
        "act_id": "UK_EMPLOYMENT_RIGHTS_1996",
        "act_title": "Employment Rights Act 1996 (c. 18)",
        "short_title": "Employment Rights Act 1996",
        "year": 1996,
        "act_number": "1996 c. 18",
        "enactment_date": "22-May-1996",
        "official_url": "https://www.legislation.gov.uk/ukpga/1996/18/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "employment rights act",
            "era 1996",
            "unfair dismissal"
        ],
        "sections": [
            {
                "section_number": "94",
                "title": "The right not to be unfairly dismissed",
                "text": "An employee has the right not to be unfairly dismissed by his employer."
            },
            {
                "section_number": "98",
                "title": "General fairness of dismissal",
                "text": "In determining for the purposes of this Part whether the dismissal of an employee is fair or unfair, it is for the employer to show the reason (or, if more than one, the principal reason) for the dismissal, and that it is either a reason falling within subsection (2) or some other substantial reason of a kind such as to justify the dismissal of an employee holding the position which the employee held."
            }
        ]
    },
    {
        "act_id": "UK_EQUALITY_2010",
        "act_title": "Equality Act 2010 (c. 15)",
        "short_title": "Equality Act 2010",
        "year": 2010,
        "act_number": "2010 c. 15",
        "enactment_date": "08-Apr-2010",
        "official_url": "https://www.legislation.gov.uk/ukpga/2010/15/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "equality act",
            "equality act 2010",
            "uk equality act"
        ],
        "sections": [
            {
                "section_number": "4",
                "title": "The protected characteristics",
                "text": "The following characteristics are protected characteristics: age; disability; gender reassignment; marriage and civil partnership; pregnancy and maternity; race; religion or belief; sex; sexual orientation."
            },
            {
                "section_number": "13",
                "title": "Direct discrimination",
                "text": "A person (A) discriminates against another (B) if, because of a protected characteristic, A treats B less favourably than A treats or would treat others."
            },
            {
                "section_number": "19",
                "title": "Indirect discrimination",
                "text": "A person (A) discriminates against another (B) if A applies to B a provision, criterion or practice which is discriminatory in relation to a relevant protected characteristic of B's."
            }
        ]
    },
    {
        "act_id": "UK_BRIBERY_2010",
        "act_title": "Bribery Act 2010 (c. 23)",
        "short_title": "Bribery Act 2010",
        "year": 2010,
        "act_number": "2010 c. 23",
        "enactment_date": "08-Apr-2010",
        "official_url": "https://www.legislation.gov.uk/ukpga/2010/23/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "bribery act",
            "bribery act 2010",
            "uk bribery act"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Offences of bribing another person",
                "text": "A person ('P') is guilty of an offence if P offers, promises or gives a financial or other advantage to another person, and P intends the advantage to induce a person to perform improperly a relevant function or activity, or to reward a person for the improper performance of such a function or activity."
            },
            {
                "section_number": "2",
                "title": "Offences relating to being bribed",
                "text": "A person ('R') is guilty of an offence if R requests, agrees to receive or accepts a financial or other advantage intending that, in consequence, a relevant function or activity should be performed improperly (whether by R or another person)."
            },
            {
                "section_number": "7",
                "title": "Failure of commercial organisations to prevent bribery",
                "text": "A relevant commercial organisation ('C') is guilty of an offence under this section if a person ('A') associated with C bribes another person intending to obtain or retain business for C, or to obtain or retain an advantage in the conduct of business for C. But it is a defence for C to prove that C had in place adequate procedures designed to prevent persons associated with C from undertaking such conduct."
            }
        ]
    },
    {
        "act_id": "UK_POCA_2002",
        "act_title": "Proceeds of Crime Act 2002 (c. 29)",
        "short_title": "Proceeds of Crime Act 2002 (POCA)",
        "year": 2002,
        "act_number": "2002 c. 29",
        "enactment_date": "24-Jul-2002",
        "official_url": "https://www.legislation.gov.uk/ukpga/2002/29/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "poca",
            "proceeds of crime act",
            "money laundering uk"
        ],
        "sections": [
            {
                "section_number": "327",
                "title": "Concealing, disguising, converting, transferring criminal property",
                "text": "A person commits an offence if he conceals criminal property; disguises criminal property; converts criminal property; transfers criminal property; or removes criminal property from England and Wales or from Scotland or from Northern Ireland."
            },
            {
                "section_number": "328",
                "title": "Arrangements facilitating acquisition, retention, use or control of criminal property",
                "text": "A person commits an offence if he enters into or becomes concerned in an arrangement which he knows or suspects facilitates (by whatever means) the acquisition, retention, use or control of criminal property by or on behalf of another person."
            },
            {
                "section_number": "329",
                "title": "Acquisition, use and possession of criminal property",
                "text": "A person commits an offence if he acquires criminal property; uses criminal property; or has possession of criminal property."
            }
        ]
    },
    {
        "act_id": "UK_FSMA_2000",
        "act_title": "Financial Services and Markets Act 2000 (c. 8)",
        "short_title": "Financial Services and Markets Act 2000",
        "year": 2000,
        "act_number": "2000 c. 8",
        "enactment_date": "14-Jun-2000",
        "official_url": "https://www.legislation.gov.uk/ukpga/2000/8/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "fsma",
            "financial services and markets act",
            "fca regulations"
        ],
        "sections": [
            {
                "section_number": "19",
                "title": "The general prohibition against carrying on regulated activities without permission",
                "text": "No person may carry on a regulated activity in the United Kingdom, or purport to do so, unless he is an authorised person or an exempt person."
            },
            {
                "section_number": "89",
                "title": "Misleading statements",
                "text": "A person who makes a statement, promise or forecast which he knows to be misleading, false or deceptive in a material particular is guilty of an offence if he makes it for the purpose of inducing, or is reckless as to whether it may induce, another person to enter into or offer to enter into a relevant agreement."
            }
        ]
    },
    {
        "act_id": "UK_DEFAMATION_2013",
        "act_title": "Defamation Act 2013 (c. 26)",
        "short_title": "Defamation Act 2013",
        "year": 2013,
        "act_number": "2013 c. 26",
        "enactment_date": "25-Apr-2013",
        "official_url": "https://www.legislation.gov.uk/ukpga/2013/26/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "defamation act",
            "defamation act 2013",
            "libel act"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Serious harm requirement",
                "text": "A statement is not defamatory unless its publication has caused or is likely to cause serious harm to the reputation of the claimant. For the purposes of this section, harm to the reputation of a body that trades for profit is not 'serious harm' unless it has caused or is likely to cause the body serious financial loss."
            },
            {
                "section_number": "2",
                "title": "Truth defence",
                "text": "It is a defence to an action for defamation for the defendant to show that the imputation conveyed by the statement complained of is substantially true."
            }
        ]
    },
    {
        "act_id": "UK_ENV_PROTECTION_1990",
        "act_title": "Environmental Protection Act 1990 (c. 43)",
        "short_title": "Environmental Protection Act 1990",
        "year": 1990,
        "act_number": "1990 c. 43",
        "enactment_date": "01-Nov-1990",
        "official_url": "https://www.legislation.gov.uk/ukpga/1990/43/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "environmental protection act",
            "epa 1990"
        ],
        "sections": [
            {
                "section_number": "33",
                "title": "Prohibition on unauthorised or harmful depositing, treatment or disposal of waste",
                "text": "A person shall not deposit controlled waste, or knowingly cause or knowingly permit controlled waste to be deposited in or on any land unless an environmental permit authorising the deposit is in force and the deposit is in accordance with the licence."
            }
        ]
    },
    {
        "act_id": "UK_OFFICIAL_SECRETS_1989",
        "act_title": "Official Secrets Act 1989 (c. 6)",
        "short_title": "Official Secrets Act 1989",
        "year": 1989,
        "act_number": "1989 c. 6",
        "enactment_date": "11-May-1989",
        "official_url": "https://www.legislation.gov.uk/ukpga/1989/6/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "official secrets act",
            "osa 1989"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Security and intelligence",
                "text": "A person who is or has been a member of the security and intelligence services, or a person who has been notified that he is subject to this subsection, is guilty of an offence if without lawful authority he discloses any information, document or other article relating to security or intelligence."
            }
        ]
    },
    {
        "act_id": "UK_COMPUTER_MISUSE_1990",
        "act_title": "Computer Misuse Act 1990 (c. 18)",
        "short_title": "Computer Misuse Act 1990",
        "year": 1990,
        "act_number": "1990 c. 18",
        "enactment_date": "29-Jun-1990",
        "official_url": "https://www.legislation.gov.uk/ukpga/1990/18/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "computer misuse act",
            "cma 1990",
            "hacking offence uk"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Unauthorised access to computer material",
                "text": "A person is guilty of an offence if he causes a computer to perform any function with intent to secure access to any program or data held in any computer, the access he intends to secure is unauthorised, and he knows at the time when he causes the computer to perform the function that that is the case."
            },
            {
                "section_number": "3",
                "title": "Unauthorised acts with intent to impair, or with recklessness as to impairing, operation of computer, etc",
                "text": "A person is guilty of an offence if he does any unauthorised act in relation to a computer, at the time when he does the act he has the requisite intent or is reckless as to whether he causes any of the following: impairing the operation of any computer, preventing or hindering access to any program or data, or impairing the operation of any program or the reliability of data."
            }
        ]
    },
    {
        "act_id": "UK_ONLINE_SAFETY_2023",
        "act_title": "Online Safety Act 2023 (c. 50)",
        "short_title": "Online Safety Act 2023",
        "year": 2023,
        "act_number": "2023 c. 50",
        "enactment_date": "26-Oct-2023",
        "official_url": "https://www.legislation.gov.uk/ukpga/2023/50/contents",
        "legislation_portal": "https://www.legislation.gov.uk",
        "supreme_court_portal": "https://www.supremecourt.uk",
        "constitutional_court_portal": "https://www.judiciary.uk",
        "aliases": [
            "online safety act",
            "osa 2023",
            "uk online safety act"
        ],
        "sections": [
            {
                "section_number": "7",
                "title": "User-to-user services: illegal content risk assessment duties",
                "text": "A provider of a user-to-user service must carry out a suitable and sufficient illegal content risk assessment before beginning to operate the service in the United Kingdom."
            },
            {
                "section_number": "10",
                "title": "Safety duties about illegal content",
                "text": "A provider of a regulated service must take proportionate steps to mitigate and effectively manage the risks of harm to individuals in the United Kingdom presented by illegal content present on the service."
            }
        ]
    }
]

EU_CORPUS = [
    {
        "act_id": "EU_GDPR_2016",
        "act_title": "Regulation (EU) 2016/679 on General Data Protection (GDPR)",
        "short_title": "GDPR (EU 2016/679)",
        "year": 2016,
        "act_number": "Regulation (EU) 2016/679",
        "enactment_date": "27-Apr-2016",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "gdpr",
            "eu gdpr",
            "general data protection regulation",
            "regulation 2016/679"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Principles relating to processing of personal data",
                "text": "Personal data shall be processed lawfully, fairly and in a transparent manner in relation to the data subject; collected for specified, explicit and legitimate purposes; adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed; accurate and, where necessary, kept up to date."
            },
            {
                "section_number": "6",
                "title": "Lawfulness of processing",
                "text": "Processing shall be lawful only if and to the extent that at least one of the following applies: the data subject has given consent to the processing of his or her personal data for one or more specific purposes; processing is necessary for the performance of a contract; processing is necessary for compliance with a legal obligation."
            },
            {
                "section_number": "17",
                "title": "Right to erasure ('right to be forgotten')",
                "text": "The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed."
            },
            {
                "section_number": "83",
                "title": "General conditions for imposing administrative fines",
                "text": "Each supervisory authority shall ensure that the imposition of administrative fines pursuant to this Article in respect of infringements of this Regulation referred to in paragraphs 4, 5 and 6 shall in each individual case be effective, proportionate and dissuasive, reaching up to 20,000,000 EUR or 4% of total global annual turnover."
            }
        ]
    },
    {
        "act_id": "EU_AI_ACT_2024",
        "act_title": "Regulation (EU) 2024/1689 laying down Harmonised Rules on Artificial Intelligence (EU AI Act)",
        "short_title": "EU AI Act (2024/1689)",
        "year": 2024,
        "act_number": "Regulation (EU) 2024/1689",
        "enactment_date": "13-Jun-2024",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "ai act",
            "eu ai act",
            "regulation 2024/1689",
            "artificial intelligence act"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Prohibited Artificial Intelligence Practices",
                "text": "The following AI practices shall be prohibited: the placing on the market, the putting into service or the use of an AI system that deploys subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques; AI systems creating social scoring; and biometric categorisation systems that deduce political or religious beliefs."
            },
            {
                "section_number": "6",
                "title": "Classification rules for high-risk AI systems",
                "text": "Irrespective of whether an AI system is placed on the market or put into service independently from the products referred to in points (a) and (b), that AI system shall be considered high-risk where both of the following conditions are fulfilled: the AI system is intended to be used as a safety component of a product, or the AI system is itself a product covered by the Union harmonisation legislation listed in Annex I."
            },
            {
                "section_number": "9",
                "title": "Risk management system for high-risk AI systems",
                "text": "A risk management system shall be established, implemented, documented and maintained in relation to high-risk AI systems. The risk management system shall be understood as a continuous iterative process planned and run throughout the entire lifecycle of a high-risk AI system."
            },
            {
                "section_number": "14",
                "title": "Human oversight of high-risk AI systems",
                "text": "High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during the period in which the AI system is in use, enabling them to prevent or minimise risks to health, safety or fundamental rights."
            },
            {
                "section_number": "50",
                "title": "Transparency obligations for providers and deployers of certain AI systems",
                "text": "Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious from the points of view of reasonable natural persons."
            }
        ]
    },
    {
        "act_id": "EU_DSA_2022",
        "act_title": "Regulation (EU) 2022/2065 on a Single Market For Digital Services (Digital Services Act)",
        "short_title": "Digital Services Act (DSA)",
        "year": 2022,
        "act_number": "Regulation (EU) 2022/2065",
        "enactment_date": "19-Oct-2022",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2022/2065/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "dsa",
            "digital services act",
            "regulation 2022/2065"
        ],
        "sections": [
            {
                "section_number": "6",
                "title": "Hosting liability exemption",
                "text": "Where an information society service is provided that consists of the storage of information provided by a recipient of the service, the service provider shall not be liable for the information stored at the request of a recipient of the service, on condition that the provider does not have actual knowledge of illegal activity or illegal content."
            },
            {
                "section_number": "16",
                "title": "Notice and action mechanisms",
                "text": "Providers of hosting services shall put mechanisms in place to allow any individual or entity to notify them of the presence on their service of specific items of information that the individual or entity considers to be illegal content."
            },
            {
                "section_number": "34",
                "title": "Risk assessment for very large online platforms",
                "text": "Providers of very large online platforms and of very large online search engines shall diligently identify, analyse and assess any systemic risks in the Union stemming from the design or functioning of their service and its related systems."
            }
        ]
    },
    {
        "act_id": "EU_DMA_2022",
        "act_title": "Regulation (EU) 2022/1925 on Contestable and Fair Markets in the Digital Sector (Digital Markets Act)",
        "short_title": "Digital Markets Act (DMA)",
        "year": 2022,
        "act_number": "Regulation (EU) 2022/1925",
        "enactment_date": "14-Sep-2022",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2022/1925/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "dma",
            "digital markets act",
            "regulation 2022/1925",
            "gatekeeper regulation"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Designation of gatekeepers",
                "text": "An undertaking shall be designated as a gatekeeper if: (a) it has a significant impact on the internal market; (b) it provides a core platform service which is an important gateway for business users to reach end users; and (c) it enjoys an entrenched and durable position."
            },
            {
                "section_number": "5",
                "title": "Obligations of gatekeepers on data combination and self-preferencing",
                "text": "The gatekeeper shall not process, for the purpose of providing online advertising services, personal data of end users using services of third parties that make use of core platform services of the gatekeeper, nor combine personal data from the relevant core platform service with personal data from any further core platform services."
            }
        ]
    },
    {
        "act_id": "EU_MICA_2023",
        "act_title": "Regulation (EU) 2023/1114 on Markets in Crypto-Assets (MiCA)",
        "short_title": "MiCA Regulation (2023/1114)",
        "year": 2023,
        "act_number": "Regulation (EU) 2023/1114",
        "enactment_date": "31-May-2023",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2023/1114/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "mica",
            "markets in crypto assets",
            "regulation 2023/1114",
            "crypto regulation eu"
        ],
        "sections": [
            {
                "section_number": "59",
                "title": "Requirements for authorization of crypto-asset service providers (CASPs)",
                "text": "Crypto-asset services shall only be provided by legal persons or other undertakings that have a registered office in a Member State where they carry out at least part of their crypto-asset services and that have been authorised as crypto-asset service providers in accordance with Article 63."
            },
            {
                "section_number": "88",
                "title": "Prohibition of market abuse relating to crypto-assets",
                "text": "This Title applies to acts carried out by any person concerning crypto-assets that are admitted to trading or for which a request for admission to trading has been made. It prohibits insider dealing, unlawful disclosure of inside information, and market manipulation."
            }
        ]
    },
    {
        "act_id": "EU_DGA_2022",
        "act_title": "Regulation (EU) 2022/868 on European Data Governance (Data Governance Act)",
        "short_title": "Data Governance Act (DGA)",
        "year": 2022,
        "act_number": "Regulation (EU) 2022/868",
        "enactment_date": "30-May-2022",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2022/868/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "dga",
            "data governance act",
            "regulation 2022/868"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Conditions for re-use of protected public sector data",
                "text": "Conditions for re-use shall be non-discriminatory, transparent, proportionate and objectively justified with regard to the categories of data and the purposes of re-use and the nature of the data for which re-use is allowed."
            }
        ]
    },
    {
        "act_id": "EU_DATA_ACT_2023",
        "act_title": "Regulation (EU) 2023/2854 on Harmonised Rules on Fair Access to and Use of Data (Data Act)",
        "short_title": "Data Act (Regulation 2023/2854)",
        "year": 2023,
        "act_number": "Regulation (EU) 2023/2854",
        "enactment_date": "13-Dec-2023",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2023/2854/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "data act",
            "eu data act",
            "regulation 2023/2854"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Obligation to make product data and related service data accessible to the user",
                "text": "Connected products shall be designed and manufactured, and related services shall be designed and provided, in such a manner that product data and related service data are, by default, easily, securely, free of charge and, where relevant and appropriate, directly accessible to the user."
            },
            {
                "section_number": "4",
                "title": "Rights and obligations of users and data holders to access, use and make available product data",
                "text": "Where data cannot be directly accessed by the user from the connected product or related service, data holders shall make readily available product data and related service data accessible to the user without undue delay, of the same quality as is available to the data holder, easily, securely, free of charge and, where relevant and appropriate, continuously and in real-time."
            }
        ]
    },
    {
        "act_id": "EU_CYBERSECURITY_2019",
        "act_title": "Regulation (EU) 2019/881 on ENISA and on Information and Communications Technology Cybersecurity Certification (Cybersecurity Act)",
        "short_title": "Cybersecurity Act (2019/881)",
        "year": 2019,
        "act_number": "Regulation (EU) 2019/881",
        "enactment_date": "17-Apr-2019",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2019/881/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "cybersecurity act",
            "enisa act",
            "regulation 2019/881"
        ],
        "sections": [
            {
                "section_number": "4",
                "title": "Mandate of ENISA",
                "text": "ENISA shall act as a reference point for advice and expertise on cybersecurity for Union institutions, bodies, offices and agencies as well as for other relevant Union stakeholders."
            },
            {
                "section_number": "49",
                "title": "European cybersecurity certification schemes",
                "text": "A European cybersecurity certification scheme shall attest that the ICT products, ICT services and ICT processes that have been evaluated in accordance with such scheme comply with specified security requirements with the objective of protecting the availability, authenticity, integrity or confidentiality of stored or transmitted or processed data."
            }
        ]
    },
    {
        "act_id": "EU_EIDAS_2024",
        "act_title": "Regulation (EU) 2024/1183 on European Digital Identity Framework (eIDAS 2)",
        "short_title": "eIDAS 2 (Regulation 2024/1183)",
        "year": 2024,
        "act_number": "Regulation (EU) 2024/1183",
        "enactment_date": "11-Apr-2024",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2024/1183/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "eidas",
            "eidas 2",
            "digital identity wallet",
            "regulation 2024/1183"
        ],
        "sections": [
            {
                "section_number": "5a",
                "title": "European Digital Identity Wallets",
                "text": "Member States shall provide at least one European Digital Identity Wallet within 24 months of the entry into force of the implementing acts. European Digital Identity Wallets shall enable the user to securely request and obtain, store, select, combine and share person identification data and electronic attestations of attributes."
            },
            {
                "section_number": "6",
                "title": "Mutual recognition of electronic identification means",
                "text": "An electronic identification means issued under a notified electronic identification scheme shall be recognized by all other Member States for the purpose of cross-border access to online public and private services."
            }
        ]
    },
    {
        "act_id": "EU_NIS2_DIR_2022",
        "act_title": "Directive (EU) 2022/2555 on Measures for a High Common Level of Cybersecurity Across the Union (NIS 2 Directive)",
        "short_title": "NIS 2 Directive (2022/2555)",
        "year": 2022,
        "act_number": "Directive (EU) 2022/2555",
        "enactment_date": "14-Dec-2022",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2022/2555/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "nis 2",
            "nis2",
            "directive 2022/2555",
            "network and information security directive"
        ],
        "sections": [
            {
                "section_number": "21",
                "title": "Cybersecurity risk-management measures",
                "text": "Member States shall ensure that essential and important entities take appropriate and proportionate technical, operational and organisational measures to manage the risks posed to the security of network and information systems which those entities use for their operations or for the provision of their services, and to prevent or minimise the impact of incidents on recipients of their services."
            },
            {
                "section_number": "23",
                "title": "Reporting obligations for significant incidents",
                "text": "Each Member State shall ensure that essential and important entities notify, without undue delay, its CSIRT or competent authority of any significant incident. An incident shall be considered to be significant if it has caused or is capable of causing severe operational disruption of the services or financial loss."
            }
        ]
    },
    {
        "act_id": "EU_COPYRIGHT_DSM_2019",
        "act_title": "Directive (EU) 2019/790 on Copyright in the Digital Single Market",
        "short_title": "EU Copyright DSM (2019/790)",
        "year": 2019,
        "act_number": "Directive (EU) 2019/790",
        "enactment_date": "17-Apr-2019",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2019/790/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "copyright dsm",
            "eu copyright directive",
            "directive 2019/790",
            "digital single market copyright"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Text and data mining for the purposes of scientific research",
                "text": "Member States shall provide for an exception to the exclusive rights for reproductions and extractions made by research organisations and cultural heritage institutions in order to carry out, for the purposes of scientific research, text and data mining of works or other subject matter to which they have lawful access."
            },
            {
                "section_number": "17",
                "title": "Use of protected content by online content-sharing service providers",
                "text": "An online content-sharing service provider performs an act of communication to the public or an act of making available to the public for the purposes of this Directive when it gives the public access to copyright-protected works or other protected subject matter uploaded by its users."
            }
        ]
    },
    {
        "act_id": "EU_CSDDD_2024",
        "act_title": "Directive (EU) 2024/1760 on Corporate Sustainability Due Diligence (CSDDD)",
        "short_title": "EU CSDDD Directive",
        "year": 2024,
        "act_number": "Directive (EU) 2024/1760",
        "enactment_date": "13-Jun-2024",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2024/1760/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "csddd",
            "corporate sustainability due diligence",
            "directive 2024/1760",
            "csdd"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Subject matter and objectives",
                "text": "This Directive lays down rules on obligations for companies regarding actual and potential human rights adverse impacts and environmental adverse impacts, with respect to their own operations, the operations of their subsidiaries, and the operations carried out by their business partners in chains of activities."
            },
            {
                "section_number": "6",
                "title": "Identification and assessment of actual and potential adverse impacts",
                "text": "Member States shall ensure that companies take appropriate measures to identify and assess actual and potential adverse human rights impacts and adverse environmental impacts arising from their own operations or those of their subsidiaries and, where related to their chains of activities, those of their business partners."
            }
        ]
    },
    {
        "act_id": "EU_CSRD_2022",
        "act_title": "Directive (EU) 2022/2464 on Corporate Sustainability Reporting (CSRD)",
        "short_title": "CSRD (Directive 2022/2464)",
        "year": 2022,
        "act_number": "Directive (EU) 2022/2464",
        "enactment_date": "14-Dec-2022",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2022/2464/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "csrd",
            "corporate sustainability reporting",
            "directive 2022/2464",
            "esg reporting eu"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Sustainability reporting standards",
                "text": "Large undertakings and listed small and medium-sized undertakings shall include in the management report information necessary to understand the undertaking's impacts on sustainability matters, and information necessary to understand how sustainability matters affect the undertaking's development, performance and position."
            },
            {
                "section_number": "19a",
                "title": "Double materiality requirement",
                "text": "Undertakings shall report both on the impact of their activities on people and the environment (inside-out impact) and on how various sustainability matters affect the company itself (outside-in financial risk)."
            }
        ]
    },
    {
        "act_id": "EU_ECOMMERCE_2000",
        "act_title": "Directive 2000/31/EC on Certain Legal Aspects of Information Society Services (E-Commerce Directive)",
        "short_title": "E-Commerce Directive (2000/31/EC)",
        "year": 2000,
        "act_number": "Directive 2000/31/EC",
        "enactment_date": "08-Jun-2000",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2000/31/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "ecommerce directive",
            "e-commerce directive",
            "directive 2000/31"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Internal market principle",
                "text": "Each Member State shall ensure that the information society services provided by a service provider established on its territory comply with the national provisions applicable in the Member State in question."
            },
            {
                "section_number": "6",
                "title": "Information to be provided in commercial communications",
                "text": "In addition to other information requirements established by Community law, Member States shall ensure that commercial communications which are part of, or constitute, an information society service comply with the conditions that the commercial communication shall be clearly identifiable as such."
            },
            {
                "section_number": "14",
                "title": "Hosting liability exemption",
                "text": "Where an information society service is provided that consists of the storage of information provided by a recipient of the service, the service provider is not liable for the information stored at the request of a recipient of the service, on condition that the provider does not have actual knowledge of illegal activity or illegal content."
            }
        ]
    },
    {
        "act_id": "EU_CONSUMER_RIGHTS_2011",
        "act_title": "Directive 2011/83/EU on Consumer Rights",
        "short_title": "Consumer Rights Directive (2011/83/EU)",
        "year": 2011,
        "act_number": "Directive 2011/83/EU",
        "enactment_date": "25-Oct-2011",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2011/83/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "consumer rights directive",
            "directive 2011/83",
            "crd"
        ],
        "sections": [
            {
                "section_number": "6",
                "title": "Information requirements for distance and off-premises contracts",
                "text": "Before the consumer is bound by a distance or off-premises contract, or any corresponding offer, the trader shall provide the consumer with the main characteristics of the goods or services, the identity of the trader, the total price including taxes, and conditions for withdrawal."
            },
            {
                "section_number": "9",
                "title": "Right of withdrawal",
                "text": "Save where the exceptions provided for in Article 16 apply, the consumer shall have a period of 14 days to withdraw from a distance or off-premises contract, without giving any reason, and without incurring any costs other than those provided for in Article 13(2) and Article 14."
            }
        ]
    },
    {
        "act_id": "EU_DIGITAL_CONTENT_2019",
        "act_title": "Directive (EU) 2019/770 on Certain Aspects Concerning Contracts for the Supply of Digital Content and Digital Services",
        "short_title": "Digital Content Directive (2019/770)",
        "year": 2019,
        "act_number": "Directive (EU) 2019/770",
        "enactment_date": "20-May-2019",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2019/770/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "digital content directive",
            "directive 2019/770",
            "dcd"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Supply of the digital content or digital service",
                "text": "The trader shall supply the digital content or digital service to the consumer. Unless the parties have agreed otherwise, the trader shall supply the digital content or digital service without undue delay after the conclusion of the contract."
            },
            {
                "section_number": "7",
                "title": "Subjective requirements for conformity",
                "text": "In order to conform with the contract, the digital content or digital service shall, in particular, be of the description, quantity and quality, and possess the functionality, compatibility, interoperability and other features, as required by the contract."
            }
        ]
    },
    {
        "act_id": "EU_SALE_OF_GOODS_2019",
        "act_title": "Directive (EU) 2019/771 on Certain Aspects Concerning Contracts for the Sale of Goods",
        "short_title": "Sale of Goods Directive (2019/771)",
        "year": 2019,
        "act_number": "Directive (EU) 2019/771",
        "enactment_date": "20-May-2019",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2019/771/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "sale of goods directive eu",
            "directive 2019/771",
            "sgd"
        ],
        "sections": [
            {
                "section_number": "5",
                "title": "Conformity of goods",
                "text": "The seller shall deliver to the consumer goods that meet the requirements of Articles 6, 7 and 8, where applicable, without prejudice to Article 9."
            },
            {
                "section_number": "10",
                "title": "Liability of the seller and remedies for lack of conformity",
                "text": "The seller shall be liable to the consumer for any lack of conformity which exists at the time when the goods were delivered and which becomes apparent within two years of that time."
            }
        ]
    },
    {
        "act_id": "EU_TRADE_SECRETS_2016",
        "act_title": "Directive (EU) 2016/943 on the Protection of Undisclosed Know-How and Business Information (Trade Secrets Directive)",
        "short_title": "Trade Secrets Directive (2016/943)",
        "year": 2016,
        "act_number": "Directive (EU) 2016/943",
        "enactment_date": "08-Jun-2016",
        "official_url": "https://eur-lex.europa.eu/eli/dir/2016/943/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "trade secrets directive",
            "directive 2016/943",
            "eu trade secrets"
        ],
        "sections": [
            {
                "section_number": "2",
                "title": "Definitions: Trade secret",
                "text": "'Trade secret' means information which meets all of the following requirements: (a) it is secret in the sense that it is not generally known among or readily accessible to persons within the circles that normally deal with the kind of information in question; (b) it has commercial value because it is secret; (c) it has been subject to reasonable steps under the circumstances, by the person lawfully in control of the information, to keep it secret."
            },
            {
                "section_number": "4",
                "title": "Unlawful acquisition, use and disclosure of trade secrets",
                "text": "Member States shall ensure that trade secret holders are entitled to apply for the measures, procedures and remedies provided for in this Directive in order to prevent, or obtain redress for, the unlawful acquisition, use or disclosure of their trade secret."
            }
        ]
    },
    {
        "act_id": "EU_PRODUCT_LIABILITY_1985",
        "act_title": "Council Directive 85/374/EEC on the Approximation of the Laws, Regulations and Administrative Provisions of the Member States Concerning Liability for Defective Products",
        "short_title": "Product Liability Directive (85/374/EEC)",
        "year": 1985,
        "act_number": "Directive 85/374/EEC",
        "enactment_date": "25-Jul-1985",
        "official_url": "https://eur-lex.europa.eu/eli/dir/1985/374/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "product liability directive",
            "directive 85/374",
            "defective products directive"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Producer liability for damage caused by defect in product",
                "text": "The producer shall be liable for damage caused by a defect in his product."
            },
            {
                "section_number": "4",
                "title": "Proof of damage, defect and causal relationship",
                "text": "The injured person shall be required to prove the damage, the defect and the causal relationship between defect and damage."
            }
        ]
    },
    {
        "act_id": "EU_TFEU_2012",
        "act_title": "Consolidated Version of the Treaty on the Functioning of the European Union (TFEU 2012)",
        "short_title": "TFEU (2012/C 326/01)",
        "year": 2012,
        "act_number": "Treaty of Lisbon (2012/C 326/01)",
        "enactment_date": "26-Oct-2012",
        "official_url": "https://eur-lex.europa.eu/eli/treaty/tfeu_2012/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "tfeu",
            "treaty on the functioning of the european union",
            "article 101 tfeu",
            "article 102 tfeu"
        ],
        "sections": [
            {
                "section_number": "101",
                "title": "Prohibition of anti-competitive agreements, decisions and concerted practices",
                "text": "The following shall be prohibited as incompatible with the internal market: all agreements between undertakings, decisions by associations of undertakings and concerted practices which may affect trade between Member States and which have as their object or effect the prevention, restriction or distortion of competition within the internal market."
            },
            {
                "section_number": "102",
                "title": "Prohibition of abuse of a dominant position",
                "text": "Any abuse by one or more undertakings of a dominant position within the internal market or in a substantial part of it shall be prohibited as incompatible with the internal market in so far as it may affect trade between Member States."
            },
            {
                "section_number": "267",
                "title": "Preliminary rulings by the Court of Justice of the European Union",
                "text": "The Court of Justice of the European Union shall have jurisdiction to give preliminary rulings concerning: (a) the interpretation of the Treaties; (b) the validity and interpretation of acts of the institutions, bodies, offices or agencies of the Union."
            }
        ]
    },
    {
        "act_id": "EU_TEU_2016",
        "act_title": "Consolidated Version of the Treaty on European Union (TEU 2016)",
        "short_title": "TEU (2016/C 202/01)",
        "year": 2016,
        "act_number": "Treaty of Lisbon (2016/C 202/01)",
        "enactment_date": "07-Jun-2016",
        "official_url": "https://eur-lex.europa.eu/eli/treaty/teu_2016/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "teu",
            "treaty on european union",
            "article 2 teu",
            "maastricht treaty as amended"
        ],
        "sections": [
            {
                "section_number": "2",
                "title": "Founding values of the Union: Human dignity, freedom, democracy, equality, rule of law",
                "text": "The Union is founded on the values of respect for human dignity, freedom, democracy, equality, the rule of law and respect for human rights, including the rights of persons belonging to minorities. These values are common to the Member States in a society in which pluralism, non-discrimination, tolerance, justice, solidarity and equality between women and men prevail."
            },
            {
                "section_number": "10",
                "title": "Representative democracy and citizen participation",
                "text": "The functioning of the Union shall be founded on representative democracy. Citizens are directly represented at Union level in the European Parliament. Member States are represented in the European Council by their Heads of State or Government and in the Council by their governments."
            }
        ]
    },
    {
        "act_id": "EU_CHARTER_2012",
        "act_title": "Charter of Fundamental Rights of the European Union (2012/C 326/02)",
        "short_title": "EU Charter of Fundamental Rights",
        "year": 2012,
        "act_number": "2012/C 326/02",
        "enactment_date": "26-Oct-2012",
        "official_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:12012P/TXT",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "charter of fundamental rights",
            "eu charter",
            "eu fundamental rights"
        ],
        "sections": [
            {
                "section_number": "8",
                "title": "Protection of personal data",
                "text": "Everyone has the right to the protection of personal data concerning him or her. Such data must be processed fairly for specified purposes and on the basis of the consent of the person concerned or some other legitimate basis laid down by law. Everyone has the right of access to data which has been collected concerning him or her, and the right to have it rectified."
            },
            {
                "section_number": "47",
                "title": "Right to an effective remedy and to a fair trial",
                "text": "Everyone whose rights and freedoms guaranteed by the law of the Union are violated has the right to an effective remedy before a tribunal in compliance with the conditions laid down in this Article. Everyone is entitled to a fair and public hearing within a reasonable time by an independent and impartial tribunal previously established by law."
            }
        ]
    },
    {
        "act_id": "EU_BRUSSELS_I_RECAST_2012",
        "act_title": "Regulation (EU) No 1215/2012 on Jurisdiction and the Recognition and Enforcement of Judgments in Civil and Commercial Matters (Brussels I Recast)",
        "short_title": "Brussels I Recast (1215/2012)",
        "year": 2012,
        "act_number": "Regulation (EU) 1215/2012",
        "enactment_date": "12-Dec-2012",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2012/1215/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "brussels i",
            "brussels i recast",
            "regulation 1215/2012",
            "eu jurisdiction regulation"
        ],
        "sections": [
            {
                "section_number": "4",
                "title": "General jurisdiction based on defendant's domicile",
                "text": "Subject to this Regulation, persons domiciled in a Member State shall, whatever their nationality, be sued in the courts of that Member State."
            },
            {
                "section_number": "7",
                "title": "Special jurisdiction in matters relating to contract and tort",
                "text": "A person domiciled in a Member State may be sued in another Member State: (1) in matters relating to a contract, in the courts for the place of performance of the obligation in question; (2) in matters relating to tort, delict or quasi-delict, in the courts for the place where the harmful event occurred or may occur."
            }
        ]
    },
    {
        "act_id": "EU_ROME_I_2008",
        "act_title": "Regulation (EC) No 593/2008 on the Law Applicable to Contractual Obligations (Rome I)",
        "short_title": "Rome I Regulation (593/2008)",
        "year": 2008,
        "act_number": "Regulation (EC) 593/2008",
        "enactment_date": "17-Jun-2008",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2008/593/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "rome i",
            "rome 1",
            "regulation 593/2008",
            "applicable law to contracts"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "Freedom of choice of law in contracts",
                "text": "A contract shall be governed by the law chosen by the parties. The choice shall be made expressly or clearly demonstrated by the terms of the contract or the circumstances of the case. By their choice the parties can select the law applicable to the whole or to part only of the contract."
            },
            {
                "section_number": "4",
                "title": "Applicable law in the absence of choice",
                "text": "To the extent that the law applicable to the contract has not been chosen in accordance with Article 3 and without prejudice to Articles 5 to 8, the law governing the contract shall be determined as follows: a contract for the sale of goods shall be governed by the law of the country where the seller has his habitual residence."
            }
        ]
    },
    {
        "act_id": "EU_ROME_II_2007",
        "act_title": "Regulation (EC) No 864/2007 on the Law Applicable to Non-Contractual Obligations (Rome II)",
        "short_title": "Rome II Regulation (864/2007)",
        "year": 2007,
        "act_number": "Regulation (EC) 864/2007",
        "enactment_date": "11-Jul-2007",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2007/864/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "rome ii",
            "rome 2",
            "regulation 864/2007",
            "applicable law to torts"
        ],
        "sections": [
            {
                "section_number": "4",
                "title": "General rule for law applicable to tort/delict",
                "text": "Unless otherwise provided for in this Regulation, the law applicable to a non-contractual obligation arising out of a tort/delict shall be the law of the country in which the damage occurs irrespective of the country in which the event giving rise to the damage occurred and irrespective of the country or countries in which the indirect consequences of that event occur."
            }
        ]
    },
    {
        "act_id": "EU_INSOLVENCY_2015",
        "act_title": "Regulation (EU) 2015/848 on Insolvency Proceedings (Recast)",
        "short_title": "European Insolvency Regulation (2015/848)",
        "year": 2015,
        "act_number": "Regulation (EU) 2015/848",
        "enactment_date": "20-May-2015",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2015/848/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "european insolvency regulation",
            "regulation 2015/848",
            "eu insolvency"
        ],
        "sections": [
            {
                "section_number": "3",
                "title": "International jurisdiction based on center of main interests (COMI)",
                "text": "The courts of the Member State within the territory of which the centre of the debtor's main interests is situated shall have jurisdiction to open insolvency proceedings ('main insolvency proceedings'). The centre of main interests shall be the place where the debtor conducts the administration of its interests on a regular basis and which is ascertainable by third parties."
            }
        ]
    },
    {
        "act_id": "EU_CHIPS_ACT_2023",
        "act_title": "Regulation (EU) 2023/1781 Establishing a Framework of Measures for Strengthening Europe's Semiconductor Ecosystem (European Chips Act)",
        "short_title": "European Chips Act (2023/1781)",
        "year": 2023,
        "act_number": "Regulation (EU) 2023/1781",
        "enactment_date": "13-Sep-2023",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2023/1781/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "chips act",
            "european chips act",
            "regulation 2023/1781"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Subject matter and general objectives (Chips for Europe Initiative)",
                "text": "This Regulation establishes a framework for strengthening the competitiveness and resilience of the Union's semiconductor technology and applications. It sets up the Chips for Europe Initiative to support large-scale technological capacity building and innovation throughout the Union."
            },
            {
                "section_number": "15",
                "title": "Integrated Production Facilities",
                "text": "Integrated Production Facilities are first-of-a-kind semiconductor manufacturing facilities in the Union that may design and produce chips, or package them, to enhance the security of supply and the resilience of the ecosystem."
            }
        ]
    },
    {
        "act_id": "EU_NET_ZERO_INDUSTRY_2024",
        "act_title": "Regulation (EU) 2024/1735 Establishing a Framework of Measures for Strengthening Europe's Net-Zero Technology Products Manufacturing Ecosystem (Net-Zero Industry Act)",
        "short_title": "Net-Zero Industry Act (2024/1735)",
        "year": 2024,
        "act_number": "Regulation (EU) 2024/1735",
        "enactment_date": "13-Jun-2024",
        "official_url": "https://eur-lex.europa.eu/eli/reg/2024/1735/oj",
        "legislation_portal": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal": "https://curia.europa.eu",
        "constitutional_court_portal": "https://curia.europa.eu",
        "aliases": [
            "net-zero industry act",
            "nzia",
            "regulation 2024/1735"
        ],
        "sections": [
            {
                "section_number": "1",
                "title": "Subject matter and scope",
                "text": "This Regulation establishes a framework of measures to strengthen the Union's manufacturing ecosystem for net-zero technology products and support the Union's clean energy transition and industrial decarbonisation."
            },
            {
                "section_number": "10",
                "title": "Net-zero strategic projects",
                "text": "Member States shall recognise as net-zero strategic projects those net-zero technology manufacturing projects located in the Union that contribute to the realisation of the objectives set out in Article 1 and meet the criteria set out in this Article."
            }
        ]
    }
]

def main():
    print("=" * 70)
    print("MULTI-JURISDICTION LEGAL DATASET & CORPUS POPULATION ENGINE")
    print("Populating India, US, UK, EU, and Northern & Eastern Europe...")
    print("=" * 70)

    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS acts (
        act_id TEXT PRIMARY KEY,
        act_title TEXT,
        short_title TEXT,
        act_number TEXT,
        enactment_date TEXT,
        year INTEGER,
        source_url TEXT,
        aliases TEXT,
        sha256 TEXT,
        jurisdiction TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        section_id TEXT PRIMARY KEY,
        act_id TEXT,
        section_number TEXT,
        title TEXT,
        text TEXT,
        source_url TEXT,
        sha256 TEXT,
        jurisdiction TEXT,
        FOREIGN KEY (act_id) REFERENCES acts (act_id)
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sections_act_sec ON sections (act_id, section_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_acts_jurisdiction ON acts (jurisdiction)")

    registry = {}
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            registry = json.load(f)

    portal_rows = []

    # 1. Northern and Eastern Europe
    print("\n[1/5] Processing Northern & Eastern European Constitutions...")
    ne_rows = []
    for item in NE_EUROPE_CORPUS:
        act_id = item["act_id"]
        jur = item["jurisdiction"]
        country = item["country"]
        dial_code = item["dial_code"]
        act_title = item["act_title"]
        short_title = item["short_title"]
        year = item["year"]
        act_number = item["act_number"]
        enactment_date = item["enactment_date"]
        official_url = item["official_url"]

        first_sec_text = item["sections"][0]["text"] if item["sections"] else act_title
        sec_hash = compute_hash(first_sec_text)

        registry[act_id] = {
            "act_title": act_title,
            "short_name": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "jurisdiction": jur,
            "country": country,
            "dial_code": dial_code,
            "aliases": item["aliases"]
        }

        ne_rows.append({
            "jurisdiction": jur,
            "country": country,
            "dial_code": dial_code,
            "act_id": act_id,
            "act_title": act_title,
            "short_title": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "sha256": sec_hash
        })

        portal_rows.append({
            "country": country,
            "dial_code": dial_code,
            "jurisdiction": jur,
            "constitutional_act": act_title,
            "legislation_portal_url": item["legislation_portal"],
            "supreme_court_portal_url": item["supreme_court_portal"],
            "constitutional_court_portal_url": item["constitutional_court_portal"],
            "description": f"National court and legislative portals for {country} ({dial_code})"
        })

        cursor.execute("""
        INSERT OR REPLACE INTO acts (act_id, act_title, short_title, act_number, enactment_date, year, source_url, aliases, sha256, jurisdiction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (act_id, act_title, short_title, act_number, enactment_date, year, official_url, json.dumps(item["aliases"]), sec_hash, jur))

        corpus_act_dir = os.path.join(CORPUS_DIR, jur, act_id)
        os.makedirs(corpus_act_dir, exist_ok=True)

        for sec in item["sections"]:
            sec_num = sec["section_number"]
            sec_title = sec["title"]
            sec_text = sec["text"]
            sec_h = compute_hash(sec_text)
            sec_id = f"{act_id}_{sec_num}"

            cursor.execute("""
            INSERT OR REPLACE INTO sections (section_id, act_id, section_number, title, text, source_url, sha256, jurisdiction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sec_id, act_id, sec_num, sec_title, sec_text, official_url, sec_h, jur))

            sec_data = {
                "act_id": act_id,
                "section_number": sec_num,
                "title": sec_title,
                "text": sec_text,
                "source_url": official_url,
                "sha256": sec_h,
                "jurisdiction": jur
            }
            with open(os.path.join(corpus_act_dir, f"section_{sec_num.replace(':', '_')}.json"), "w", encoding="utf-8") as f:
                json.dump(sec_data, f, indent=2)

    print(f"  OK: Indexed {len(NE_EUROPE_CORPUS)} Northern & Eastern European constitutions.")

    # 2. United States
    print("\n[2/5] Processing United States Statutes & Codes...")
    us_rows = []
    for item in US_CORPUS:
        act_id = item["act_id"]
        jur = "US"
        act_title = item["act_title"]
        short_title = item["short_title"]
        year = item["year"]
        act_number = item["act_number"]
        enactment_date = item["enactment_date"]
        official_url = item["official_url"]

        first_sec_text = item["sections"][0]["text"] if item["sections"] else act_title
        sec_hash = compute_hash(first_sec_text)
        registry[act_id] = {
            "act_title": act_title,
            "short_name": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "jurisdiction": jur,
            "country": "United States",
            "dial_code": "+1",
            "aliases": item["aliases"]
        }

        us_rows.append({
            "jurisdiction": jur,
            "act_id": act_id,
            "act_title": act_title,
            "short_title": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "sha256": sec_hash
        })

        cursor.execute("""
        INSERT OR REPLACE INTO acts (act_id, act_title, short_title, act_number, enactment_date, year, source_url, aliases, sha256, jurisdiction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (act_id, act_title, short_title, act_number, enactment_date, year, official_url, json.dumps(item["aliases"]), sec_hash, jur))

        corpus_act_dir = os.path.join(CORPUS_DIR, jur, act_id)
        os.makedirs(corpus_act_dir, exist_ok=True)

        for sec in item["sections"]:
            sec_num = sec["section_number"]
            sec_title = sec["title"]
            sec_text = sec["text"]
            sec_h = compute_hash(sec_text)
            sec_id = f"{act_id}_{sec_num}"

            cursor.execute("""
            INSERT OR REPLACE INTO sections (section_id, act_id, section_number, title, text, source_url, sha256, jurisdiction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sec_id, act_id, sec_num, sec_title, sec_text, official_url, sec_h, jur))

            sec_data = {
                "act_id": act_id,
                "section_number": sec_num,
                "title": sec_title,
                "text": sec_text,
                "source_url": official_url,
                "sha256": sec_h,
                "jurisdiction": jur
            }
            with open(os.path.join(corpus_act_dir, f"section_{sec_num.replace(':', '_')}.json"), "w", encoding="utf-8") as f:
                json.dump(sec_data, f, indent=2)

    portal_rows.append({
        "country": "United States",
        "dial_code": "+1",
        "jurisdiction": "US",
        "constitutional_act": "Constitution of the United States (1787) / United States Code (U.S.C.)",
        "legislation_portal_url": "https://www.congress.gov",
        "supreme_court_portal_url": "https://www.supremecourt.gov",
        "constitutional_court_portal_url": "https://uscode.house.gov",
        "description": "United States Code (U.S.C.) and federal legislation on Congress.gov, Statutes at Large via Library of Congress, and US Supreme Court"
    })
    print(f"  OK: Indexed {len(US_CORPUS)} US statutory and constitutional codes.")

    # 3. United Kingdom
    print("\n[3/5] Processing United Kingdom Statutes...")
    uk_rows = []
    for item in UK_CORPUS:
        act_id = item["act_id"]
        jur = "UK"
        act_title = item["act_title"]
        short_title = item["short_title"]
        year = item["year"]
        act_number = item["act_number"]
        enactment_date = item["enactment_date"]
        official_url = item["official_url"]

        first_sec_text = item["sections"][0]["text"] if item["sections"] else act_title
        sec_hash = compute_hash(first_sec_text)
        registry[act_id] = {
            "act_title": act_title,
            "short_name": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "jurisdiction": jur,
            "country": "United Kingdom",
            "dial_code": "+44",
            "aliases": item["aliases"]
        }

        uk_rows.append({
            "jurisdiction": jur,
            "act_id": act_id,
            "act_title": act_title,
            "short_title": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "sha256": sec_hash
        })

        cursor.execute("""
        INSERT OR REPLACE INTO acts (act_id, act_title, short_title, act_number, enactment_date, year, source_url, aliases, sha256, jurisdiction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (act_id, act_title, short_title, act_number, enactment_date, year, official_url, json.dumps(item["aliases"]), sec_hash, jur))

        corpus_act_dir = os.path.join(CORPUS_DIR, jur, act_id)
        os.makedirs(corpus_act_dir, exist_ok=True)

        for sec in item["sections"]:
            sec_num = sec["section_number"]
            sec_title = sec["title"]
            sec_text = sec["text"]
            sec_h = compute_hash(sec_text)
            sec_id = f"{act_id}_{sec_num}"

            cursor.execute("""
            INSERT OR REPLACE INTO sections (section_id, act_id, section_number, title, text, source_url, sha256, jurisdiction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sec_id, act_id, sec_num, sec_title, sec_text, official_url, sec_h, jur))

            sec_data = {
                "act_id": act_id,
                "section_number": sec_num,
                "title": sec_title,
                "text": sec_text,
                "source_url": official_url,
                "sha256": sec_h,
                "jurisdiction": jur
            }
            with open(os.path.join(corpus_act_dir, f"section_{sec_num.replace(':', '_')}.json"), "w", encoding="utf-8") as f:
                json.dump(sec_data, f, indent=2)

    portal_rows.append({
        "country": "United Kingdom",
        "dial_code": "+44",
        "jurisdiction": "UK",
        "constitutional_act": "Acts of Parliament (Theft Act 1968, Human Rights Act 1998, Consumer Rights Act 2015, Sale of Goods 1979)",
        "legislation_portal_url": "https://www.legislation.gov.uk",
        "supreme_court_portal_url": "https://www.supremecourt.uk",
        "constitutional_court_portal_url": "https://www.judiciary.uk",
        "description": "Primary and secondary legislation for England, Wales, Scotland, and Northern Ireland on Legislation.gov.uk managed by The National Archives, and UK Supreme Court"
    })
    print(f"  OK: Indexed {len(UK_CORPUS)} UK statutes.")

    # 4. European Union
    print("\n[4/5] Processing European Union Regulations & Treaties...")
    eu_rows = []
    for item in EU_CORPUS:
        act_id = item["act_id"]
        jur = "EU"
        act_title = item["act_title"]
        short_title = item["short_title"]
        year = item["year"]
        act_number = item["act_number"]
        enactment_date = item["enactment_date"]
        official_url = item["official_url"]

        first_sec_text = item["sections"][0]["text"] if item["sections"] else act_title
        sec_hash = compute_hash(first_sec_text)
        registry[act_id] = {
            "act_title": act_title,
            "short_name": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "jurisdiction": jur,
            "country": "European Union",
            "dial_code": "+32",
            "aliases": item["aliases"]
        }

        eu_rows.append({
            "jurisdiction": jur,
            "act_id": act_id,
            "act_title": act_title,
            "short_title": short_title,
            "year": year,
            "act_number": act_number,
            "enactment_date": enactment_date,
            "official_url": official_url,
            "sha256": sec_hash
        })

        cursor.execute("""
        INSERT OR REPLACE INTO acts (act_id, act_title, short_title, act_number, enactment_date, year, source_url, aliases, sha256, jurisdiction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (act_id, act_title, short_title, act_number, enactment_date, year, official_url, json.dumps(item["aliases"]), sec_hash, jur))

        corpus_act_dir = os.path.join(CORPUS_DIR, jur, act_id)
        os.makedirs(corpus_act_dir, exist_ok=True)

        for sec in item["sections"]:
            sec_num = sec["section_number"]
            sec_title = sec["title"]
            sec_text = sec["text"]
            sec_h = compute_hash(sec_text)
            sec_id = f"{act_id}_{sec_num}"

            cursor.execute("""
            INSERT OR REPLACE INTO sections (section_id, act_id, section_number, title, text, source_url, sha256, jurisdiction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (sec_id, act_id, sec_num, sec_title, sec_text, official_url, sec_h, jur))

            sec_data = {
                "act_id": act_id,
                "section_number": sec_num,
                "title": sec_title,
                "text": sec_text,
                "source_url": official_url,
                "sha256": sec_h,
                "jurisdiction": jur
            }
            with open(os.path.join(corpus_act_dir, f"section_{sec_num.replace(':', '_')}.json"), "w", encoding="utf-8") as f:
                json.dump(sec_data, f, indent=2)

    portal_rows.append({
        "country": "European Union",
        "dial_code": "+32",
        "jurisdiction": "EU",
        "constitutional_act": "Treaties (TFEU, TEU), Charter of Fundamental Rights, and Regulations (GDPR, AI Act, DSA, DMA, MiCA)",
        "legislation_portal_url": "https://eur-lex.europa.eu/homepage.html",
        "supreme_court_portal_url": "https://curia.europa.eu",
        "constitutional_court_portal_url": "https://curia.europa.eu",
        "description": "Official EU treaties, regulations, directives, and court rulings published on EUR-Lex and Court of Justice of the European Union (CJEU)"
    })
    print(f"  OK: Indexed {len(EU_CORPUS)} EU regulations and treaties.")

    # 5. India Portals
    portal_rows.append({
        "country": "India",
        "dial_code": "+91",
        "jurisdiction": "INDIA",
        "constitutional_act": "The Constitution of India (1950) / Bharatiya Nyaya Sanhita (2023)",
        "legislation_portal_url": "https://www.indiacode.nic.in",
        "supreme_court_portal_url": "https://main.sci.gov.in",
        "constitutional_court_portal_url": "https://ecourts.gov.in/ecourts2.0/",
        "description": "Supreme Court of India, eCourts Services 2.0 (ecourts.gov.in/ecourts2.0/), and Digital Police Citizen Services (digitalpolicecitizenservices.gov.in)"
    })

    conn.commit()
    conn.close()

    # Save JSON Registry
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    print(f"\n[5/5] Updated registry: {REGISTRY_FILE} ({len(registry)} total Acts).")

    # Save CSV Files
    df_ne = pd.DataFrame(ne_rows)
    ne_csv = os.path.join(CSV_DIR, "northern_eastern_europe_constitutions.csv")
    df_ne.to_csv(ne_csv, index=False)
    print(f"Saved: {ne_csv} ({len(df_ne)} rows)")

    df_us = pd.DataFrame(us_rows)
    us_csv = os.path.join(CSV_DIR, "us_federal_statutes.csv")
    df_us.to_csv(us_csv, index=False)
    print(f"Saved: {us_csv} ({len(df_us)} rows)")

    df_uk = pd.DataFrame(uk_rows)
    uk_csv = os.path.join(CSV_DIR, "uk_statutes.csv")
    df_uk.to_csv(uk_csv, index=False)
    print(f"Saved: {uk_csv} ({len(df_uk)} rows)")

    df_eu = pd.DataFrame(eu_rows)
    eu_csv = os.path.join(CSV_DIR, "eu_regulations.csv")
    df_eu.to_csv(eu_csv, index=False)
    print(f"Saved: {eu_csv} ({len(df_eu)} rows)")

    df_portals = pd.DataFrame(portal_rows)
    portals_csv = os.path.join(CSV_DIR, "court_portals_registry.csv")
    df_portals.to_csv(portals_csv, index=False)
    print(f"Saved: {portals_csv} ({len(df_portals)} countries and jurisdictions)")

    # Unified Master CSV
    india_csv = os.path.join(CSV_DIR, "india_central_acts.csv")
    master_rows = []
    if os.path.exists(india_csv):
        df_india = pd.read_csv(india_csv)
        for _, r in df_india.iterrows():
            master_rows.append({
                "jurisdiction": "INDIA",
                "act_id": r.get("act_id"),
                "act_title": r.get("act_title"),
                "short_title": r.get("short_title", r.get("act_title")),
                "year": r.get("year"),
                "act_number": r.get("act_number", "Central Act"),
                "enactment_date": r.get("enactment_date", str(r.get("year"))),
                "official_url": r.get("official_url"),
                "sha256": r.get("sha256")
            })

    for r in ne_rows:
        master_rows.append({
            "jurisdiction": r["jurisdiction"],
            "act_id": r["act_id"],
            "act_title": r["act_title"],
            "short_title": r["short_title"],
            "year": r["year"],
            "act_number": r["act_number"],
            "enactment_date": r["enactment_date"],
            "official_url": r["official_url"],
            "sha256": r["sha256"]
        })

    for r in us_rows:
        master_rows.append(r)

    for r in uk_rows:
        master_rows.append(r)

    for r in eu_rows:
        master_rows.append(r)

    df_master = pd.DataFrame(master_rows)
    master_csv = os.path.join(CSV_DIR, "all_jurisdictions_acts.csv")
    df_master.to_csv(master_csv, index=False)
    print(f"Saved: {master_csv} ({len(df_master)} master statutes across all jurisdictions)")
    print("\n[SUCCESS] All datasets, indexes, and portals generated flawlessly.")

if __name__ == "__main__":
    main()

"""Seed content for the 10-week Effata Dutch curriculum.

Week 1 is fully fleshed out (vocab + grammar + exercises) so the app is
usable end-to-end on day one. Weeks 2-10 are seeded as roadmap entries
(title/goal/module focus) -- the data model is ready for their vocab and
grammar content to be filled in the same shape as Week 1 as Leo progresses.
"""

CURRICULUM = [
    {
        "week_number": 1,
        "title": "Fundamentals: Greetings, Self-Introduction, De/Het",
        "goal": "Introduce yourself, greet people appropriately by time of day, and start "
        "reading nouns correctly with de/het.",
        "module_focus": "Vocabulary Accelerator + Grammar Simplifier (de/het)",
    },
    {
        "week_number": 2,
        "title": "Daily Life & Numbers",
        "goal": "Talk about your daily routine, tell time, and count for shopping/prices.",
        "module_focus": "Vocabulary Accelerator + Grammar Simplifier (present tense)",
    },
    {
        "week_number": 3,
        "title": "Family, Work, and Word Order",
        "goal": "Describe your family and job; master Dutch V2 word order in main clauses.",
        "module_focus": "Grammar Simplifier (word order) + Conversation Simulator",
    },
    {
        "week_number": 4,
        "title": "Housing & Relocation Admin",
        "goal": "Vocabulary for huurcontract, gemeente, inschrijving -- practical relocation Dutch.",
        "module_focus": "Vocabulary Accelerator + Conversation Simulator (roleplay: gemeente)",
    },
    {
        "week_number": 5,
        "title": "Past Tense & Telling Stories",
        "goal": "Form the perfect tense (voltooid deelwoord) to talk about what already happened.",
        "module_focus": "Grammar Simplifier (perfect tense) + Memory Lock review",
    },
    {
        "week_number": 6,
        "title": "Workplace Dutch",
        "goal": "Meetings, email phrases, small talk with colleagues.",
        "module_focus": "Vocabulary Accelerator + Conversation Simulator (roleplay: kantoor)",
    },
    {
        "week_number": 7,
        "title": "Travel & Directions",
        "goal": "Ask for and give directions, navigate public transport (NS, GVB).",
        "module_focus": "Vocabulary Accelerator + Pronunciation Coach focus (g, ui sounds)",
    },
    {
        "week_number": 8,
        "title": "Modal Verbs & Opinions",
        "goal": "Express ability, permission, and opinion with kunnen/mogen/willen/moeten.",
        "module_focus": "Grammar Simplifier (modals) + Conversation Simulator (debate-lite)",
    },
    {
        "week_number": 9,
        "title": "Church & Sermon Vocabulary",
        "goal": "Build vocabulary for worship, scripture reading, and simple sermon delivery.",
        "module_focus": "Vocabulary Accelerator + Pronunciation Coach (public-speaking clarity)",
    },
    {
        "week_number": 10,
        "title": "Fluency Consolidation",
        "goal": "Free conversation across all prior scenarios; full Memory Lock review of weeks 1-9.",
        "module_focus": "Conversation Simulator (mixed scenarios) + Memory Lock (cumulative review)",
    },
]

WEEK_1_VOCAB_THEMES = [
    {
        "name": "Greetings & Politeness",
        "items": [
            {
                "dutch": "Hallo",
                "english": "Hello",
                "ipa": "/ˈɦɑ.loː/",
                "pronunciation_tip": "The Dutch 'h' is breathy, softer than English 'h'.",
                "example_nl": "Hallo, hoe gaat het met je?",
                "example_en": "Hello, how are you?",
                "usage_context": "Informal greeting, any time of day.",
            },
            {
                "dutch": "Goedemorgen",
                "english": "Good morning",
                "ipa": "/ˌɣu.də.ˈmɔr.ɣə(n)/",
                "pronunciation_tip": "The 'g' is a guttural, throaty fricative -- not an English hard g. "
                "Say it like clearing your throat gently.",
                "example_nl": "Goedemorgen! Heb je al koffie gehad?",
                "example_en": "Good morning! Have you had coffee yet?",
                "usage_context": "Used until roughly noon.",
            },
            {
                "dutch": "Goedenavond",
                "english": "Good evening",
                "ipa": "/ˌɣu.də.ˈnaː.vɔnt/",
                "pronunciation_tip": "Same guttural 'g' as goedemorgen.",
                "example_nl": "Goedenavond, welkom bij ons.",
                "example_en": "Good evening, welcome to us.",
                "usage_context": "Used from early evening onward, including as a greeting when entering a shop.",
            },
            {
                "dutch": "Tot ziens",
                "english": "Goodbye (see you)",
                "ipa": "/tɔt ˈzins/",
                "pronunciation_tip": "'z' is voiced, like English 'z' in 'zoo'.",
                "example_nl": "Tot ziens, fijne dag nog!",
                "example_en": "Goodbye, have a nice day!",
                "usage_context": "Polite goodbye in most contexts, including shops and offices.",
            },
            {
                "dutch": "Alstublieft",
                "english": "Please / here you go (formal)",
                "ipa": "/ˌɑls.ty.ˈblift/",
                "pronunciation_tip": "Often shortened in speech to 'alstublieft' -> colloquially 'astublieft'.",
                "example_nl": "Uw koffie, alstublieft.",
                "example_en": "Your coffee, please/here you go.",
                "usage_context": "Formal register -- use with strangers, officials, elders.",
            },
            {
                "dutch": "Dank je wel",
                "english": "Thank you (informal)",
                "ipa": "/dɑŋk jə ʋɛl/",
                "pronunciation_tip": "'w' in Dutch is closer to English 'v' with rounded lips.",
                "example_nl": "Dank je wel voor je hulp!",
                "example_en": "Thank you for your help!",
                "usage_context": "Informal 'je'; use 'dank u wel' with strangers/officials.",
            },
        ],
    },
    {
        "name": "Introducing Yourself",
        "items": [
            {
                "dutch": "Ik heet ...",
                "english": "My name is ...",
                "ipa": "/ɪk ɦeːt/",
                "pronunciation_tip": "'ee' is a long, closed vowel -- hold it slightly longer than English 'ay'.",
                "example_nl": "Ik heet Leo. Aangenaam!",
                "example_en": "My name is Leo. Nice to meet you!",
                "usage_context": "Core self-introduction phrase.",
            },
            {
                "dutch": "Ik kom uit ...",
                "english": "I come from ...",
                "ipa": "/ɪk kɔm œʏt/",
                "pronunciation_tip": "'ui' (as in uit) is a diphthong with no English equivalent -- round your lips "
                "starting near 'oe' and glide toward 'ui'.",
                "example_nl": "Ik kom uit Indonesië.",
                "example_en": "I come from Indonesia.",
                "usage_context": "Stating country/city of origin.",
            },
            {
                "dutch": "Aangenaam",
                "english": "Nice to meet you / Pleased to meet you",
                "ipa": "/ˌaːn.ɣə.ˈnaːm/",
                "pronunciation_tip": "Guttural 'g' again, mid-word this time.",
                "example_nl": "Aangenaam kennis te maken.",
                "example_en": "Pleased to make your acquaintance.",
                "usage_context": "Formal first-meeting phrase.",
            },
            {
                "dutch": "Ik woon in ...",
                "english": "I live in ...",
                "ipa": "/ɪk ʋoːn ɪn/",
                "pronunciation_tip": "'oo' is long and closed, similar to French 'eau'.",
                "example_nl": "Ik woon in Amsterdam.",
                "example_en": "I live in Amsterdam.",
                "usage_context": "Stating current residence -- useful for relocation admin.",
            },
        ],
    },
]

WEEK_1_GRAMMAR_TOPICS = [
    {
        "title": "De vs. Het: the two Dutch definite articles",
        "explanation_md": (
            "Dutch has two words for 'the': **de** and **het**. There is no reliable rule that "
            "predicts which one a noun takes -- it must be memorized per word (about 2/3 of nouns "
            "are 'de'-words). Two patterns that DO help:\n\n"
            "- Plural nouns are always **de** (de honden, de huizen).\n"
            "- Diminutives (ending in -je, -tje, -pje) are always **het** (het huisje, het kopje).\n\n"
            "Best practice: learn every new noun together with its article, e.g. flashcard 'het huis' "
            "not just 'huis'."
        ),
        "common_mistakes_md": (
            "- Guessing 'de' by default because it's more common -- this fails for common words like "
            "het huis, het boek, het meisje.\n"
            "- Forgetting that plurals always take 'de', even if the singular is 'het' (het boek -> "
            "de boeken)."
        ),
        "exercises": [
            {
                "prompt": "___ huis (the house)",
                "choices": ["De", "Het"],
                "correct_index": 1,
                "explanation": "'Huis' is a het-word: het huis.",
            },
            {
                "prompt": "___ boeken (the books)",
                "choices": ["De", "Het"],
                "correct_index": 0,
                "explanation": "Plural nouns always take 'de', regardless of the singular article.",
            },
            {
                "prompt": "___ tafel (the table)",
                "choices": ["De", "Het"],
                "correct_index": 0,
                "explanation": "'Tafel' is a de-word: de tafel.",
            },
            {
                "prompt": "___ meisje (the girl)",
                "choices": ["De", "Het"],
                "correct_index": 1,
                "explanation": "Diminutives ending in -je are always 'het', even though 'meisje' refers to a "
                "female.",
            },
        ],
    },
]

"""Seed content for the 10-week Effata Dutch curriculum.

Each week is explicitly mapped onto one of the six target domains from the
coaching brief: (1) engineering/technical work, (2) presenting work results,
(3) everyday conversation, (4) shopping, (5) community/social life, and
(6) preaching in church -- this is also the SCENARIOS list conversation.py
rotates the Gesprek coach through, so the vocabulary a week teaches and the
scenarios the coach leads with stay aligned.

Weeks 1, 2, 6, 7, and 9 are fully fleshed out (vocab + grammar/exercises
where relevant) so the app is usable end-to-end across all six domains on
day one. Weeks 3-5, 8, and 10 are seeded as roadmap entries only (grammar
foundation the other domains lean on) -- fill their vocab in the same shape
as the fleshed-out weeks as content is added.
"""

CURRICULUM = [
    {
        "week_number": 1,
        "title": "Fondasi: Sapaan, Perkenalan Diri, De/Het",
        "goal": "Introduce yourself, greet people appropriately by time of day, and start "
        "reading nouns correctly with de/het. [Domain: Dagelijks gesprek]",
        "module_focus": "Vocabulary Accelerator + Grammar Simplifier (de/het)",
    },
    {
        "week_number": 2,
        "title": "Werk & Engineering: Kosakata Kerja Teknis",
        "goal": "Talk about your engineering work -- stand-ups, bugs, deadlines, code review -- "
        "using the vocabulary Dutch colleagues actually use. [Domain: Werk & Engineering]",
        "module_focus": "Vocabulary Accelerator + Conversation Simulator (roleplay: stand-up)",
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
        "title": "Presentatie Geven: Hasil Kerja",
        "goal": "Present a project update or work result clearly to colleagues -- structuring a "
        "short presentation and handling questions. [Domain: Presentatie geven]",
        "module_focus": "Vocabulary Accelerator + Conversation Simulator (roleplay: project update)",
    },
    {
        "week_number": 7,
        "title": "Boodschappen Doen: Berbelanja",
        "goal": "Shop confidently -- supermarket, bakery, market stall -- asking prices, "
        "quantities, and paying. [Domain: Boodschappen doen]",
        "module_focus": "Vocabulary Accelerator + Pronunciation Coach focus (g, ui sounds)",
    },
    {
        "week_number": 8,
        "title": "Modal Verbs & Opinions",
        "goal": "Express ability, permission, and opinion with kunnen/mogen/willen/moeten -- "
        "useful across every domain, especially community small talk.",
        "module_focus": "Grammar Simplifier (modals) + Conversation Simulator (debate-lite)",
    },
    {
        "week_number": 9,
        "title": "Preken in de Kerk: Ibadah & Khotbah",
        "goal": "Build vocabulary for worship, scripture reading, and simple sermon delivery in "
        "front of a congregation. [Domain: Preken in de kerk]",
        "module_focus": "Vocabulary Accelerator + Pronunciation Coach (public-speaking clarity)",
    },
    {
        "week_number": 10,
        "title": "Gemeenschap & Vloeiendheid: Konsolidasi",
        "goal": "Socialize naturally in a Dutch community (buurtborrel, vereniging) and free-"
        "converse across all six domains; full Memory Lock review of weeks 1-9. "
        "[Domain: Gemeenschap & vrienden]",
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

WEEK_2_VOCAB_THEMES = [
    {
        "name": "Werk & Engineering",
        "items": [
            {
                "dutch": "de vergadering",
                "english": "the meeting",
                "ipa": "/də vərˈɣaːdərɪŋ/",
                "pronunciation_tip": "Guttural 'g' in the middle -- throaty, not a hard English 'g'.",
                "example_nl": "We hebben elke ochtend een korte vergadering.",
                "example_en": "We have a short meeting every morning.",
                "usage_context": "Standard word for any work meeting, including stand-ups.",
            },
            {
                "dutch": "de bug oplossen",
                "english": "to fix the bug",
                "ipa": "/də bʌɣ ˈɔplɔsə(n)/",
                "pronunciation_tip": "'bug' is borrowed English, pronounced roughly as in English; 'oplossen' "
                "has the guttural 'g' again.",
                "example_nl": "Ik moet deze bug voor vrijdag oplossen.",
                "example_en": "I need to fix this bug by Friday.",
                "usage_context": "Everyday engineering standup/ticket language.",
            },
            {
                "dutch": "de deadline halen",
                "english": "to make/hit the deadline",
                "ipa": "/də ˈdɛdlaɪn ˈɦaːlə(n)/",
                "pronunciation_tip": "'halen' -- long 'aa' sound, open your mouth wider than English 'a'.",
                "example_nl": "Denk je dat we de deadline gaan halen?",
                "example_en": "Do you think we'll make the deadline?",
                "usage_context": "Common in sprint planning and status updates.",
            },
            {
                "dutch": "de collega",
                "english": "the colleague",
                "ipa": "/də kɔˈleːɣaː/",
                "pronunciation_tip": "Stress on the second syllable: col-LE-ga.",
                "example_nl": "Mijn collega reviewt mijn code.",
                "example_en": "My colleague is reviewing my code.",
                "usage_context": "Neutral, professional term for a coworker.",
            },
            {
                "dutch": "Ik ben het niet mee eens",
                "english": "I disagree",
                "ipa": "/ɪk bɛn ət nit meː eːns/",
                "pronunciation_tip": "Softer and more indirect than it looks in English -- Dutch workplace "
                "disagreement is usually stated plainly but politely, not hedged excessively.",
                "example_nl": "Ik ben het niet mee eens, ik denk dat we een andere aanpak nodig hebben.",
                "example_en": "I disagree, I think we need a different approach.",
                "usage_context": "Direct but professional disagreement in a meeting or code review.",
            },
        ],
    },
]

WEEK_6_VOCAB_THEMES = [
    {
        "name": "Presentatie Geven",
        "items": [
            {
                "dutch": "Vandaag laat ik jullie zien...",
                "english": "Today I'll show you...",
                "ipa": "/vɑnˈdaːɣ laːt ɪk ˈjʏlə(n) zin/",
                "pronunciation_tip": "'jullie' -- the 'ui' diphthong again, round your lips gliding from 'y' to 'u'.",
                "example_nl": "Vandaag laat ik jullie zien wat we deze sprint bereikt hebben.",
                "example_en": "Today I'll show you what we achieved this sprint.",
                "usage_context": "Standard presentation opener.",
            },
            {
                "dutch": "het resultaat",
                "english": "the result",
                "ipa": "/ət reːzʏlˈtaːt/",
                "pronunciation_tip": "Stress on the last syllable: re-zul-TAAT.",
                "example_nl": "Het resultaat is beter dan verwacht.",
                "example_en": "The result is better than expected.",
                "usage_context": "Reporting outcomes in a work presentation.",
            },
            {
                "dutch": "Zijn er nog vragen?",
                "english": "Are there any questions?",
                "ipa": "/zɛin ər nɔx ˈvraːɣə(n)/",
                "pronunciation_tip": "'nog' has the guttural 'g'; 'vragen' too, at the end.",
                "example_nl": "Dat was mijn presentatie. Zijn er nog vragen?",
                "example_en": "That was my presentation. Are there any questions?",
                "usage_context": "Standard closing line before Q&A.",
            },
            {
                "dutch": "Goede vraag",
                "english": "Good question",
                "ipa": "/ˈɣuːdə vraːɣ/",
                "pronunciation_tip": "Two guttural 'g's back to back -- practice slowly.",
                "example_nl": "Goede vraag, laat me dat toelichten.",
                "example_en": "Good question, let me clarify that.",
                "usage_context": "Buys a moment to think when answering a question.",
            },
        ],
    },
]

WEEK_7_VOCAB_THEMES = [
    {
        "name": "Boodschappen Doen",
        "items": [
            {
                "dutch": "Hoeveel kost dit?",
                "english": "How much does this cost?",
                "ipa": "/huˈveːl kɔst dɪt/",
                "pronunciation_tip": "'hoe' is a long, closed 'oo' sound, similar to English 'who'.",
                "example_nl": "Hoeveel kost dit brood?",
                "example_en": "How much does this bread cost?",
                "usage_context": "Core shopping phrase, works anywhere.",
            },
            {
                "dutch": "Heeft u ... ?",
                "english": "Do you have ... ? (formal)",
                "ipa": "/ɦeːft y/",
                "pronunciation_tip": "Formal 'u' register -- appropriate with shopkeepers you don't know.",
                "example_nl": "Heeft u ook magere melk?",
                "example_en": "Do you also have low-fat milk?",
                "usage_context": "Asking a shop assistant if an item is available.",
            },
            {
                "dutch": "de boodschappen",
                "english": "the groceries",
                "ipa": "/də ˈboːtsxɑpə(n)/",
                "pronunciation_tip": "'sch' is pronounced 's-kh', not like English 'sh'.",
                "example_nl": "Ik doe zaterdag boodschappen.",
                "example_en": "I do the groceries on Saturday.",
                "usage_context": "General term for grocery shopping.",
            },
            {
                "dutch": "Mag ik contant/met kaart betalen?",
                "english": "May I pay cash/by card?",
                "ipa": "/mɑɣ ɪk kɔnˈtɑnt mɛt kaːrt bəˈtaːlə(n)/",
                "pronunciation_tip": "Most Dutch shops are card-first; cash is often less welcome -- good to ask.",
                "example_nl": "Mag ik met kaart betalen?",
                "example_en": "May I pay by card?",
                "usage_context": "At the register.",
            },
            {
                "dutch": "Doei! / Fijne dag!",
                "english": "Bye! / Have a nice day!",
                "ipa": "/duj fɛinə daːx/",
                "pronunciation_tip": "'Doei' is casual, used constantly in shops when leaving.",
                "example_nl": "Dank u wel, fijne dag nog!",
                "example_en": "Thank you, have a nice day!",
                "usage_context": "Casual goodbye after a purchase.",
            },
        ],
    },
]

WEEK_9_VOCAB_THEMES = [
    {
        "name": "Preken in de Kerk",
        "items": [
            {
                "dutch": "de gemeente",
                "english": "the congregation",
                "ipa": "/də ɣəˈmeːntə/",
                "pronunciation_tip": "Same word used for a municipality -- context makes the meaning clear.",
                "example_nl": "Welkom, gemeente, bij deze dienst.",
                "example_en": "Welcome, congregation, to this service.",
                "usage_context": "Addressing the congregation at the start of a service.",
            },
            {
                "dutch": "de preek houden",
                "english": "to give the sermon",
                "ipa": "/də preːk ˈɦaʊdə(n)/",
                "pronunciation_tip": "'preek' has a long, closed 'ee'.",
                "example_nl": "Vandaag houd ik de preek over vergeving.",
                "example_en": "Today I'm giving the sermon on forgiveness.",
                "usage_context": "Announcing the sermon topic.",
            },
            {
                "dutch": "Laten we bidden",
                "english": "Let us pray",
                "ipa": "/ˈlaːtə(n) ʋə ˈbɪdə(n)/",
                "pronunciation_tip": "'w' is close to English 'v' with rounded lips, not English 'w'.",
                "example_nl": "Laten we bidden voor deze gemeente.",
                "example_en": "Let us pray for this congregation.",
                "usage_context": "Transitioning into a prayer.",
            },
            {
                "dutch": "de zegen",
                "english": "the blessing",
                "ipa": "/də ˈzeːɣə(n)/",
                "pronunciation_tip": "'z' is voiced like English 'z'; 'g' guttural as usual.",
                "example_nl": "Ontvang de zegen en ga in vrede.",
                "example_en": "Receive the blessing and go in peace.",
                "usage_context": "Closing benediction of a service.",
            },
            {
                "dutch": "het Woord van God",
                "english": "the Word of God",
                "ipa": "/ət ʋoːrt vɑn ɣɔt/",
                "pronunciation_tip": "'Woord' -- long, closed 'oo', and the final 'd' devoices to a 't' sound.",
                "example_nl": "Laten we samen luisteren naar het Woord van God.",
                "example_en": "Let us listen together to the Word of God.",
                "usage_context": "Introducing a scripture reading.",
            },
        ],
    },
]

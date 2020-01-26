
bankTransforms = [

    [
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    [
        {"select": ['descendants']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    [
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    [
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['Action']]},
        "distinct",
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    [
        {"select": ['descendants']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['Action']]},
        "distinct",
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],

    [
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['Action']]},
        "distinct",
        {"select": ['ancestors']},
        {"select": ['referencesTo']},
        {"where": ['type:isIn', ['SoundBank']]},
        "distinct",
    ],
]
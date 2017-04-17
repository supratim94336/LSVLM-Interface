lms = [
    {
        'id' : 'AbsDiscLM',
        'name' : 'N-Gram (Absolute Discounting)',
        'fields' : [
            ("M", "N", "int", "The gram size to use for this LM."),
            ("Disc", "Disc", "float", "The weight given to this LM, between 0 and 1. (1 - Disc) weight will be given to the backoff LM."),
            ("BackOffLM", "Backoff LM", "lm"),
            ("Corpus", "Corpus", "corpus")
        ],
        'optional_fields' : [
            ("ShortHistLM", "ShortHistLM", "lm"),
            ("FallBackLM", "FallBackLM", "lm")
        ]
    },{
        'id' : 'Dirichlet',
        'name' : 'Dirichlet',
        'fields' : [
            ("M", "N", "int", "The gram size to use for this LM."),
            ("mu", "mu", "float", "I don't know what this does."),
            ("BackOffLM", "Backoff LM", "lm"),
            ("Corpus", "Corpus", "corpus")   
        ],
        'optional_fields': [
            ("ShortHistLM", "ShortHistLM", "lm"),
            ("FallBackLM", "FallBackLM", "lm")
        ]
    },{
        'id' : 'Linear',
        'name' : 'Linear',
        'fields' : [
            ("LMs", "LMs", "lm-many", "Mix multiple LMs together. For each LM, set a weight between 0 and 1.")
        ],
        'optional_fields': [
            ("ShortHistLM", "ShortHistLM", "lm"),
            ("FallBackLM", "FallBackLM", "lm")
        ]
    },{
        'id' : 'LogLinear',
        'name' : 'Log-linear',
        'fields' : [
            ("LMs", "LMs", "lm-many", "Mix multiple LMs together. For each LM, set a weight between 0 and 1.")
        ],
        'optional_fields': [
            ("ShortHistLM", "ShortHistLM", "lm"),
            ("FallBackLM", "FallBackLM", "lm")
        ]
#    },{
#        'id' : 'NGram',
#        'name': 'N-Gram',
#        'fields' : [
#            ("M", "int"),
#            ("C", "int"),
#            ("BackOffLM", "lm"),
#            ("Corpus", "corpus")
#        ]
    },{ 'id' : 'ZeroLM',
    'name' : 'Zero LM',
    'fields' : [
            ("Corpus", "Corpus", "corpus", "For this language model, the probability of any word will be the reciprocal of the number of unique words in this corpus")
        ]}
]

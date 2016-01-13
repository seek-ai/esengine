from esengine.utils.payload.meta import BaseSuggester, MetaSuggester
from esengine.utils.payload.exception import NoSuggester

SUGGESTERS = {
    'term': {
        'args': ('field', ),
        'kwargs': ('analyzer', 'size', 'sort', 'suggest_mode')
    },
    'phrase': {
        'args': ('field', ),
        'kwargs': (
            'gram_size', 'real_word_error_likelihood', 'confidence',
            'max_errors', 'separator', 'size', 'analyzer', 'shard_size',
            'collate'
        )
    },
    'completion': {
        'args': ('field', ),
        'kwargs': ('size', )
    }
}


class Suggester(BaseSuggester):
    __metaclass__ = MetaSuggester

    _ee_type = 'suggester'
    _definitions = SUGGESTERS
    _exception = NoSuggester

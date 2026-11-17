import copy
import hashlib
import unittest

from generate import exclusion, parse_registry, render, validate

REGISTRY = '''File-Date: 2026-01-01
%%
Type: language
Subtag: en
Description: English
Description: Another name
  continued
%%
Type: language
Subtag: zz
Description: Example
%%
Type: language
Subtag: old
Description: Old code
Deprecated: 2000-01-01
Preferred-Value: en
%%
Type: language
Subtag: qaa..qtz
Description: Private use
Scope: private-use
%%
Type: script
Subtag: Latn
Description: Latin
'''
DATA = {'schema_version': 2, 'sources': {'example': {'reference': 'https://example.org/name', 'description': 'Test source'}},
        'languages': [{'code': 'en', 'endonym': 'English', 'sources': ['example']}]}


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.records = {r['Subtag'][0]: r for r in parse_registry(REGISTRY)}

    def test_registry_preserves_repeated_fields_and_continuations(self):
        self.assertEqual(self.records['en']['Description'], ['English', 'Another name continued'])
        self.assertNotIn('Latn', self.records)

    def test_exclusions(self):
        self.assertEqual(exclusion(self.records['old']), 'deprecated')
        self.assertEqual(exclusion(self.records['qaa..qtz']), 'private_use_range')
        for scope in ['special', 'collection']:
            self.assertEqual(exclusion({'Subtag': ['abc'], 'Scope': [scope]}), scope)
        self.assertIsNone(exclusion({'Subtag': ['abc'], 'Scope': ['macrolanguage']}))

    def test_rejects_invalid_source_duplicate_and_excluded_records(self):
        for change in ['source', 'duplicate', 'excluded', 'empty', 'multiple', 'status']:
            with self.subTest(change=change):
                data = copy.deepcopy(DATA)
                entry = data['languages'][0]
                if change == 'source':
                    entry['sources'] = ['missing']
                elif change == 'duplicate':
                    data['languages'].append(copy.deepcopy(entry))
                elif change == 'excluded':
                    entry['code'] = 'old'
                elif change == 'empty':
                    entry['endonym'] = ''
                elif change == 'multiple':
                    entry['endonym'] = ['English', 'Another name']
                else:
                    entry['status'] = 'verified'
                with self.assertRaises(ValueError):
                    validate(data, self.records)

    def test_project_history_is_a_valid_reference(self):
        data = copy.deepcopy(DATA)
        data['sources']['example']['reference'] = 'git:original'
        self.assertIn('en', validate(data, self.records))

    def test_report_accounts_for_gaps_and_exclusions(self):
        raw = REGISTRY.encode()
        meta = {'file_date': '2026-01-01', 'sha256': hashlib.sha256(raw).hexdigest()}
        import json
        outputs = render(raw, meta, DATA)
        report = json.loads(outputs['data/coverage.json'])
        self.assertEqual(report['eligible_languages'], 2)
        self.assertEqual(report['missing_endonyms'], 1)
        self.assertNotIn('statuses', report)
        by_code = {r['code']: r for r in report['records']}
        self.assertFalse(by_code['zz']['lookup_available'])
        self.assertIsNone(by_code['zz']['excluded'])
        self.assertEqual(by_code['old']['excluded'], 'deprecated')
        self.assertEqual(report['lookup_entries'], 1)
        self.assertEqual(len(report['records']), 4)
        self.assertEqual(outputs, render(raw, meta, DATA))
        with self.assertRaises(ValueError):
            render(raw + b'\n', meta, DATA)

    def test_diacritics_are_preserved_exactly(self):
        raw = REGISTRY.encode()
        metadata = {'file_date': '2026-01-01', 'sha256': hashlib.sha256(raw).hexdigest()}
        for name in ['עִבְרִית', 'الْعَرَبِيَّة', 'Latīna', 'ру́сский', 'Lati\u0304na', 'bòsanskī', 'hr̀vātskī', 'ср̏пскӣ', 'slovẹ́nščina']:
            with self.subTest(name=name):
                data = copy.deepcopy(DATA)
                data['languages'][0]['endonym'] = name
                generated = render(raw, metadata, data)['src/generated.rs']
                self.assertIn(f'=> "{name}"', generated)


if __name__ == '__main__':
    unittest.main()

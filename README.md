# glossonymata

A Rust lookup of personally preferred language endonyms, keyed by ICU4X base
language subtags. Each language has one chosen spelling. Preferences include
niqqud for Hebrew, taškīl for Arabic, vowel-length macrons for Latin, and stress
or pitch accents. Prefer full dictionary accent notation for words, including
pitch, vowel length, and vowel-quality marks where supplied, rather than reducing
them to stress-only acute accents. These marks are part of the returned string,
with no separate annotated form or diacritic-removal mode.

```rust
use glossonymata::endonym;
use icu_locale_core::subtags::language;

assert_eq!(endonym(language!("he")), Some("עִבְרִית"));
assert_eq!(endonym(language!("ar")), Some("الْعَرَبِيَّة"));
assert_eq!(endonym(language!("la")), Some("Latīna"));
assert_eq!(endonym(language!("ru")), Some("ру́сский"));
assert_eq!(endonym(language!("zz")), None);
```

Spellings reflect personal preferences rather than a claim of a single universal
endonym. Diacritics are curated per language, never automatically added, stripped,
or normalized. Some existing entries have not yet been adjusted to these
preferences. The lookup does not canonicalize aliases or select variants by
script or region. Unsupported and excluded codes return `None`.

## Coverage checklist

The pinned IANA Language Subtag Registry supplies the checklist, not the preferred
names. All `Type: language` records are accounted for. Macrolanguages are included;
collections, special codes, deprecated subtags, and private-use ranges are
explicitly excluded. Unregistered codes are outside the target.

See [the coverage summary](data/coverage.md) and [the complete checklist](data/coverage.json).
Coverage measures whether a preferred endonym has been selected. A missing name
is a curation gap; there are no verification tiers or review-status gates.

## Editing names

Edit `data/endonyms.json`. Each language record has exactly three fields:

```json
{
  "code": "la",
  "endonym": "Latīna",
  "sources": ["wiktionary-la"]
}
```

`endonym` is the exact spelling returned by the lookup. `sources` references keys
in the top-level source map, whose entries contain `reference` and `description`.
References are reading material and provenance for the choice, not approval
requirements. They can be dictionary URLs, upstream data references, or project
history. Entries still referencing `legacy-table` retain the original project provenance;
its per-name references were not recorded. See [curation notes](data/curation.md)
for the choices made so far and the remaining work.

To change a preference, replace the single `endonym` value and update its
references as needed. No alternate-name arrays, script metadata, or annotation
flags are required. Record stress and vowel points directly in the string.

Regenerate and check with Python 3 (standard library only):

```sh
python3 scripts/generate.py
python3 scripts/generate.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
cargo test --locked
```

The generator validates unique eligible codes, nonempty names, and source
references. It preserves Unicode spelling exactly. CI checks generated files
against the inputs. Cargo builds use checked-in Rust and need neither Python
nor network access.

## Updating the checklist

`data/language-subtag-registry.txt` is the unmodified IANA snapshot;
`data/registry.json` records its upstream URL, file date, and SHA-256 digest.
To update, replace the snapshot and update its metadata, regenerate, and inspect
the checklist diff. Curated entries that become deprecated must be removed or
moved to a replacement after choosing the appropriate name. Old choices remain
in version history. No registry downloads happen during builds.

`src/generated.rs`, `data/coverage.json`, and `data/coverage.md` are generated;
edit the source data instead.

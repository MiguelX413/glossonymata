# Curation notes

The lookup holds one personal choice per language. These notes explain editorial
choices; they do not add review tiers to the schema or gate lookup availability.

## Source pass

The initial source pass used the official [CLDR 48 core archive](https://unicode.org/Public/cldr/48/core.zip).
250 existing spellings exactly matched explicit self-names in their own locales;
those records now cite the individual release-48 XML files. Another 49 eligible
languages had explicit self-names and were added. Names inherited from an English
fallback were not imported. The Norwegian written standards were checked in the
shared Norwegian locale. Existing capitalization was retained for Abkhaz,
Guarani, Haitian Creole, and Navajo, with that adjustment noted in the references.
Some Chinese written names cite the Traditional Chinese locale; those references
support the written labels, not local spoken pronunciations.

## Spelling choices

Full dictionary accent notation is the standing preference for words: retain
pitch, vowel-length, and vowel-quality marks where the reference supplies them.

- Hebrew and Arabic retain the previously selected pointed forms.
- Latin retains its vowel-length macron.
- Belarusian, Bulgarian, Ukrainian, and standard Macedonian now show stress
  with an acute, following the relevant language sections of their dictionary
  references. The Bulgarian word for Macedonian and a common nonstandard
  Macedonian stress pattern were deliberately not substituted for the standard
  Macedonian endonym.
- Urdu uses the dictionary's vowel-marked اُرْدُو.
- Lithuanian uses the dictionary form lietùvių, keeping its stress mark.
- Chewa uses Chicheŵá, retaining the existing Chewa rather than Nyanja naming
  choice and adding the dictionary's consonant and tone marks.
- Kurdish uses kurdî. The old bracketed Kurmanji qualifier was editorial metadata,
  so it was removed from the endonym itself.
- Old English retains Ænglisċ: the dictionary explicitly lists it as an alternative
  to Englisċ. The palatalization dot remains.
- Dhivehi retains its supported short name rather than expanding it to a compound.
- Classical Syriac remains unpointed. The consulted entry's pointed Assyrian
  Neo-Aramaic headword was not copied into the Classical Syriac record.

Per-language references and explanations are in [endonyms.json](endonyms.json).

## Resolved preferences

Coptic uses the Bohairic form ϯⲙⲉⲧⲣⲉⲙⲛ̀ⲭⲏⲙⲓ from CLDR, as explicitly selected.
The full dictionary accent preference has been applied to the four pending names:

| Language | Preferred form | Notation |
| --- | --- | --- |
| Bosnian | bòsanskī | Rising pitch accent and vowel length |
| Croatian | hr̀vātskī | Rising pitch on syllabic r and vowel lengths |
| Serbian | ср̏пскӣ | Falling pitch on syllabic r and vowel length; Cyrillic retained |
| Slovenian | slovẹ́nščina | Tonal accent and close-e vowel-quality mark |

The dictionary language-noun headwords supply these forms. The simpler non-tonal
Slovenian declension spelling is not used as a replacement for its full headword.

## Nahuan names

Classical Nahuatl (`nci`) uses nāhuatlahtōlli, retaining the dictionary's long-vowel
macrons and saltillo h. Pipil/Nawat (`ppl`) retains Nāwat and now has a specific
dictionary reference supporting its long initial vowel. These are different
languages; their forms are not copied indiscriminately to other Nahuan codes.

Modern Mexican Nahuan varieties need variety-specific names and length evidence.
[INALI's catalogue](https://www.inali.gob.mx/sitios/clin-inali/html/l_nahuatl.html)
records multiple self-designations, and its categories need to be matched carefully
to the IANA inventory. The collection code `nah` remains outside the project's
individual-language checklist. Orthographic length markers and saltillo notation
are preserved from each selected reference rather than inferred from a generic
Spanish label or substituted between varieties.

## Remaining work

This is a first curation pass, not exhaustive linguistic research. There are 383
selected names. Of those, 63 still have only their original `legacy-table`
reference, including several historical languages and smaller language varieties.
Their values have been retained rather than guessing at pronunciation, historical
spelling, or vowel pointing. The names with new references also may admit further
pronunciation marks; a CLDR spelling match does not resolve every accent choice.

The [coverage checklist](coverage.md) separately reports eligible languages still
missing a chosen endonym. Counts there are generated from the data.

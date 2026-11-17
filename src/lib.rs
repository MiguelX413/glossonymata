//! Personally curated endonyms keyed by ICU4X base language subtags.
//!
//! Each language has one preferred spelling, which may include vowel points,
//! vowel-length macrons, or stress accents. Diacritics are returned as stored.
//! IANA supplies the coverage checklist; references document spelling choices.

use icu_locale_core::subtags::Language;

/// Returns the project's preferred endonym for a base language subtag.
///
/// See `data/endonyms.json` for spellings and references and `data/coverage.md`
/// for coverage. No alias canonicalization or diacritic removal is performed.
/// Unsupported or excluded subtags return `None`.
pub fn endonym(language: Language) -> Option<&'static str> {
    generated::lookup(language.as_str())
}

mod generated;

#[cfg(test)]
mod tests {
    use super::endonym;
    use icu_locale_core::subtags::language;

    #[test]
    fn returns_representative_endonyms() {
        let cases = [
            (language!("ar"), "الْعَرَبِيَّة"),
            (language!("he"), "עִבְרִית"),
            (language!("la"), "Latīna"),
            (language!("ru"), "ру́сский"),
            (language!("chr"), "ᏣᎳᎩ"),
            (language!("en"), "English"),
            (language!("jje"), "제줏말"),
            (language!("nv"), "Diné bizaad"),
            (language!("pal"), "𐭯𐭠𐭫𐭮𐭩𐭪"),
            (language!("sux"), "𒅴𒂠"),
        ];

        for (language, expected) in cases {
            assert_eq!(endonym(language), Some(expected));
        }
    }

    #[test]
    fn distinguishes_related_language_subtags() {
        assert_eq!(endonym(language!("nb")), Some("norsk bokmål"));
        assert_eq!(endonym(language!("nn")), Some("norsk nynorsk"));
        assert_eq!(endonym(language!("no")), Some("norsk"));

        assert_eq!(endonym(language!("lzh")), Some("文言"));
        assert_eq!(endonym(language!("yue")), Some("粵語"));
        assert_eq!(endonym(language!("zh")), Some("中文"));
    }

    #[test]
    fn returns_none_for_unmapped_languages() {
        for language in [language!("ams"), language!("ryn"), language!("zz")] {
            assert_eq!(endonym(language), None);
        }
    }
}

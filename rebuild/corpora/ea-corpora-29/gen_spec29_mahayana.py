#!/usr/bin/env python3
"""Writes spec29-buddhist-sanskrit.json (29/09) and spec29-east-asian-buddhism.json (29/10)."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
GT = "https://gretil.sub.uni-goettingen.de/gretil/corpustei/"
NC = "CC BY-NC-SA 4.0, stated in the file's <licence>"
SEAT = {"spine": "EA-CORPORA-29", "ruling": "The author's direction of 2026-10-28: 'we need buddhist canon, various traditions, mahayana included.'", "seating": "EA-CORPORA-29", "fetched": "2026-10-28"}

# ---------- 29/09 Sanskrit ----------
S = [
 ("Mahāyāna sūtra", "saddharmapundarika", "sa_saddharmapuNDarIkasUtra.xml", "Saddharmapuṇḍarīkasūtra (the Lotus Sūtra)", "saddharmapuṇḍarīka"),
 ("Mahāyāna sūtra", "astasahasrika", "sa_aSTasAhasrikA-prajJApAramitA.xml", "Aṣṭasāhasrikā Prajñāpāramitā (the Perfection of Wisdom in 8,000 Lines)", "prajñāpāramitā"),
 ("Mahāyāna sūtra", "vajracchedika", "sa_vajracchedikA-prajJApAramitA.xml", "Vajracchedikā Prajñāpāramitā (the Diamond Sūtra)", "evaṃ mayā śrutam"),
 ("Mahāyāna sūtra", "prajnaparamitahrdaya", "sa_prajJApAramitAhRdayasUtra.xml", "Prajñāpāramitāhṛdayasūtra (the Heart Sūtra)", "śūnyatā"),
 ("Mahāyāna sūtra", "lankavatara", "sa_saddharmalaGkAvatArasUtra.xml", "Saddharmalaṅkāvatārasūtra", "laṅkāvatār"),
 ("Mahāyāna sūtra", "vimalakirtinirdesa", "sa_vimalakIrtinirdeza.xml", "Vimalakīrtinirdeśa", "vimalakīrti"),
 ("Mahāyāna sūtra", "gandavyuha", "sa_gaNDavyUhasUtra.xml", "Gaṇḍavyūhasūtra", "sudhana"),
 ("Mahāyāna sūtra", "samadhiraja", "sa_samAdhirAjasUtra.xml", "Samādhirājasūtra", "samādhirāj"),
 ("Mahāyāna sūtra", "sukhavativyuha", "sa_sukhAvatIvyUha.xml", "Sukhāvatīvyūha (the larger)", "sukhāvatī"),
 ("Mahāyāna sūtra", "smaller-sukhavativyuha", "sa_smaller-sukhAvatIvyUha.xml", "Sukhāvatīvyūha (the smaller)", "amitāyu"),
 ("Mahāyāna sūtra", "karandavyuha", "sa_kAraNDavyUha.xml", "Kāraṇḍavyūha", "avalokiteśvar"),
 ("Mahāyāna sūtra", "suvarnaprabhasa", "sa_suvarNaprabhAsasUtra.xml", "Suvarṇaprabhāsasūtra (the Golden Light)", "suvarṇaprabhās"),
 ("Mahāyāna sūtra", "kasyapaparivarta", "sa_kAzyapaparivartasUtra.xml", "Kāśyapaparivarta", "kāśyap"),
 ("Mahāyāna sūtra", "lalitavistara", "sa_lalitavistara.xml", "Lalitavistara", "lalitavistar"),
 ("Śāstra", "nagarjuna-mulamadhyamakakarika", "sa_nAgArjuna-mUlamadhyamakakArikA.xml", "Nāgārjuna, Mūlamadhyamakakārikā", "na svato nāpi parato na dvābhyāṃ"),
 ("Śāstra", "nagarjuna-vigrahavyavartani", "sa_nAgArjuna-vigrahavyAvartanI.xml", "Nāgārjuna, Vigrahavyāvartanī", "svabhāv"),
 ("Śāstra", "nagarjuna-ratnavali", "sa_nAgArjuna-ratnAvalI.xml", "Nāgārjuna, Ratnāvalī", "dharm"),
 ("Śāstra", "madhyamakavatara", "sa_madhyamakAvatAra-1-5.xml", "Candrakīrti, Madhyamakāvatāra, chapters 1–5", "bodhisattv"),
 ("Śāstra", "santideva-bodhicaryavatara", "sa_zAntideva-bodhicaryAvatAra.xml", "Śāntideva, Bodhicaryāvatāra", "sugatān"),
 ("Śāstra", "santideva-siksasamuccaya", "sa_zAntideva-zikSAsamuccaya.xml", "Śāntideva, Śikṣāsamuccaya", "śikṣā-samuccayaḥ"),
 ("Śāstra", "asanga-mahayanasutralamkara", "sa_asaGga-mahAyAnasUtrAlaMkAra.xml", "Mahāyānasūtrālaṃkāra (ascribed to Maitreya/Asaṅga)", "mahāyān"),
 ("Śāstra", "maitreya-madhyantavibhaga", "sa_maitreya-madhyAntavibhAgakArikA.xml", "Madhyāntavibhāgakārikā (ascribed to Maitreya)", "abhūtaparikalp"),
 ("Śāstra", "ratnagotravibhaga", "sa_ratnagotravibhAga.xml", "Ratnagotravibhāga", "tathāgatagarbh"),
 ("Śāstra", "abhisamayalamkara", "sa_abhisamayAlaMkAra.xml", "Abhisamayālaṃkāra", "prajñāpāramit"),
 ("Śāstra", "vasubandhu-trimsika", "sa_vasubandhu-triMzikAvijJaptikArikA.xml", "Vasubandhu, Triṃśikā Vijñaptimātratā", "vijñapti"),
 ("Śāstra", "vasubandhu-abhidharmakosa", "sa_vasubandhu-abhidharmakoza.xml", "Vasubandhu, Abhidharmakośa (the kārikās)", "abhidharm"),
 ("Kāvya and narrative", "asvaghosa-buddhacarita", "sa_azvaghoSa-buddhacarita.xml", "Aśvaghoṣa, Buddhacarita", "śākya"),
 ("Kāvya and narrative", "asvaghosa-saundarananda", "sa_azvaghoSa-saundarAnanda.xml", "Aśvaghoṣa, Saundarananda", "nand"),
 ("Kāvya and narrative", "aryasura-jatakamala", "sa_AryazUra-jAtakamAlA.xml", "Āryaśūra, Jātakamālā", "bodhisattv"),
 ("Kāvya and narrative", "divyavadana", "sa_divyAvadAna.xml", "Divyāvadāna", "bhikṣav"),
 ("Kāvya and narrative", "mahavastu", "sa_mahAvastu-avAdana.xml", "Mahāvastu", "bhagavā"),
 ("Kāvya and narrative", "udanavarga", "sa_udAnavarga.xml", "Udānavarga", "apramād"),
]
items, loci = [], []
for cls, slug, f, work, find in S:
    items.append({"kind": "gretil", "slug": slug, "work": f"{work} — GRETIL TEI ({f})", "class": cls, "url": GT + f, "path": f,
                  "source": "GRETIL (Göttingen Register of Electronic Texts in Indian Languages)", "licence": NC})
    loci.append({"label": work, "text": f"text/{slug}.txt", "find": find})
sk = {"corpus": "buddhist-sanskrit", "seat": "EA-CORPORA-29/09",
 "title": "The Buddhist Canon in Sanskrit: the Mahāyāna sūtras, the śāstras of Madhyamaka and Yogācāra, and the kāvya and avadāna literature (GRETIL)",
 "language": "san",
 "license": {"payload": "GRETIL TEI files, each CC BY-NC-SA 4.0 at the file: handled under the NC payload/record split ruled at EA-CORPORA-02, the NonCommercial payload licence carried forward unmodified and not attaching to this seat record. The underlying texts are ancient; the editions GRETIL transcribes are named in each file's teiHeader.",
             "record": "CC-BY-4.0 applies to this seat record only."},
 "normalization": "The TEI as fetched under original/; text/<slug>.txt the TEI <body> reduced by code, one line per <l> or <p>, a blank line after each <lg>, headings marked '=== ==='; notes dropped from the text layer and kept in the TEI.",
 "units": "one text file per work; each work carries its genre as class", "items": items, "loci": loci,
 "classes": ["Mahāyāna sūtra", "Śāstra", "Kāvya and narrative"],
 "cross_references": {"already_on_the_shelf": "The Pali Tipiṭaka (29/08) and the Dhammapada (02/17); the Chinese, Korean and Japanese canons (29/10); the Derge Kangyur selection (29/11). The Sanskrit poetics of ars-poetica (29/04) come from the same repository."},
 "scope": "Thirty-two works: fourteen Mahāyāna sūtras (the Lotus, the Perfection of Wisdom in 8,000 lines, the Diamond and the Heart, the Laṅkāvatāra, the Vimalakīrti, the Gaṇḍavyūha, the Samādhirāja, both Sukhāvatīvyūhas, the Kāraṇḍavyūha, the Golden Light, the Kāśyapaparivarta, the Lalitavistara); twelve śāstras (Nāgārjuna, Candrakīrti, Śāntideva, the Maitreya texts, the Ratnagotravibhāga, Vasubandhu); and six works of kāvya and narrative (Aśvaghoṣa, Āryaśūra, the Divyāvadāna, the Mahāvastu, the Udānavarga).",
 "why_seated": "At the author's direction of 2026-10-28 for the twenty-ninth seating: the Buddhist canon in its several traditions, Mahāyāna included, each in the language of its own canon.",
 } | SEAT | {"spine": "29/09"}
(HERE / "spec29-buddhist-sanskrit.json").write_text(json.dumps(sk, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# ---------- 29/10 East Asian ----------
E, el = [], []
def ws(cls, slug, work, find, lang="zh", title=None, titles=None):
    it = {"kind": "ws", "slug": slug, "work": work, "class": cls, "lang": lang}
    if titles: it["titles"] = titles
    else: it["title"] = title
    E.append(it); el.append({"label": work.split(" — ")[0], "text": f"text/{slug}.txt", "find": find})
ws("Chinese canon", "miaofa-lianhua-jing", "《妙法蓮華經》 (the Lotus Sūtra), Kumārajīva's translation (406), twenty-eight chapters, as in the Taishō canon (T 262) — Chinese Wikisource", "如是我聞", titles=[f"妙法蓮華經/{i:02d}" for i in range(0, 29)])
ws("Chinese canon", "jingang-jing", "《金剛般若波羅蜜經》 (the Diamond Sūtra), Kumārajīva's translation — Chinese Wikisource", "應無所住而生其心", title="金剛般若波羅蜜經 (鳩摩羅什)")
ws("Chinese canon", "xin-jing", "《般若波羅蜜多心經》 (the Heart Sūtra), Xuanzang's translation (649) — Chinese Wikisource", "色不異空", title="般若波羅蜜多心經 (玄奘譯)")
ws("Chinese canon", "weimojie-jing", "《維摩詰所說經》 (the Vimalakīrti Sūtra), Kumārajīva's translation, fourteen chapters (T 475) — Chinese Wikisource", "維摩詰", titles=[f"維摩詰所說經/{i:02d}" for i in range(1, 15)])
ws("Chinese canon", "amituo-jing", "《佛說阿彌陀經》 (the smaller Sukhāvatīvyūha), Kumārajīva's translation — Chinese Wikisource", "極樂", title="佛說阿彌陀經")
ws("Chinese canon", "sishierzhang-jing", "《四十二章經》 (the Sūtra in Forty-Two Sections), the Taishō text — Chinese Wikisource", "辭親出家", title="四十二章經 (大正新脩大藏經譯本)")
ws("Chinese canon", "fo-yijiao-jing", "《佛遺教經》 (the Sūtra of the Teaching Bequeathed by the Buddha), Kumārajīva's translation — Chinese Wikisource", "波羅提木叉", title="佛遺教經")
ws("Chinese canon", "dasheng-qixin-lun", "《大乘起信論》 (the Awakening of Faith in the Mahāyāna), Paramārtha's version, the transcription marked incomplete by Wikisource — Chinese Wikisource", "夫起信論者", title="大乘起信論 (真諦)")
ws("Chinese canon", "zhao-lun", "僧肇《肇論》 (the Treatises of Sengzhao), the preface, the Zongben yi and the four treatises — Chinese Wikisource", "物不遷", titles=["肇論/序", "肇論/宗本義", "肇論/1", "肇論/2", "肇論/3", "肇論/4", "肇論/5"])
ws("Chan", "liuzu-tanjing", "《六祖大師法寶壇經》 (the Platform Sūtra of the Sixth Patriarch), the Zongbao recension, in simplified characters as transcribed — Chinese Wikisource", "菩提本无树", title="六祖大師法寶壇經")
ws("Chan", "xinxin-ming", "僧璨《信心銘》 (Inscription on Faith in Mind), as in the Jingde chuandeng lu, juan 30 — Chinese Wikisource", "至道無難", title="信心銘")
ws("Chan", "zhengdao-ge", "玄覺《永嘉證道歌》 (Song of Realizing the Way) — Chinese Wikisource", "絕學無為閑道人", title="永嘉證道歌")
ws("Chan", "linji-lu", "《鎮州臨濟慧照禪師語錄》 (the Record of Linji), compiled by Huiran (T 1985) — Chinese Wikisource", "隨處作主", title="鎮州臨濟慧照禪師語錄")
ws("Chan", "biyan-lu", "圜悟克勤《碧巖錄》 (the Blue Cliff Record, 1125), the preface and ten juan — Chinese Wikisource", "廓然無聖", titles=["碧巖錄/序"] + [f"碧巖錄/卷第{n}" for n in "一二三四五六七八九十"])
ws("Chan", "wumen-guan", "無門慧開《無門關》 (the Gateless Barrier, 1228) — Chinese Wikisource", "趙州狗子", title="無門關")
ws("Japan", "tannisho-iyaku", "『歎異抄』 (the Tannishō), in the rendering of 意訳聖典 (Kyoto: Honganji, 1923) — Japanese Wikisource", "彌陀", lang="ja", title="歎異抄 (意訳聖典)")
ws("Japan", "honen-shichikajo-kishomon", "法然『七箇條の起請文』 (Hōnen, the Seven-Article Pledge, 1204), as in the Jōdoshū zensho — Japanese Wikisource", "念仏", lang="ja", title="七箇條の起請文 (浄土宗全書)")
ws("Japan", "hakuin-yasenkanna", "白隠『夜船閑話』 (Hakuin, Idle Talk on a Night Boat, 1757) — Japanese Wikisource", "白幽", lang="ja", title="夜船閑話")
ws("Japan", "hannya-shingyo-ja", "『般若心経』 (the Heart Sūtra) as received in Japan, Xuanzang's text with the Japanese reading — Japanese Wikisource", "色即是空", lang="ja", title="般若心経")
NIM = json.load(open("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/nim.json", encoding="utf-8"))
ws("Korea", "han-yongun-nimui-chimmuk", "한용운 『님의 沈默』 (Han Yong-un, The Silence of Love; Seoul: 회동서관, 1926), the preface, the eighty-eight poems and the afterword, in the spelling of 1926 — Korean Wikisource", "님은갓슴니다", lang="ko", titles=NIM)
ea = {"corpus": "east-asian-buddhism", "seat": "EA-CORPORA-29/10",
 "title": "The Mahāyāna in East Asia: the Chinese canon (the Lotus, the Diamond, the Heart, the Vimalakīrti), Chan from the Platform Sūtra to the Gateless Barrier, the Tannishō, Hōnen and Hakuin, and Han Yong-un's The Silence of Love",
 "language": "mul",
 "license": {"payload": "Wikisource transcriptions under CC BY-SA 4.0 for the site's contributions; the texts are classical (the Chinese canon, Chan records, Kamakura and Edo Japanese works) or first published before 1931 (Han Yong-un, 1926; the 意訳聖典 rendering, 1923), in the public domain in the United States.",
             "record": "CC-BY-4.0 applies to this seat record only."},
 "normalization": "Wikisource pages as served under original/, each with its revision id; text/<slug>.txt the parser output reduced by code, several pages of one work joined under '=== <title> ===' headings. Nothing corrected.",
 "units": "one text file per work; each work carries its tradition as class", "items": E, "loci": el,
 "classes": ["Chinese canon", "Chan", "Japan", "Korea"],
 "cross_references": {"already_on_the_shelf": "The Sanskrit originals of the Lotus, the Diamond, the Heart, the Vimalakīrti and the Sukhāvatīvyūha (29/09); the Tibetan of the same sūtras (29/11); the Pali Tipiṭaka (29/08); Yi Illo's Pahanjip (29/04)."},
 "queued": ["Dōgen, Shōbōgenzō and the Shōbōgenzō zuimonki: no transcription found this session (Aozora Bunko holds neither; the Japanese Wikisource page for the Zuimonki's first book serves no text)", "Shinran, Kyōgyōshinshō, and the Tannishō in its Kamakura text: the Tannishō is seated in the 1923 rendering", "Chinul, Susimgyeol (修心訣), and Wŏnhyo, Palsim suhaeng chang (發心修行章): not found on Korean or Chinese Wikisource", "The Taishō canon entire: CBETA's text is CC BY-NC-SA; a route to be ruled, not seated here"],
 "scope": "Twenty works: nine of the Chinese canon (the Lotus in twenty-eight chapters, the Diamond, the Heart, the Vimalakīrti, the smaller Sukhāvatīvyūha, the Forty-Two Sections, the Bequeathed Teaching, the Awakening of Faith, Sengzhao); six of Chan (the Platform Sūtra, the Xinxin ming, the Zhengdao ge, the Record of Linji, the Blue Cliff Record, the Gateless Barrier); four of Japan (the Tannishō, Hōnen, Hakuin, the Heart Sūtra as read in Japan); and Korea's The Silence of Love (1926).",
 "why_seated": "At the author's direction of 2026-10-28 for the twenty-ninth seating: the Buddhist canon in its several traditions, Mahāyāna included.",
 } | SEAT | {"spine": "29/10"}
(HERE / "spec29-east-asian-buddhism.json").write_text(json.dumps(ea, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(items), "sanskrit;", len(E), "east asian (Korea added after the subpage list)")

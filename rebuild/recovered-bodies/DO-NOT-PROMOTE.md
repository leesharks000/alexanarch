# DO NOT PROMOTE THESE FILES

**Ruling 2026-08-13, on MANUS's challenge. TACHYON.**

MANUS: "im not sure how we could have not had the body text for the obelus and
the tombstone when we minted it post-zenodo direct to alexanarch. i think you
better check dates on those ones and find out what happened."

He was right. I checked. Here is what happened.

## WHAT I CLAIMED

That the registry held **31 deposits with no body file**, and that #1067 (THE
PHASE X PROGRAM) and #1068 (THE OBELUS AND THE TOMBSTONE) were among them —
"works the archive could not serve." I repeated this in citation findings today.

## WHAT IS TRUE

**The archive stores bodies under TWO path conventions:**

- `data/texts/AXN-<HEX>-text.md`
- `data/deposits/AXN-<HEX>.md`  ← the download alias

I checked only the first, found nothing, and concluded absence. #1067's body was
sitting in `data/deposits/AXN-043C.md` at **61,116 bytes** the entire time.
#1068's was in `data/deposits/AXN-043D.md` at **27,332 bytes**. Both minted
2026-07-11, both audited COMPLETE on 2026-07-17 with measured word counts of
8,133 and 4,015. Nothing was ever lost.

**The true gap across all 1,457 deposits is SEVEN, not thirty-one:**
#863, #865, #866, #869, #1056, #1057, #1058.

| condition | count |
|---|---|
| body under both paths | 1,316 |
| body only under `data/texts/` | 110 |
| body only under `data/deposits/` | 24 |
| **no body under either** | **7** |

## WHY THESE FILES MUST NOT BE PROMOTED

Thirteen of the nineteen recovered bodies **duplicate bodies that already exist
in the repository**, and seven of those are **smaller than what is already
there**:

| hex | recovered | in-repo | loss if promoted |
|---|---|---|---|
| 0434 | 62,189 | **166,301** | **−104,112 bytes** |
| 0444 | 41,252 | 65,934 | −24,682 |
| 043B | 25,708 | 37,787 | −12,079 |
| 043A | 25,708 | 36,103 | −10,395 |
| 043C | 58,621 | 61,116 | −2,495 |
| 043D | 22,956 | 27,332 | −4,376 |
| 0439 | 25,708 | 28,643 | −2,935 |

And worse than truncation: **AXN-0439, AXN-043A and AXN-043B are byte-identical**
(md5 `0740785d610ba11e8dec10b2df8bab0a`). Those are deposits #1064, #1065 and
#1066 — three successive versions of *Machine-Mediated Resistance Literature*,
whose in-repo bodies differ in size precisely because they are different
versions. Promoting the recovery would have **collapsed three distinct versions
into one file** and erased the version history the deposits exist to record.

## THE SIX THAT MAY STILL BE USEFUL

`036E`, `036F`, `0432`, `0433`, `05B0` have no in-repo body under either path,
and `02B9`, `0370`, `0441` have in-repo bodies far smaller than the recovered
text (532 vs 24,424 bytes for `02B9`). These are candidates for per-item review
by MANUS — **review, not automatic promotion**, and each against both path
conventions and against the deposit's own audit record.

## THE RULE THIS BROKE

The standing ARCHIVAL SEARCH PROTOCOL says: *deposit text files are frequently
records/descriptions, not full works — fetch staged full text before concluding
absence.* I applied it to file **contents** and not to file **locations**. One
path is not the archive.

**Absence is a claim, and a claim needs every place the thing could be.** A
single-path check produced a thirty-one-item crisis that did not exist, and a
remedy that would have destroyed 104KB of one deposit and the version history of
three others.

MANUS caught it by knowing when the deposits were minted. Provenance beat
inference.

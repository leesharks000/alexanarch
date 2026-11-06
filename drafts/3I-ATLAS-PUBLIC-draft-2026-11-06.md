# A Firm No: What the 3I/ATLAS Radio Searches Could See

Lee Sharks · Crimson Hexagonal Archive · draft of 6 November 2026 · not deposited

**A note on how this was done.** The searches described here were run on public telescope data between 2 and 6 November 2026 with two machine collaborators, Claude (Anthropic) and ChatGPT (OpenAI), working on the same files and checking each other. Every plan for a test was frozen and hashed before its data were read, except where a look is marked exploratory. The full working record, with the code, the results and every number below, is the companion notebook by Nobel Glas and Orin Trace, *What the Filters Kept*. What this essay claims is my decision.

---

## Start with one search

On 2 November 2026, signed out, in a private browser window, I typed **avi loeb 3i atlas** into Google.

The AI Overview gave Avi Loeb's early suggestion that the interstellar object 3I/ATLAS "could potentially be artificial or extraterrestrial technology", listed his anomalies, and then, under the heading **"Shift to Natural Consensus"**, closed the matter: "Following its closest approach to Earth in December 2025, Loeb acknowledged to NewsNation that 'given all the data that we have, I would agree that it's most likely natural.'"

That sentence is real. So is what came after it. On 23 April 2026 Loeb wrote that the object's fading light curve "does not show any evidence for artificial (self-produced) light", then set out the anomalies one by one, each with a probability ("aligned to within 5 degrees with the orbital plane of the planets around the Sun, with a probability of 0.2%"), and concluded: "Altogether, these anomalies led me to rank 3I/ATLAS as Level 4 on the Loeb Scale." A later essay of his sat among the Overview's own source cards. The answer carried the December sentence forward as his position and left the argument behind.

That is how a summary flattens a person: a dated, quotable line outranks a long argument with qualifications in it, and once it is composed it reads as the settled view. Nobody has to intend it. The short sentence is easier to carry, and it gets carried.

The same thing happened to the science.

---

## The firm no

Three teams published radio searches of 3I/ATLAS: the Allen Telescope Array in California (Sheikh et al., arXiv:2512.18142), the Green Bank Telescope in West Virginia (arXiv:2512.19763) and China's FAST. All three found nothing they judged worth following up. The Green Bank team reports "a nondetection of candidate signals down to the 100 mW level". The ATA team: "We did not find any signals worthy of additional follow-up."

The public account turned that into a verdict. One widely shared write-up: "The question everyone was waiting for has an answer, and it is a firm one."

A null result is a real result. But it is a result about an instrument. The archive has a name for this, from earlier work on how classifiers decide what physics experiments keep: **instrument-conditioned nullity**. Stated carefully: "A null result constrains only those hypotheses for which the end-to-end acceptance of the acquisition and analysis chain is sufficiently characterized." (*The Iceberg Document*, #1450.) Put plainly, a search that finds nothing has told you about everything it could have seen, and nothing about anything it couldn't.

So the honest question about 3I/ATLAS is what these searches could see, and what their own rules removed before anyone looked.

---

## What the ATA's filter kept

The Allen Telescope Array search started with nearly 74 million narrowband "hits" in 7.25 hours of data. A hit is any narrow spike of power the software flags. Almost all of them are our own interference: satellites, radar, phones, the electronics of the telescope itself. The team cut them down in stages: frequency blanking, a drift-rate window, a comparison between two beams, and finally inspection by eye. About 2 million survived the first cuts; 211 survived to be plotted. All 211 were human interference.

The drift-rate window is where it gets interesting.

A transmitter riding on a moving object doesn't hold still in frequency. As the distance between it and the telescope changes faster or slower (the Earth turning, the object moving), its frequency slides: the Doppler drift. Searches use this. A signal that drifts the way the object's motion predicts is interesting; one that doesn't is probably local. The ATA team computed the drift a transmitter on 3I/ATLAS would show and filtered for it. Their stated purpose: "To filter out signals that do not match the dynamics of 3I/ATLAS."

The paper takes the rate of change of the object's distance from JPL's Horizons ephemeris, finds it positive in all five sessions, converts it to a drift, and reports that drift as positive ("the minimum drift rate of 3I/ATLAS would be 0.15 Hz/s"). Then: "We filter our hits for drift rates between 0.05–1.5 Hz/s at all frequencies." Their Figure 4 shows the kept range on a signed axis, from 0 to +1.5 Hz/s.

The physics runs the other way. When an object's distance from you is growing faster, the frequency you receive from it falls. A rising recession rate gives a negative drift. I checked this at the ATA's own site on 3 July 2025 with the same ephemeris: the range-rate went from −51.440 km/s at 06:50 UTC to −51.377 at 07:20. A tone riding on the object drifts at about −0.125 Hz/s at 1075 MHz. Every public ATA session shows the same sign.

The paper got the size of the drift right and gave it the wrong sign. On its own figure, the drift it computed for a transmitter on 3I/ATLAS falls in the half its filter threw away.

What this shows, and what it doesn't. It shows that the documented method removed the class of signals it set out to keep. It does not show that a transmission was discarded. I haven't seen the executed filter code or the before-and-after hit lists, so the claim rests on the manuscript, the figure and the physics. And because the ATA's data are public, the removed class can be searched again. We did: along the object's true drift, at ten frequencies in the July 3 session and fourteen windows in the July 8 session, nothing stood out against the same path with its sign flipped, the reference beam or a fixed tone. The discrepancy hid nothing that this look could see. It is still a discrepancy in a published method, and the public verdict was built on it.

---

## Thirteen features under the floor

Then there is the Green Bank cadence of 18 December 2025.

The Green Bank search observed in a standard pattern: three looks at the object (ON) alternating with three looks at empty sky nearby (OFF). A signal from the object should appear in the ON looks and vanish in the OFF looks.

We took a narrow slice of that data, 2.93 MHz wide around 1667 MHz, near a frequency where comets naturally glow (the hydroxyl line). We followed the object's own drift through all three ON looks and counted places where weak power lined up in all three while the OFF looks stayed quiet. Then, as the control, we did the same count along forty deliberately wrong drifts. If nothing is there, the true drift should look like the wrong ones.

The wrong drifts gave an average of 3.75 such clusters, never more than 8. The object's true drift gave 13.

Here is what we did with those thirteen, in order.

- **Reproduced them.** An independent implementation gets exactly 13.
- **Tied them to the object.** They appear only with the object in the beam. Of the 20 ways to assign three of the six looks as "ON", only the real assignment gives 13; the others give 0 to 6.
- **Ruled out the usual suspects.** The comet's own hydroxyl emission would sit within about 11 kHz of known frequencies; the nearest of the thirteen is 54 kHz away. Interference fixed in the receiver, measured from the OFF looks and masked out, leaves 12 (one of the thirteen sits on a known interference line). No cluster is a single spike.
- **Built four different backgrounds**, each destroying one thing a real source would need: the order of the time samples, which looks were ON, the positions of features in frequency, the object's motion. In 139 tries none reached 13.
- **Looked everywhere else in the band.** Across 64 slices of the same Green Bank data, this one is the largest excess by a wide margin, and the only slice that beats every control.

And here is what they are not.

- **They don't replicate.** Not in fifteen other slices of the same band, not at 2.5 GHz, not at the Parkes telescope in July, not as a match between the July and December data, not in MeerKAT's lists.
- **They're fragile.** Normalize the data a different way and the 13 drop to 6, with 7 of 40 controls as high. Move the detection threshold a little either way and the excess disappears. All of it sits in a thin band just above the threshold, with nothing below.
- **They're faint.** In each look, each cluster stands about 2.5 to 3.3 standard deviations up, which is below where any detection threshold sits. Together they carry a few bits of information at most. There is nothing to read in them.
- **They don't look like what a weak steady transmitter would make.** If they were the visible tips of a population of faint steady tones, more of them would stand higher. They don't.

So: thirteen features, reproducible, tied to the object's position and motion, standing alone in their band, unreplicated and thin. They fall short of a detection, and they are the one result in the whole public record of 3I/ATLAS that nobody can settle.

Two more things make them worth stating in public.

First, they sit in exactly the drift class the ATA filter removed. On the night of the Green Bank observation, the object's range-rate was rising (from −1.917 to −1.827 km/s between 04:30 and 05:40 UTC), so a tone on it would drift negative, about −0.12 Hz/s at 1667 MHz. The Green Bank search itself didn't cut by sign. But anything of this kind is the kind a positive-only filter discards.

Second, they sit below the floor of every published search. None of those searches reported a firm no about features like these. Their pipelines aren't built to see them. "Nothing was found" is true of what was looked for, at the strength it was looked for.

---

## What would settle it

One document. In the third ON look the telescope's position record, read at the moment it was written, shows the dish 16 arcminutes off the object. If the dish was really there, nothing from the object reached that look and the thirteen can't be emission from it. We tested this as far as public data allow. The header was written partway through a slew, as 20 of the night's 24 headers were. And the hydrogen the dish recorded in that look matches the object's patch of sky and not the empty sky beside it. The public data say the dish was on the object. The antenna's own pointing record for 05:08:17–05:13:15 UTC on 18 December 2025 would say it directly. Green Bank and Breakthrough Listen hold it. It isn't public.

Failing that, a new observation at 1667 MHz with sensitivity near Green Bank's, with the thirteen frequencies and the counting rule fixed in advance, would test whether they come back.

There is a precedent for this kind of patience. When the ozone hole first appeared in satellite data, the software's quality threshold flagged the low readings as probable instrument faults. The comparison data shared the same wrong assumption and agreed. What broke it was an independent ground station with different blind spots, and the raw satellite data, which had been kept and could be reprocessed. (The popular story that "NASA's software deleted the ozone hole" is wrong; the true story, told in *The Iceberg Document*, is better.) What saves an anomaly is preservation and independence. Breakthrough Listen's public data are that kind of preservation. That's the only reason any of this could be checked.

---

## What the public was told, and what it could have been told

The searches were careful. The teams published their data, which is more than most science does, and it's what made this work possible. My argument is with what happens to a bounded result on its way to the public.

"No signal" travelled as "a firm one". Loeb's long argument travelled as one sentence from December. A sign error in a drift filter travelled nowhere at all. And the one unexplained excess in the public data sits where no published search was built to look.

A scope-bearing sentence would have cost almost nothing: *no narrowband signal above these strengths, within these drift rates, in these bands, on these dates.* That sentence is true, and it leaves room for what it doesn't cover. The firm no doesn't.

I don't know what the thirteen are. Nobody does. That is the finding, and it is more than the public account allows.

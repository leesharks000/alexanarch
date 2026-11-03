# Completed numerical-anchor pass — 3 November 2026

All six paired ATA July3 native extracts saved; all three discovery and all three reserved continuation observations scored. No discovery or continuation screening flags. No work remains pending in this bounded pass.

Discovery strict ±5Hz best joint scores and matched-comparison counts equal/higher: OH1667-rest 2.150674,90/100;1667MHz-rest 2.604677,64/100;1667MHz-receiver 2.998742,18/100. All three broad maxima were frozen before reserved powers. Continuation ±5Hz at frozen centers with fixed duration/template: OH nominee2.311207,67/100; emitter1667 nominee2.745526,12/100; receiver1667 nominee2.632525,32/100. No all-three-scan persistence requirement. All nominees were carriers; three-tone10/100/1000Hz patterns were also searched in discovery.

16 ordinary-HDF5 source slices bitwise equal; all6nativefiles CRC/SHA pass with zero masks;12selected-max scalar checks reproduce scores within8.9e-16. All18fixed-cell injection diagnostics complete. Injections show monotonic component response but mostly remain below screen at4raw-MAD, so no broad faint-signal exclusion. The detector requires target/reference excess and does not test equally shared all-beam messages, arbitrary modulation, phase, polarization, subintegration timing or general OH profiles. Rest-frequency tests use a first-order model, not a full Doppler/clock uncertainty budget. A failed screen does not identify a human source or settle artificiality.

Report: https://chatgpt.com/library?file_id=libfile_7e1a6b1f31348191b2aba036b407ff31&account_id=personal
Evidence: https://chatgpt.com/library?file_id=libfile_9ce39f0cc9c48191ac2ca1cf7248237e&account_id=personal
Plan: https://chatgpt.com/library?file_id=libfile_e46429c156088191bce3cfc6183b1aa8&account_id=personal
Exact native IDs, filenames and source hashes are in saved-ids.json and the report. Core scripts: search.py, injections.py, check_math.py, discovery/acquire_ata.py, holdout/acquire_ata.py. Full primary surfaces and complete comparison/segment-max ledgers in each directory's all-search-arrays.npz.

This section supersedes the earlier numerical-search progress notes below. Earlier work is preserved as historical context. Prior original13GBT reconstruction, earlierC03/new-bandATA tests and pointing uncertainties remain distinct, not overwritten by this numerical test. No semantic content or inference specifically about AI operators was established.


---

# Numerical discovery complete; continuation frozen

All three new paired focal extracts saved, all18fixed injections and8source checks complete. No discovery screening flags. frozen-nominees.json and Frozen-1667-continuation-2026-11-03.md specify three prospective continuation tests. No continuation focal powers inspected yet. Evidence contains all primary surfaces and matched comparison/segment maxima.

# Numerical-anchor search progress — 3 November 2026

First new discovery paired native extract completed, CRC/SHA verified and saved as libfile_20a39cefdec881919b7b1b9e1d2a729a. All masks zero. First-scan full search scored and partial ledger saved; these are incomplete exploratory results, not detections. Remaining two discovery pairs are acquiring. Source decoding spot-check and 18 fixed-cell injection diagnostics are running. No heldout focal powers acquired yet. Active numerical plan is libfile_e46429c156088191bce3cfc6183b1aa8; executable evidence libfile_9ce39f0cc9c48191ac2ca1cf7248237e.

One transfer interruption resumed from SHA-checked compressed chunks; the ordinary public Range probe succeeded. No authenticated access, contact or policy escalation.

## Active newsearch — numerical1667anchors and intermittent patterns

User changesprior: assume numericalsignificance; examine1667closely. Frozen plan Numerical-1667-search-plan-2026-11-03.md and numeric-search-config.json before new selected powers. Threeanchors: physicalOH1667.35903MHzcometrest; literal1667MHzcometrest; literal1667MHzfixedreceiverframe. Waveforms carrier and3toothlocalpeakpatterns spacing10/100/1000Hz. Allwithin-scansegments1/2/4/8/16/19samples, no all3scanoccupancyrequirement andnogapconcatenation. Matched100frequencycenters+/-200Hz*k eachmaximizeoveridenticalfullfamily/time/frequencytrials. Jointtargetlocalpeak andtarget-minusreference score; rawpositivegates. Screens>=3empiricalMAD andaboveallcomparisons; descriptiveconditionalranks, notglobalpvalues.

Newfocalpowers: first3July3LoA.C1504pairs chunks182/183bothbeams/masks. Holdoutnext3pairsindices3–5reserved; oldinstrumentedtestsusedotherfrequencychunksinthosepairs. Beforeholdoutpowersfreezeonebest+/-100Hznomineeperanchor'sfrequency/frame/template/duration; followat+/-5Hzanywithin-scanstartofsameL innew3pairs. Sourceandmeaningremainunknownunlessfurtherindependentevidence. Initialexactplan/config savedwiththischeckpoint. Priorcompletedpersistent-tonebatchnotchanged.

Next: acquire/savenativepairs; sourcebitwisechecks; execute fixedfamily completecontrols anddiagnosticcomponentinjections; freezeall3nomineesandtestheldoutpowers; saveallpartialresultsatboundedbatches.

## LATEST COMPLETED BATCH — new-band search and allfourheldouttests complete

All acquisition and analysis jobs in thisbatch ended. No backgroundsearch isrunning. Main newreport:3I-ATLAS-new-band-search-2026-11-03.md. Completeevidence libfile_61cc8ebb901c81918cc2de8efa867237 (latestfinalversion). PriorC03report libfile_44f436fca71481918d3de5e73564797b and original13directreport remainpreserved. Currentnewworkdirectory signal-continuation-20261103; restorefromsavedfiles iftemporaryworkspaceexpires.

MEASUREDRESULTS:
1. SixGBTfrequency-baseline trueframeclusterlocations tested innewATAJuly3scans07:50:48,07:57:32,08:04:16UTC. All6x2windows(+/-5/100Hz)x2normalizations=24combinations give0flags. Notatestofall13originalGBTlocations. LowerATA sensitivity/differentepoch meansnofaintDecember/intermittentexclusion. Sourceunknown.
2. Supplementalnewfullbandsearch:781966commonfrequencygridpoints across3sourcechunks, physicalframe4clusters vs40comparisonframesmean4.475,SD3.07398,max13,22/40>=4. Conditionalrank23/41=.56098;notglobalpvalue. Noaggregateexcess. Allfournewmaxima selectedunderpredeclaredtop5cap, frequenciesfrozenbeforeheldoutpowers.
3. Heldoutsame-night3newpairs08:11:01,08:17:46,08:24:30UTC. All4failfixed+/-5Hzconstantrest test. Bestminimumacross3targets, byfullID:ATA-BAND-F00-0001=-.322679,F00-0002=-.060686,F00-0003=-.098724,F00-0004=.800147. Allbelow2.5required;targetstrengthfailsirrespectiveofreferenceveto. Eligiblecomparisoncounts100,100,100,69;geactual65,51,66,7respectively. All369eligiblecomparisons0flags. Lastfeature's31excludedcomparisonsaremetadataedgeexclusions,notRFIcuts. Noemitteridentified;intermittency/othermodulationunexcluded.
4. 24ordinaryHDFsource-slicechecks(12discoveryfirstpair,12holdoutfirstpair)bitwiseequal over3chunks,bothbeams,powers/masks. All6newpairednativearchiveshashverifiedandmaskszero. 24discoverymaxima-scorecalculationsmatchseparatefixedfrequencycodewithzeroerror. Allscorecubes,controls,perintegrationtables,41frameclusters,sourcehashes,plansandcodearepreserved.
5. Publicsourceclarifiesheaderchain:currentGBTj2000_major/minor ->RA_STR/DEC_STR ->firstinputrawspecheadercopiedtoallproducts. Exactdeployedbuild/configurationandactualantenna historynotobtained. GBTscan17stillunresolved;doNOTclaimprovedmispointing. PublicscheduleprogrammeGBT25B-999. PublicNRAOquotedGBTfiltervalidatedwith8797unfilteredrecords;dateintervalquery0GBTrecords. BLindex1296HDFlinks/norawheaderFITSloglinks;operatorlogsrouteauthwall. GBT-pointing-evidence-needed.mdspecifiesminimalpacket;notmessagedtoanyone.

Durable newnativearchives (eachpairedpowers+masks,three0.5MHzchunks):
Discovery0 libfile_319b7ede4dac8191acbfe60758e0bc03
Discovery1 libfile_c24907423ce48191b221c51b27bade31
Discovery2 libfile_950e3d84e5d081918ab3f5ea722555b4
Heldout0 libfile_178d43182ad0819188c521f2a190d0e9
Heldout1 libfile_4c2a7b38abec8191b42c0372ca6370cd
Heldout2 libfile_005238e5d5b88191b05690e8766249ce
Exacthashes/sourceURLs in native-input-ledger.json andindividualmanifests. Onecancellednetworkapprovalcallbackinterruptedfirstheldoutdownload;regular80bytepublicRangeprobe succeeded, then acquisitionresumedwithSHAverifiedchunkcache. Noauth/escalationused. Completedpowers/results survivedallpartialcheckpoints. Cachedcompressedsourcechunks aretransientandredundant,excludedfromevidence.

NEXTSUBSTANTIVEWORK: thisboundedpersistentconstant-tonebatch iscomplete. Do notrecastit asnoallpossiblesignal or ashumanidentification. A differentintermittent/relationalhypothesisneeds a declared observable,correct handlingofrealscangaps, trialinventory/injections andunused-observationprediction. Originalauthors'human-source-rejectionauditstillneedsactualoriginalexamplepowers/fullrejectionledger; keepourmaximaIDs distinctfromtheir211cases. ActualGBTantenna/GO/rawheadertime series stillneededforpointing. User'sfiveconditionsremainhypotheticalandnotamplitude-only. Noartificialoriginorsemanticmessageidentified.

## Four-candidate continuation: two heldoutnativepairs complete

Heldoutscan0 savedlibfile_178d43182ad0819188c521f2a190d0e9. Heldoutscan1nowcomplete withzero masks, CRC/hashpass:ATA-band-holdout-powers-scan1-2026-11-03.npz,102616588bytes,SHA25605d618381b966bb86f3d494e26aae3e766bc9cf3283a30cede6fbbaa8007d23a; being savedwiththischeckpoint. Thirdpairacquiring withchecksumverifiedper-chunkcache. Noheldoutscorecomputeduntilall3inputscomplete. Lastconfirmedfullevidenceversion4containsallcompleteddiscovery/sixlocation/broadframe/morphology/mathematicalvalidationandfirstholdoutmetadata; nextfinalpackagewilladdcompletedholdouttables. No newsourceclassification.

## Four-candidate continuation: first nativepair complete after transfer restart

Firstheldoutpaired1.5MHzcutout completed withzero nonzero masks andCRC/SHA256pass:ATA-band-holdout-powers-scan0-2026-11-03.npz,102616291bytes,SHA256c2b3bf4216c5ce7c3bb4621cd2b07936f6c0e9954491babfdc7d70a536825f0f. Being savedwiththischeckpoint; remaining2pairsacquiring. Earlieracquisitionprocessendedwhenanetworkapprovalcallbackwascancelled;80bytepublic-rangeprobe succeeded, so resumedregularpublicreadwithper-chunkSHA256cache. Noescalation/authenticationorcredentialsused. Cacheisaconnectionrestartoptimizationonly, numericalmethodunchanged. analyze_holdout.pywaitsforcompleted3inputs; noholdoutscoresyet. Frozenplanlibfile_7f0c737914948191919fadeea98fc664.

Directfixed-frequencymathcrosscheckofall4newmaximax6beams=24scores nowdone: allmatchbroadsearchscores withexactzeroerror. Sourceplotsandperintegrationcontributionssaved; top2positivecontributions span24–41%ineachtarget. Noemitteridentified. GBT-pointing-evidence-needed.md specifiesprecisetimewindowandcolumns; notsenttoanyone. Neitherrepeatedscalarheadersnorpublicsourcecode substitute for actualantenna history.

## Bounded full-band search completed; four new maxima frozen for continuation

All41framescomplete. Physicalframe4clusters vsfalsemean4.475,SD3.07398,max13,22/40>=4,conditionalplusonerank23/41=.56098. Noaggregateexcess. Commonmetadatafrequencygrid781966points across180–182storagechunks, identicalcountedcoverage forall41frames. Fourtrueclusters IDsATA-BAND-F00-0001..0004, rankedbymin-targetscore; allfourfrozenin band-holdout/targets.json. BestrestHz inrankingorder:1665737025.9742508,1666484637.8055997,1665766813.6614635,1665646564.467809. Discoverymin-targetscores2.8971,2.6806,2.6268,2.5286. Sourcesunknown, notcandidateconfirmed orhumanidentified.

Nextfixed3July3scanpairs indices9–11:29461_38726318,29866_38751037,30270_38775695. PlanATA-band-candidates-holdout-plan-2026-11-03.mdsavedbeforethosepowersread. Fixedbestfrequencies +/-5Hz, frequencybaseline1024,per0.5MHzcalibration, same3target>=2.5/ref<2, matched100frequencycomparisoncenters subjecttomodel/metadata-onlycoverageeligibility. Allfourreportedwithoutfrequency/driftrescue. Acquirefull3chunksforbothbeamseachpair, masksretained. Candidate nearstorageedge meanssomecomparisonsineligible; do notreport100aseligibleblindly. Actualscientificstatusawaitsnewdata.

AllsixfixedGBTfrequencyfollowupresultsandfirst3newnativepairs saved: scan0libfile_319b7ede4dac8191acbfe60758e0bc03,scan1libfile_c24907423ce48191b221c51b27bade31,scan2libfile_950e3d84e5d081918ab3f5ea722555b4. Evidencecurrent libfile_61cc8ebb901c81918cc2de8efa867237 version2beforethissave; allfull-bandresults/code andtrueframefrequency-scorecubes now included in nextversion. Nativefilehashes remain in eachsource manifest.

## Six-location batch complete; bounded new-band search running

All3newpaired1.5MHzcutouts acquired, CRC/SHA256verified, masksallzero. Firstnativepair savedlibfile_319b7ede4dac8191acbfe60758e0bc03; nexttwo being saved withthischeckpoint. TwelveordinaryHDFslices across3chunks/powers/masks/bothbeams matchbitwise. Fixedall6targets x2normalizations x2windows complete: noflags in anytargetwindow. Scores, matchedcomparisoncubes, calibration andpaths in six-followup/analysis. No new human-source classifications follow from thesenulls. LowerATA sensitivity/differentepoch limitinference.

Frozenfull-band newcandidate search running as six-followup/search_band.py; all41framecounts andclusterledgers persist aftereachcompletedframe in six-followup/broad-search/. Same full-band frequencycoverage acrossallframes determined bymetadata. User's latest 'Continue thischat' continues thisauthorizedtask. Iftrueframe clusters exist, freeze top5bestfrequencies and acquirepredeclarednext3scansbeforelooking;otherwiseboundednullcomplete. Do notassume processes survive a timeout; checkcompletedjsonoutputs andrerununfinishedbatchesifneeded.

Tracking investigation: publicNRAOAPI correctGBTqueryroutevalidated against8797unfilteredGBTrecords; requested2025-12-18/19intervalreturns0GBTrecords. Thisis a testedquery result, notabsenceofobservations or recordsatGBO. SchedulematchesGBT25B-999. BLrootcontains1296HDFproductsandnoraw/header/FITS/loglinks. Noactualtracking obtained. Publiccode shows j2000_major/minor ->RA_STR/DEC_STR ->firstinputheadercopiedtoallrawspecproducts; exactdeployedbuildunverified. Source provenance/redacted snapshotretained.

## Additional frozen search — new candidates in the same new band

Before inspecting new six-location scores or newband patterns, specified Broad-ATA-search-plan-2026-11-03.md: full retained threechunk commonmetadata coverage, one-nativerestgrid, frequencybaselineonly, same all3target2.5/ref2gate,10Hzclusters, top5byminimumtargetscore, matching40falseaccelerations seed11. Commoncoverageintersection computed fromephemeris/metadataover41frames. Conditionalranknotglobalpvalue. Anytruecluster gets frozenbestfrequency +/-5Hz and next3July3pairs indices9–11 beforepowers. This supplements ratherthanalters six-locationfollowup and adds disclosedselectiontrials. Newpowers alreadyacquiring but no spectralpatterns/scores examined at thissupplement's specification.

## Six-candidate continuation partial checkpoint — first new nativepair complete

Firstpaired1.5MHzATAcutout (nextscanafterprevioussix) acquired,19integrations/beam, zero nonzero masks, CRC/hashverified:GBT-FB-six-ATA-powers-scan0-2026-11-03.npz,102590346bytes,SHA256c33e0cb8abb899b501bd4ac8b28713095e06771682b0b9627bed5a37104caf9f. IndependentordinaryHDFsourcechecks12slices across3chunks,powers/masks,bothbeams, firsttarget/lastreference integration allbitwiseequal. Remainingtwo pairs acquiring; fixedallsixscoringawaitscompleteinputs. Planlibfile_b9fd807273e48191b47e0e89fb580790; newevidence libfile_61cc8ebb901c81918cc2de8efa867237.

PublicGBTindex1296HDFproducts,no raw/header/FITS/log links. Publicoperatorlogsroute sign-inwall. NRAOmetadataqueryrouteworking; date-onlyreturnsrecordsbutquotedGBTdatefilterreturnszero, unfilteredGBTcontrolpending; do notconflatewithnoobservationsorGBOholdingnodata. Rawsourcecodechain clarifies scalarheaders: hpguppi statusloop reads j2000_major/minor thenRA_STR/DEC_STR;rawspec copies firstinputheader intoallproducts. Exactexecutedbuild andactualantenna history unverified. Do notclaim observedtelescopeofftarget. Sourceprovenancepin/hashes saved; connectionparameters inpublicsource snapshotredactedandnotused.

## Active continuation — six GBT alternate-detector locations,3November2026

Current authorized task: continue searching. Prior completed evidence restored from libfile_30a7cba244288191b5634a465f7e5a4f version3; native files are saved separately, not assumed to remain local. Prior checkpoint version20 read in full. New frozen plan: Six-candidate-ATA-plan-2026-11-03.md and targets.json, allsix alternate GBT clusters, nextthree previouslyunexaminedJuly3LoA.C1504pairs, three sourcechunks180–182, bothbeams/masks. Fixed +/-5/100Hz windows, selectingfrequencybaseline and secondarytimemedian, per0.5MHzcalibration and100matchedcomparisonsperlocation. No new powers examined at this checkpoint. Source unknown unless evidence identifies it. PreservepriorC03null and normalization-sensitive13vs6results.

GBTtrackingbranch: publicsupportlink to operatorlogs redirects to a sign-inwall; actualtrackingdata notobtained. Publicschedule andNRAOportalHTML accessible; furthermetadata/codeprovenancecheck inprogress. No person-directedcontact or credentials used. Neverreplace actualtracking with repeatedscalarheaders.

Next: acquire nativepairs with bounded verifiedHTTP ranges; run fixedall6scores/comparisons; savepartialpowers/results aftereachbatch. Anyflag requires a separatelyfrozen continuation on next3scans.

## LATEST COMPLETED BATCH — 3 November 2026 — supersedes running-status notes below

Completed C03 independent-epoch ATA follow-up, a distinct ATA-OFFSET-01 heldout same-night continuation, and the missing GBT alternate-normalization40falseframe comparison. All jobs ended; no need to assume a still-running process.

Main report: 3I-ATLAS-C03-followup-2026-11-03.md. Evidence: current version of libfile_30a7cba244288191b5634a465f7e5a4f, C03-followup-evidence-2026-11-03.zip. Raw sixpairednativecutouts are independently saved; exactids/hashes in native-cutout-records.json and report. Previous direct original13report remains libfile_ec087222fc5c8191a477c4289e631591; original13nativeGBTinputs remain saved separately.

MEASURED RESULTS:
1. C03 rest1665633776.617Hz:3newJuly3pairedscans, noflags +/-5 or100Hz under either detector. Primary best targetminimum -0.29696 strict,1.07009 wide. LowerATA sensitivity and different epoch prevent exclusion of a faint/intermittentDecember source.
2. ATA-OFFSET-01 was selected in alternate comparison-window powers at rest1665614737.5230594Hz, targets2.8044,2.9953,3.0396. It is NOT C03 and NOT establishedRFI. Its exactfrequency and +/-5Hz continuation plan were frozen before reading next3scans. Those scans have noflag in either normalization; selecting-detector exactscores -0.65729,-1.72716,-0.46406. Bestminimum overwindow -0.89643,96/100matchedcomparisons atleasthigh. Persistenttone case weakened; source remainsunknown.
3. GBT alternatefrequencybaseline:6clusters, falseframesmean3.425,SD2.119994,max9,7/40>=6, conditionalplusonerank8/41. Nativehashes verified, normalizationcachebitwisematches, all78selectedbin alternatescores matchwithzeroerror. Sixtrueclusters reproduceoldcount. These are alternate detector's own6clusters, NOT6survivors oforiginal13. At originalselectedbins onlyC03passesalternateON/OFF. Originaltime-median13vsmean3.75,max8,0/40>=13 remains unchanged. Overallaggregateexcessnormalization-sensitive; no transmitter identified by thiscomparison. Perframeclusters/counts and updatedoriginal13ledger saved.
4. GBTscan17header discrepancy16.108arcminICRF/9.827apparent repeatedacross3products. Actual settledpointing notobtained; doNOTclaimprovenmispointing. Parkesrootaccessible; testedblc00/blc07children403. NoParkespowersread. MeerKATthresholdedlists notsubstitutedforpowers.
5. ATAall12inputbeams maskszero;6pairednativefilesCRC/hashpass;8normalHDFslices offirstpairpowers/masksbitwiseequal. Injectionfinalrecoveriespersistent0/3,2/3,3/3 at0.3/0.6/1MAD;middleonly0/9. Fixes tonumericalrecoverybookkeeping didnotchangeastronomicalscores.

NEXT SUBSTANTIVE WORK: resolve actual GBTscan17tracking versusheadersemantics; obtain source-evidence ledger for surveyrejectedrealfeatures, preserving ours versus authors' IDs. For originalcandidate pool, specify an independent empiricalbackground/sensitivitycheck before further reinterpretation. For intermittent/modulated hypothesis, freeze observable relation and heldoutprediction instead of expanding passed/failedwindows after inspection. Keep user's fiveconditionshypothetical, not amplitude-only; no artificialorigin/message established.

Reproduce current ATA results with acquire_ata.py/analyze_ata.py and offset-holdout counterparts. gbt_robust_controls.py reads prior original13nativefiles/ephemeris; itslarge deterministic scorecaches are omittedfromevidence but checksums retained. Allmethodplans, code, metadata, scores, controls, perintegrationtables andfigures are included.

## Current bounded continuation — new powers acquired

ATA-OFFSET-01 all three new same-night paired cutouts acquired with zero nonzero masks; CRC/hash checks pass. Holdout scoring running (offset-holdout/analyze_holdout.py). These three native pairs are being saved in this batch. Do not infer results before reading actual summary.

Also completing a previously missing direct GBT check: matching40false-frame counts under the fixed alternate frequency-baseline normalization. Frozen parameters in GBT-robustness-control-plan.md. Code gbt_robust_controls.py computes all41frames on six already-persistent fullcoarse inputs, bitwise checks normalized caches and matches all78prior selected-bin scores. Large deterministic score caches are transient; persist final frame/cluster tables, math validation and code. Keep this same-data robustness result separate from original13excess and independent ATAepoch. Process may need rerunning on interruption; completed original work remains saved.

Injection bookkeeping adds a numerical boundary guard under1microHz so a one-native-channel equality is not rejected through subtraction at1.66GHz. Final persistent injected recoveries0/3,2/3,3/3 at amplitude0.3,0.6,1.0; middle-only0/9. Astronomical scoring unchanged. Source spotvalidation8slices allbitwiseequal saved in independent-ata-hdf5-validation.json.

## 3 November — C03 July follow-up completed; ATA-OFFSET-01 continuation queued

All three paired native0.5MHz chunks acquired, SHA256 and CRC verified, masks allzero. C03 has no flags in either frozen +/-5Hz or +/-100Hz window under either normalization. Time-median best minimum across3targets: -0.29696 strict,1.07009 wider. Offset controls give0/100 flags in either primary window. These are conditional, lower-sensitivity July results; they do not refute the original December13cluster excess or identify its sources.

Alternate frequency-baseline normalization flags one comparison-window coordinate, designated ATA-OFFSET-01, rest1665614737.5230594Hz. Target scores2.8044,2.9953,3.0396; reference0.8212,-0.3162,-1.4341; primary time-median targets1.6400,1.7226,1.6032. No clear visible track. Source unknown. Do not label a false positive merely because selected from a comparison window. Frozen next-three-scan plan in offset-holdout/ATA-OFFSET-01-holdout-plan-2026-11-03.md; new powers not yet read at this checkpoint.

Injection recovery bookkeeping now tests any acceptable gridpoint within one native channel of the injected location, instead of only the highest target-minimum coordinate. Astronomical scores unchanged. In18idealized cases, persistent amplitudes0.3,0.6,1.0 recover0/3,2/3,3/3 respectively; middle-only0/9 by the required3scan persistence rule. Not a physical sensitivity curve.

Coordinate branch: ON17 header discrepancy16.108arcmin relative to ICRF,9.827arcmin relative to apparent. Same header appears in3frequency/resolution products, so not a single-export transcription; no actual encoder/GO tracking logs found. Do not claim proven mispointing. Parkes Oct5root opens; tested published child blc00/blc07 return403. MeerKATlists exist but are thresholded hit lists; no new powers there.

New native pairs1/2 saved successfully as libfile_d97acc5464f88191b65fe1970f0160e6 and libfile_0c4b2b1b57a08191ae11616aba261326. Current evidence version1 confirmed. Pair0 already libfile_1e5ab075742c8191b90a791dc82f029c. Next: finish source spotvalidation, execute frozen heldout plan, then write bounded report and persist batch.

# C03new-power batch1: first ATApair complete

New LoA.C1504chunk180 for firstJuly3scan is acquired,19samples perbeam,0nonzero masks, native1665.75–1666.25MHz region. C03first-orderprediction~1665.9195MHz, constantrest1665633776.617Hz, strict±5Hz/secondary±100Hz windows remain frozen. Firstpair file C03-ATA-new-powers-scan0-2026-11-03.npz,34216817bytes,SHA256c6c2efcb705156c804a697fee2cc34c50a6a2cb8bc8b35f46a063933829a1f90. It is being saved with this checkpoint. Two morepairs acquiring; no new score result yet. Metadataprefetch was expanded to bothcomplete data/mask indexes because HDF5chunk-info lookup walks them; all finalchunk offsets remain determined by HDF5.

ParkesOctober5rootindexopens but its published blc07 andblc00childdirectories return403from thisenvironment; do not generalize to allfiles. NoPKSpowersread. GBTframe check now compares bothJPLICRFandapparentcoordinates: nominalON17header differs16.108arcmin fromICRF and9.827arcmin fromapparent; simplyswitching to apparent does not reconcileit. Actualtracking/frame/epoch metadata remain unverified, so no off-target conclusion.

Next: finishpairedpowers, validate source-read spotcheck, score frozenC03and matchedcontrols, run declaredpower-domain injections, persistcompletedoutputs. Original13excess remains aseparatepreserved result.

# Active continuation — C03 independent observations, 3 November2026

Authorized: continue the search. We are testing fixed C03 in previously unexamined ATAJuly3 spectral powers and examining a ParkesOctober5 follow-up route. Also audit GBT0017headerframe/pointing semantics. No new-power result exists yet. The earlier original-thirteen result remains13vs3.75mean/max8controls, not refuted by a narrow-window null.

# C03 independent-observation follow-up plan

3 November 2026. Written before reading the new ATA or Parkes spectral powers.
This is an internal dated plan, not a public preregistration.

## Fixed target and scope
Primary target: C03, nominal first-order rest frequency F0=1665633776.617 Hz from the supplied GBT export. This is a coordinate on a2.79Hz grid, not a physical sub-hertz measurement. Model: emitted first-order rest frequency constant across epochs, received f(t)=F*(1-v_radial(t)/c), with JPL Horizons observer-site radial velocity at integration centers. This is a finite baseline hypothesis; intrinsic chirps, intermittency and arbitrary semantic organization are not excluded by its failure.

Primary new power batch: first three chronological July3ATA scan directories in the already saved published-session index:
fil_60859_24992_38453552_JPLH_ATLAS_0001
fil_60859_25484_38483581_JPLH_ATLAS_0001
fil_60859_25888_38508239_JPLH_ATLAS_0001
Use both simultaneous beams of LoA.C1504, targetbeam0/referencebeam1, and original19integrations at16.777216s and1.9073486Hz resolution. Those observation times were used at other frequencies in earlier work, but the C03-frequency powers have not been inspected.

## Frozen target windows and controls
- Strict coordinate test: rest F0±5Hz, half-native-channel grid.
- Secondary model-tolerance window: rest F0±100Hz on the same grid. This permits a finite additional offset; it is not a quantified complete relativistic/ephemeris uncertainty budget and cannot cover arbitrary transmitter modulation.
- Retain the entire0.5MHzcompressed source chunk containing the predicted frequency, all times and beams. If an edge prevents coverage, acquire adjacent chunk(s) based on metadata/ephemeris alone before viewing powers.
- One hundred matched control centers: F0±k*1000Hz, k=1..50, using the same window widths, grid, time coverage, detector and beam requirements. Discard an uncovered control only by metadata before powers.
- First-order absolute model is explicit; higher-order Doppler/clock effects can shift apparent rest frequency across months. Record both strict and100Hz-window results without enlarging either after inspection.
- Preserve raw powers and masks. A shared feature remains in the ledger as unlocalized; it does not become an identified human emitter without evidence.

## Detector and interpretation
Primary detector matches the original C03 family: per-channel time-median division minus1,3native-bin boxcar, physical-track power sum, per-scan median/MAD calibration over the full extracted slab. Use exact rest-frequency coordinates for candidate paths, no circular-wrap valid-power assumptions. Derive calibration with fixed-band shifts, and record approximation/edge treatment.
Frequency-baseline normalization with1024channel median blocks is a planned sensitivity check; it does not replace the primary result.

A candidate flag requires a single consistent frequency with score>=2.5in all3target scans and<2in all3reference scans. This is a follow-up flag, not a globally calibrated discovery threshold. Record the strongest target-minimum score and off-beam scores even if no flag survives. Apply the identical procedure to the matched frequency controls. Retain both primary and secondary frequency-window results.
An alternate-normalization pass at the same coordinate is a robustness check, not independent confirmation. The new observing epoch/instrument is independent of the GBT selection; the statistical methods are still exploratory.

Power-domain injections: amplitudes0.3,0.6,1.0in local per-sample MAD units, placements F0-3,F0,F0+3Hz, both all3targetscans and middle-target-scan-only occupancy. Add before normalization, no addition to reference beam. These are idealized native-bin powers, not a voltage/channel-response simulation or physical flux calibration. Do not extrapolate18placements/occupancies into a complete sensitivity bound.

## Other branches
Inspect Parkes October5public metadata to locate the C03 band and its6scan cadence; if accessible, freeze a second instrument-specific plan before powers. Its lower published sensitivity must remain explicit.
Inspect actual public metadata for GBTscan0017. Check JPL astrometric versus apparent coordinates, GBTheader provenance, coordinateframe/epoch and catalog-versus-encoder semantics. A numericalheader discrepancy is not proof of telescope mispointing. No person-directed contact is authorized here.
MeerKAThit-list availability can be mapped, but do not silently substitute thresholded hit tables for a subthreshold power search.

## Durable work batches
Save plan/checkpoint before acquisition. After acquisition save raw cutouts, source metadata/range hashes and ephemeris. After scoring save every candidate/control result and update checkpoint. All conclusions remain separate from the exact13clusterreproduction (which remains13vscontrolmean3.75,max8under its original rules).


--- Historical checkpoint ---

# Latest completed state — original13directaudit,3November2026

The original13coincidenceclusters and all78roundedscanvalues reproduce on public full-coarse7powers. All6optimizedtrue-framevectors match the unchanged supplied function bitwise. The packet's40seed11falseaccelerationcontrols reproduce mean3.75,SD2.046338,max8,none>=13. The finite plus-one rank1/41is not a global p-value. Keep this as a reproducible exploratorycount excess, not an identified transmission or a demonstrated fluctuation.

Important scope correction: all13span2.93MHz, none in our prior±5kHzOHwindow. That narrow-window result cannot reject them. The earlier report libfile_d1b9045bdfe48191b47dbafa2c5130a2 now has a scope addendum (version1). New report: GBT-OH13-direct-audit-2026-11-03.md. New evidence: libfile_6b47f6362dcc8191b56b0921522df356. All6complete full-channel native archives are separately saved; IDs and hashes in native-input-ledger.json.

Matched-control sensitivities: corrected reference rest-gridspacing gives12vsmean3.625,max9; carrier±10Hztrajectoryveto12vsmean3.725,max8; broader±60Hzveto11vsmean3.725,max8. No control reachestruecount in each construction. Actual nominalONroletriple has13; other19triples0–6, descriptive only because roles/time/sky/noise are not exchangeable.

C02directly crosses common fixed line complex near1665.61512MHz, visibleallON/OFF. About91%of its positive0013contribution is near measured localpeaks; it is the only strictON>=3survivor. C01does not cross centralcitedcarrier (nearestselectedpath27.5Hz), but occupies nearbylinecomb;52%ofpositive0015contribution near measuredpeaks. Do not conflate incorrectliteralcarrier-crossingwording with no contamination: localcomplex evidence is real. Four prominentpeaksshow~60.35Hzspacing, descriptive, emitterunidentified. C03–C13remainunclassified; no demonstratedhumanoriginforeach.

C03priority: nominal first-order rest1665633776.617Hz (2.79Hzgrid; no sub-hertz physicalaccuracy claimed). Underalternatefrequencybaselinenormalization,ONscores2.546,2.820,2.966 andOFF1.623,1.069,0.168. Removinglargesttwo path samples leavesON2.990,2.780,2.524. These are same-data robustness, not independent confirmation. Wholetruepipeline aftertrimming1or2largest samples gives7clusters; alternatenormalization6. Theirmatchingfalsecontrolsnotrun; do not use thosecountsas calibratedrejection/validation.

Lower-cut bookkeeping discrepancy: statedON>=2/OFF<1.5 gives80vs83.575mean;ON>=2/OFF<2gives107vs108.15mean, not packet118vs120.9. Needoriginalconfiguration; qualitativeabsenceofloosecutexcess holds. Supplied FFTscript concatenatesgappedONscans; claimedshuffletestimplementationnotincluded. Preserveunknown vs notdone.

NominalON17header coordinates differ from suppliedcomet by16.108arcmin IF sameframe;ON13=.158,ON15=.711arcmin. Officialblimpycodeconfirmshours/deg units. Actualpointing,frame/epoch and catalogvsencodermetadata meaning unresolved. Do not callscan17offtarget withoutantenna/pointingtelemetry. All6headersreplicated, masksunchanged.

Data durability:294fullcoarsechunks match priorcompressedhashes;112871892overlappingnativevalues match bitwise;all6full outputCRCs/SHAchecked. Totalcompressedoutput1050141263bytes. restore_inputs.py has been executed successfully for all6archives and reproduces exactnativeNPYhashes. Standalonenormalizationmodule ASTmatchesexecutedfunction; codehardening prevents completedstatewithoutmissingrawdatafromsilentlycreatingzeroarrays. Scores,41candidate-sets,all13six-scanwaterfalls,paths/times anddiagnostics are in evidence; large regenerable numericalcaches excluded.

Next focusedwork: verifyheadersemantics/actualpointing and freeze an independent-data test forC03beforeexaminingnewpowers, with explicit frequency/modeltolerance,occupancy andstatistic. Resolveglobaltrialhistory andlower-cutconfiguration. The broader fiveconditions remainhypotheses; no semanticmessage identified. Keep ATApublishedFig7/8audit separate.

--- Historical checkpoints below ---

# Exact reproduction complete: original thirteen survive reproduction

All thirteen clusters reproduce, and every one of78reported rounded scan scores agrees to its0.01precision. Mean cluster frequencies agree within0.0005Hz (export rounding, not physical accuracy). For all6scans, optimized true-frame score vectors are bitwise identical to the original unmodified supplied function.40false-acceleration controls reproduce mean3.75,SD2.046338,max8;none reaches13. A plus-one rank is1/41under this finite control construction; it is not a globally calibrated p-value. The earlier pastedmax10is superseded by READMEand independently reproducedmax8for these40seed11controls.

This is a reproducible exploratory count excess under the supplied method, not an established transmission. The original selection spans2.93MHz and is separate from the previous±5kHzaggregateanalysis. Do not overwrite it with the earlier negative narrow-window result. All full-coarse inputs are acquired;scan18 is being saved with this checkpoint. Remaining work: direct13candidate diagnostics, source-line contamination check, coordinate-grid and spike-removal sensitivity, and careful treatment of the nominalON17header discrepancy. Do not automatically classify C01as crossing the fixed tone: its entire supplied path remains below it. Both possible human interference and intrinsic/transmitter interpretations must carry their actual evidence.

## Input batch complete through scan0017; exact reproduction running

Full coarse7 for scans13–17 has completed source-chunk SHA comparison against the previous acquisition, native overlap equality, output CRC and SHA checks; scan18 is finishing. All13 supplied frequencies span the coarse channel, none in the former±5kHz line window. The original supplied code is preserved unchanged. Exact original-parameter Horizons query has been saved, including response; header RA units confirmed as hours by official blimpy source. A source-header inconsistency exists for nominalONscan17: its coordinates differ from the supplied comet position by16.108arcmin (ON13=0.158arcmin; ON15=0.711arcmin). This is a nominal-header check, not proof of actual telescope pointing/tracking. Need actual pointing telemetry before using the discrepancy as a rejection.

reproduce.py is computing the legacy40-control procedure with float64 row caching, each true-frame output checked against unmodified supplied code. No reproduced candidate count exists yet. Candidate labels C01/C02 remain supplied classifications pending raw-spectrum audit; C01's listed monotone track is already below the cited fixed tone at its start, so a literal crossing must not be assumed merely from the proximity label.

# Active continuation: direct thirteen-candidate audit, 3 November2026

The original candidate CSV and code were supplied. They expose an important scope mismatch: the thirteen are drawn from an entire2.93MHz coarse channel, and none is in the previous±5kHz OH window. Previous results remain bounded to their narrower selection and must not be used as a rejection of these thirteen. The new audit plan follows. No full-channel reproduction result yet.

# Direct audit of Claude's thirteen candidates
Written3November2026 before acquiring full-channel powers for this audit.

## Inputs and scope correction
User supplied oh13.zip (SHA2562034f51db60240330fb35c618900be6ace1af5e49b3609a29abb0f1202dfdff5) and oh13_candidates.csv (SHA256d3d15492915a18b09787534bc2e8df70f54a4d9934658ad631e0a9a7fb7f42df). ZIP CSV and attached CSV are identical;78rows,13IDs,6scans. The13span rest1665.604557–1668.429424MHz, a full2.93MHz coarse-channel selection, NOT a±5kHz OH-line window. None lies in the previous central±5kHz1667window; seven lie in the earlier wider raw cutouts. Therefore the previous narrow-window result does not adjudicate these13. Keep it as a separate completed analysis and add explicit scope correction.

## Frozen reproduction
- Preserve attached sources unchanged under reference/. Never run their fetching scripts blindly.
- Acquire entire coarse channel7 for all6exact files from the already verified published index. Reuse known chunk locations/hashes, retain every49native integration and1048576channels. Check equality to existing saved overlapping windows and per-chunk hashes.
- Save native full-channel arrays, output CRC/hashes and source manifests per completed scan.
- Fetch and save the EXACT original-code Horizons query (C/2025N1, geodeticGBT(-79.8398,38.4331,0.807), original start/stop/1minute grid). Compare candidate-export path/velocities with current response; do not assume the historical solution identical.
- Reproduce original time-median-per-channel division, 3-channel boxcar, rolling/integer drift, global coarse-channel MAD score,9DCbinszeroing, ±1channel ON/OFFmaxfilter, ON>=2.5allthree/OFF<2allthree, and10Hz clustering. Save all clusters, not only first50. Reproduce40false-acceleration controls seed11 and0.03–1Hz/s scaling at1.42GHz; compare README13vs3.75±2.05,max8 with earlier pastedmax10.
- For efficient but faithful computation cache each scan's normalized3-bin rows once. Preservefloat64math and accumulation order; verify selected outputs against original unmodified code. Calibrate every frame's MAD separately as original.
- Export uses clustermean frequency but scores of a separately chosen best member; identify that mapping and do not require rounded mean coordinate to reproduce best score.

## Candidate diagnostics, after reproduction
For all13: reported vs reproduced scores, per-time/per-scan contributions, fixed topocentric feature crosschecks, brightest samples, ON/OFFmorphology and local-neighbor controls. Test C01/C02's supplied interference labels rather than adopt them. Keep source-ID/human-transmitter-ID unresolved unless independently supported.

Inspect method sensitivities separately, without silently changing legacy reproduction: time-median versus frequency-baseline normalization; three-bin smoothing/tolerance; global coordinate spacing versus exact reference rest-grid spacing; circular rolling/edge validity; same-count clustering in true/null; different masks. Selection-bias checks must rerun the whole selection in each control, not treat positive ONmeans of selected candidates as independent evidence.

A metadata concern to audit: uploaded ONscan0017 pointing RA10.86618h andDec6.7017deg differ visibly from uploaded comet coordinates162.722566deg,6.692033deg. Verify original header units and values before interpreting; nominal header coordinates alone do not establish actual pointing/tracking.

## Checkpoint
Persist full-channel inputs and completed computation batches during work. Nextcommand: acquire fullcoarse7withboundedranges, all6files, save each output.


---

# Latest state: GBT1667 reconstruction and extra checks complete, 3 November2026

All six raw cutouts, source hashes, exact ephemeris, acquisition/analysis code and final report are preserved in this completed batch. The report is GBT-1667-excess-audit-2026-11-03.md; evidence package is libfile_130c575875688191881fcdc77c1c6782. Native cutout IDs are in native-input-ledger.json. No unfinished spectral analysis is being claimed as complete.

Result: no exceptional general1667 comet-pointing narrowband excess under this independently defined detector. In±5kHz, thresholds2,2.5,3 empirical MAD units give ON86,19,3 versusOFF99,32,6. A second normalization width gives18ON versus28OFF at2.5. These are NOT Claude's sigma units or his missing13candidate identities.

The strongest ON-minus-OFF feature is distributed over all threeON scans and is not a single-spike artifact, but51of66neighbor windows have an equal/larger contrast maximum. Among40correlated alternative drift curves,38 have an equal/larger ON maximum and28 an equal/larger contrast maximum. No global p-value is claimed. All50new contrast peaks have per-scan/leave-one-out/sample-concentration records; all26at1667 have six-scan waterfalls.

Eighteen native-power injections through complete normalization show the stronger persistent model passing the descriptive ON≥4 andcontrast≥4 gate at3/3placements (amplitude0.6per-samplelocalMAD). At0.15/0.3 and for middle-scan-only injections,0/3 placements pass percase. This is not a completeness curve, voltage simulation, physical upperlimit or proof that every weak/intermittent signal is absent. Fourth condition is not equated with low amplitude.

Ordinary original-file HDF5 reads match64selected saved values bitwise. All six output CRCs and SHA256checked.582,092,902bytes of native cutouts retained from1,907,740,953compressedchunkbytes plusmetadata. Score files, CSVs, plots, fullcodes and original ephemeris are in the final evidence package. Earlier checkpoint statuses below are historical and superseded.

Next substantive action: obtain or locate Claude's exact13candidatecoordinates and score/control/trial definitions, then cross-match them to the already saved native powers. Without that handoff the original13-versus40 statistic cannot be individually adjudicated. Any fresh confirmation must use unexamined observations at the specified1667feature with adequate sensitivity; another receiver band is not direct replication. Keep the unresolved ATA Fig7/8 raw-data audit separate.

---

## Batch2 complete — new1667 track-power reconstruction

All six native raw-power cutouts are now saved (native-input-ledger.json lists their Library IDs). A separate ordinary HDF5 read of original source scan13 agrees bit-for-bit for32 selected values at each OH window (64 values total). No mask dataset exists in that inspected source. All input-file hashes match the acquisition ledger.

New detector, central rest±5kHz,1024-channel baseline:1667 ON connected-peak counts at2,2.5,3 units are86,19,3; OFF counts99,32,6.1665 counts at2.5 are24 ON and24 OFF. Score units are empirical background MAD, NOT Gaussian significance or Claude's sigma. The1667 ON maximum is3.1547 and OFF maximum4.1177. With4096-channel baseline,1667 counts at2.5 are18 ON and28 OFF. No general comet-pointing excess appears under this reconstruction.

The26 selected1667 ON-minus-OFF contrast clusters have a maximum3.37849 at rest1667.363232724MHz (offset+4202.724Hz). This top peak is distributed across all three ON scans (individual scores1.717,1.908,1.266), with aggregateON2.820 andOFF-1.961; it is not dominated by one integration (top two positive samples7.56%). However51 of66 matched neighboring10kHz windows have an equal/larger maximum contrast;64 of66 have an equal/larger ON maximum. Thus it is not exceptional relative to these descriptive controls. No formal global p-value computed; neighboring windows are not independent experiments.

All50 new contrast clusters (26 at1667,24 at1665) have a per-scan ledger and leave-one-ON-scan-out scores. They are not Claude's missing13 candidate identities. The full distributions, continuous tracks, raw spectral medians and threshold curves are saved. At1667,15 of26 contrast-selected peaks have positive scores in all three ON scans, but that is same-data selection and not independent confirmation.

Currently running extra_checks.py: correlated drift-curve multiplier controls,18 power-domain injections through original-power normalization (two occupancies,three amplitudes,three placements), and six-scan waterfalls for every new1667 contrast cluster. No extra-check result is asserted yet. Next: inspect outputs, write bounded final report, update evidence ZIP/checkpoint. Main analysis is already preserved by this batch.

## Batch1 complete — all six GBT native-resolution cutouts acquired

All scans0013–0018 completed, each49 samples, both original0.8MHz windows at2.7939677Hz resolution. Output CRCs and SHA256 verified. Native-input-ledger.json lists each output and downloaded compressed-byte total. Scans13–16 already saved; scans17–18 being saved with this checkpoint. All six raw cutouts are distinct from normalized analysis. The initial source file contains only data, no mask dataset. Selected samples are being independently checked against ordinary HDF5 reads of the original file via validate.py.

Next command: python -u gbt-excess-20261103/analyze.py. Analysis code SHA256 969347848572ea5d4d617e91d62307939a06eb5c7d560221765be80e1777f685. It uses first-sample-center reference, JPL radial-velocity curve, nearest native-bin track sums, empirical per-background MAD units, ON/OFF contrast, stationary-frequency comparison, local median-block widths1024 and4096, central rest-frequency windows±5kHz and nearby-window controls. Threshold counts are descriptive; no global significance claim will be made. Exact Claude detector/frequencies still unavailable. This is an exploratory reconstruction.

## Completed power batches: scans0013–0016

Four of six native-resolution OH scan cutouts have completed and passed ZIP CRC and output hash checks. Scan13 is already saved as libfile_17d429ae470c81919f72cc2c6523fa43; scans14–16 are being persisted with this checkpoint. Scans17–18 still acquiring. No score analysis has been run. First source HDF5 inspection lists only data, no separate mask dataset. Analysis code defines a new detector (1024-channel local median bandpass with4096-channel sensitivity variant), not Claude's unrecovered original statistic.

## Completed power batch: scan0013

Scan0013 native-resolution windows completed and passed ZIP CRC validation. Output GBT-OH-scan0013-2026-11-03.npz, 97,620,813 bytes, SHA256 ebbb776ee940da6ef0a45583891453f80c6c94021228a983ec4df0bbeac01ee8. All49 integrations and both frozen windows retained. Remaining scans acquiring; no statistic evaluated yet. Archive input state and decoding code accompany the evidence package. Resume with acquire.py acquire --scan0 (completed scans can be skipped once outputs verified); currently running sequentially. Save individual scan outputs as they finish.

# Active batch — Green Bank 1667 MHz reconstruction, 3 November 2026

## Batch 1 checkpoint: metadata complete, powers acquiring

All six exact blc23 L-band file headers, channel selections and HDF5 chunk locations are saved. JPL Horizons query uses C/2025 N1 and observer -9@399, verified by response as Green Bank 100-m GBT. Saved response uses JPL#55 solution dated 21 October 2026; this is not necessarily Claude's ephemeris, so exact replication remains unclaimed. Deldot during cadence is about -1.90 to -1.86 km/s, predicting negative frequency drift about -0.11 Hz/s. Both lines fall inside frozen windows.

Native powers have not completed acquisition yet. An initial decoder setup erroneously supplied HDF5-generated bitshuffle filter prefixes as user parameters; no resulting powers were saved. Corrected code supplies block size/codec only and uses HDF5 native memory rather than threaded Python file callbacks. A complete compressed block decoded successfully in this corrected configuration. The current acquisition runs scan13–18 sequentially with eight bounded-range workers, shared physical chunks deduplicated, atomic per-piece state, native-resolution power windows and hashes. Resume only from nonempty completed-piece state and CRC-checked output archives. Code, exact input links, all six metadata records and ephemeris are in GBT-OH-reconstruction-evidence-2026-11-03.zip. Next: finish first scan, save it, then remaining scans. No new excess result yet.


Authorized by Lee: proceed with the investigation. We are acquiring the six L-band scans and small native-resolution OH windows. Exact Claude thirteen-candidate artifacts are still absent; label this as a new exploratory reconstruction. The full frozen batch plan follows and precedes the historical checkpoint. No new power-spectrum result exists yet.

# Green Bank 1667 MHz reconstruction — batch plan

Written 3 November 2026 before retrieving spectral powers for this reconstruction.

## Status and scope
Claude's exact thirteen frequencies, original score definition, trial ledger and code are not available in the current record. This is a new exploratory reconstruction, not a reproduction of that statistic. All six L-band scans have already been examined by Claude; no scan in this cadence will be described as fresh confirmation. Prior ATA work is distinct.

## Batch 1: data and physical checks
1. Enumerate exact public index links for blc23 L-band scans0013–0018, high spectral resolution product0000, and retrieve each header and chunk-location metadata.
2. Obtain JPL Horizons topocentric radial velocities for 3I/ATLAS at Green Bank at scan sample centers; archive query/response. Verify designation and observer location. Apply first-order radial Doppler model with explicit sign; use independent header frequency/time checks.
3. Extract native float32 spectra for every integration over observed 1666.95–1667.75 MHz and1665.00–1665.80 MHz (generous windows around the two laboratory lines allowing ephemeris correction); retain original channel order, exact frequencies, timestamps and raw powers. This interval choice is frozen before power inspection; extend only if verified ephemeris shows it misses required context and document why. Downloaded compressed chunks may cover wider coarse channels; preserve their hashes and trim stored arrays to the stated intervals.
4. Validate range responses, input dimensions, zero masks, finite values, chunk filter decoding and per-scan time coverage. Compare at least one decoded chunk with ordinary HDF5 decoding via an in-memory single-chunk reconstruction.
5. Persist spectra and input manifests after each completed scan. Save batch1 artifacts and update main checkpoint before score analysis.

## Batch 2: exploratory analysis
- Inspect raw/normalized frequency-time spectra, bandpass and coarse-channel boundaries; preserve original arrays.
- Use row local median noise normalization and frequency structure controls with explicit bandwidths; compare a second normalization as sensitivity check.
- Comet-frame constant-rest-frequency track stack versus fixed observer frequency; separate ON(13,15,17)/OFF(14,16,18). Score ON/OFF separately and combined with recorded variances, do not blindly assume equal receiver noise.
- Retain continuous scores and score distributions, counts above 2,2.5,3 as descriptive benchmarks only. Cluster adjacent bins into peaks before interpreting counts.
- Report every selected peak with per-scan contribution, leave-one-ON-scan-out robustness, and corresponding OFF-track scores. Identify single-integration contributions.
- Compare matched nearby-frequency and controlled drift templates on identical valid coverage. Do not assign formal global significance without calibrating complete selection/trials and noise correlations.
- Broad OH emission, bandpass effects and interference remain candidate explanations. Missing1665 counterpart is not mandatory rejection of an artificial emitter model.
- Injection recovery through complete normalization/selection measures sensitivity; statistical score units are not turboSETI units or physical flux/EIRP.
- Any relational/message hypothesis must be specified finitely and tested on unexamined data, not endlessly fit to these scans.

## Immediate next action
Run metadata acquisition; no signal conclusion yet. Code and completed batches must be durable before long continuation.


---

# 3I/ATLAS research: durable checkpoint and recovery handoff

## 1667 MHz follow-up: access verified and next analysis, 3 November 2026

Current user asks how to investigate Claude's reported 1667 MHz excess more deeply. No reproduction of the excess has yet occurred.

Primary sources checked:
- https://seti.berkeley.edu/atlas/ : GBT L-band scans 0013–0018, one six-scan cadence, spectrograms total intensity only. Do not propose polarization analysis on this product.
- https://arxiv.org/html/2512.19763v1 : December 18, 2025 observations; ABACAD three ON and three OFF, five minutes per scan. L-band covers 1.1–1.9 GHz. Paper uses approximately 16-sigma ON and 10-sigma OFF thresholds after software calibration, not Claude's bespoke 2–3-sigma statistic.
- https://bldata.berkeley.edu/ATLAS/GB_ATLAS/ : index opens and lists the six L-band scans and all three spectral products.

Direct public file access works with HTTP 206. Inspected headers for scan 0013 on nodes blc21–blc26 using bounded ranges; all are accessible. Node blc23 is the segment containing both OH lines:
https://bldata.berkeley.edu/ATLAS/GB_ATLAS/blc23_guppi_61027_17226_DIAG_3I_ATLAS_0013.rawspec.0000.h5

Verified scan-0013 metadata: dataset data shape (49,1,67108864), float32, chunks (1,1,1048576), fch1 1688.96484375 MHz, foff -2.7939677238464355e-6 MHz (2.7939677 Hz channel width), tsamp 6.084537002666661 s, tstart MJD 61027.199375. File size 10,205,777,185 bytes. Header/metadata inspection transferred 118,049 bytes for this file. Initial 65,536-byte block SHA256 b01e8a87062a472a894c3df6bbb1a9fb68c522d973cbb9ce5b6d283160b4f673. No power-spectrum cutout has been fetched in this continuation.

The same public index lists blc23 products for:
- 0013, 17226, ON
- 0014, 17543, OFF
- 0015, 17861, ON
- 0016, 18179, OFF
- 0017, 18497, ON
- 0018, 18814, OFF
Use the exact hrefs from the index rather than infer filenames. Only scan0013 metadata has been checked on this pass; verify all remaining headers before extraction. The header's single feed/intensity dimension and official total-intensity description do not preserve separate polarization streams.

Recommended staged follow-up, not yet executed or fully preregistered:
1. Recover Claude's exact 13 candidate frequencies, selection definition, normalization, deduplication, reference epoch, ephemeris and controls. If unavailable, label a new reconstruction rather than claim exact replication.
2. Extract bounded original-resolution context around the 1667 MHz region from all six blc23 scans; inspect bandpass and coarse-channel boundaries, timestamps, channel order and Doppler sign/reference frame. Keep unnormalized powers.
3. Inspect all 13, not a selected four, and cluster adjacent bins/templates into distinguishable features. Produce per-scan and time-bin contributions; leave-one-scan-out is robustness only, because all original scans are already examined.
4. Compare ON/OFF behavior with local-noise normalization and time-variable interference considered. Compare physical comet-frame, stationary receiver-frame, and controlled offset tracks. Different frames must sample comparable noise and not create a misleading control population.
5. Replace the single threshold-count claim with the full score distribution and threshold curve, plus matched controls. Calibrate the complete selection over tested windows, thresholds and track choices; do not treat 40 control drifts as 40 independent sky observations.
6. Compare broad OH-line/background and instrumental models as well as narrow tones. Other OH transition is useful context, not mandatory artificial-signal replication.
7. Test recovery by injecting signals through the entire normalization/selection pipeline over amplitudes, durations and occupancy; publish completeness. This measures what a null can exclude.
8. Actual confirmation requires unexamined observations of the same predicted feature, ideally another epoch/instrument with adequate sensitivity. A different GBT receiver band cannot directly reproduce 1667 MHz. Frozen relational predictions can be tested only after a candidate relation is defined; do not retrofit new symbolic keys indefinitely.

Next concrete deliverable: exact input/candidate ledger, small spectral cutouts, and per-scan contribution table, before another global verdict. Persist that bounded batch and code. The reported 13-versus-controls excess is presently an unresolved exploratory statistic, not a verified astronomical excess or a detected message.



Checkpoint date: 3 November 2026 (updated with user-supplied Claude narrative). Purpose: preserve active task identity, verified outputs, gaps, and the next action across timeouts, usage-limit pauses, context loss, or replacement of the temporary workspace. This checkpoint contains no new astronomical analysis.



## Continuation update — Claude's reported MeerKAT and Green Bank work, 3 November 2026

Source: Lee pasted Claude's account in the current conversation. This recovers a narrative record, not the underlying code, input files, plots, hashes, ephemeris query, or complete candidate ledger. It is not yet established that this is the same interrupted pass described earlier. Keep it separate from our independently saved ATA analyses. The unrelated opening MPAI review in the paste is not astronomical evidence.

### Reported MeerKAT hit-list searches

Claude reports about 6 million hits across five observing days, with 63 other beams as controls. Each hit list is said to include only detections with S/N >= 6.

1. Comet drift: minute-by-minute JPL Horizons predictions, within 0.005 Hz/s; comet-beam match fraction 0.70%, other-beam fraction 1.24%. A December 19 comb at 1276–1281 MHz was labelled Galileo E6 and appeared in all 64 beams. Reported seven-pointing drifts: -0.30, -0.19, -0.005, -0.19, -0.17, -0.09, -0.12 Hz/s; comet prediction approximately -0.18 to -0.12. Agreement only in last pointing weakens simple persistent comet-drift interpretation; specific transmitter ID remains to be audited against files.
2. Comet-frame frequency repeats: 187 recurring frequencies; another statistic counts 358 matches. Across 400 random frame shifts, average 392 matches and 87% tie or exceed true-frame count. Resolve unique-frequency versus pairwise-match units before reproducing.
3. OH windows: ±5 kHz around 1612, 1665, 1667 MHz rest; zero hits in any beam.
4. Hydrogen, H/sqrt(2), H/phi: ±1 kHz in comet frame; zero hits in any beam.
5. A later hydrogen-band candidate around 1420.549–1420.558 MHz on December 19: 449 hits, all 64 beams, all seven pointings over about three hours; S/N 6.7–7.2, slopes spread -10 to +10 Hz/s. Claude reports LSR velocities -1.7 to -3.4 km/s and interprets this as Galactic hydrogen. Shared occurrence and inconsistent slopes undermine a localized comet tone; physical source assignment and velocity transformation not independently reproduced.
6. Important admitted correction: ±20-channel (~32 Hz) beam matching missed counterparts a few kHz away in broad features. Earlier unique-beam counts 310, 47, 628 are overstated and must not be reused as valid localization evidence. Widening a coincidence window must be calibrated for accidental matches; inspect shared spectral morphology rather than use an unlimited window.

### Reported Green Bank raw-spectrum searches

Claude reports six L-band scans and two OH channels, subthreshold tone searches, plus wrong-drift controls:
- 1667 MHz, 2.5 sigma: 13 candidates; 40 wrong-drift controls average about 4, maximum 10.
- 1667 MHz, 3 sigma: 1; controls 0–2.
- 1667 MHz, 2 sigma: 118; controls 121 ± 12.
- 1665 MHz, 2.5 sigma: 5; controls 5.7 ± 2.2, maximum 11; 29/40 tie or beat true frame.
- Four candidate plots reportedly show no convincing track; one is dominated by one scan.
- Reported recovery floor around one third of per-sample noise; injection definitions, completeness versus amplitude, durations, and statistical normalization unavailable.
- Candidate-set structure tests report p = 0.14–0.48 versus size-matched random sets. Nine false-drift frames tested, retaining sets with at least four candidates. No mirrored pairs in either population; mean candidate distance to whole-kHz offsets 0.25 kHz versus false-frame 0.15–0.37 kHz. Metric definitions, selections, and all trials remain needed.

### Limits on interpretation and next audit

These results, if reproduced, support no demonstrated comet-locked narrowband signal in the specific tested data and templates. They do not establish absence of every structured signal or full agreement across every band in the published survey.

- Second OH line absence is a replication failure only for a stated model predicting corresponding structure there. An artificial emitter is not intrinsically required to use both OH transitions.
- A 2.5-sigma-cut excess disappearing at adjacent cuts does not by itself prove fluctuation; both real populations and selection effects can do that. The reported 13 exceeds all 40 controls. If this were a single prespecified exchangeable statistic, the plus-one Monte Carlo tail estimate would be 1/41, not zero; post-selection trials and control validity must be audited before any significance claim.
- Condition 4 (boundary of determinability) does not logically force amplitude below the quoted recovery floor. Ambiguity may concern source, modulation, temporal relation, or interpretation at detectable amplitude.
- Comet-frame tests impose an emitter model. A sender able to control transmission could compensate its apparent drift; a failure of this template is not a general null for deliberate address.
- Reported nonsignificant structure tests mean no detected structure under those statistics, not proof of structure's absence.
- Do not assume every raw spectral product preserves polarization or voltage phase; inspect the actual dataset dimensions and metadata.
- Obtain or locate Claude's filenames, code, ephemeris query, candidate tables, plots, trials ledger, and injection results before calling this independently verified.

### Access update and immediate next action

The archive is a nested public index; do not shift navigation onto Lee. On 3 November, we followed the root to July 5 and July 9 session indexes successfully (HTTP 200). Both explicitly list the required Figure 7/8 scan directories. Those exact directories return 403 from both urllib and web retrieval, with encoded or literal colons; the first listed scan in each of those sessions also returns 403. Known July 3 scan opens, lists 28 subband folders and metadata; a known beam file supports HTTP 206 byte ranges (256 bytes retrieved from a 4,782,367,488-byte file). These results establish request-specific failure, not universal archive inaccessibility. Next substantive steps remain mapping available products ourselves and auditing real rejections, while locating the separate Claude-work artifacts if accessible.


## Latest correction — working public download exists

Lee Sharks reports that he can download the data, but the files are huge. Do not treat earlier assistant HTTP 403 responses as proof of general inaccessibility or assume the archive operators must repair permissions. The assistant has not yet matched Lee's working URL/filename to the exact Fig. 7/8 observations. The new pasted attachment was unavailable, so no content was read from it.

Immediate next action (superseded by 3 November navigation update above): follow the nested public index ourselves; reuse a working URL if already supplied, rather than require Lee to locate it or upload multi-gigabyte data. Compare its identity with the required scan/subband/beam; test a small HTTP byte-range request. If ranges are supported, use the already developed metadata/chunk extraction method to preserve only the needed original-resolution spectral windows, with manifests and hashes. If range access is unavailable, use a resumable download into durable storage or a local cutout workflow. Keep raw power spectra distinct from plots and filtered hit lists. No external message has been sent.

## Current continuation — published human-source examples, batches 1–2

User has authorized continuing the search under all five conditions, including an intention to become recognizable as signal to observers who learn how to look, and double-checking human-source rejections. The active branch is the published-rejection audit, not a synthetic injection exercise.

Batch 1 identifies the authors' Figures 7 and 8 as actual published inspected cases. Figure 7 is centered at 1626.675919 MHz, above Iridium's documented 1626.5 MHz upper service-band edge. This undermines a simple in-band attribution, not the wider possibility of human interference. Figure 8's similar two-beam feature supports spatial rejection but does not identify an emitter. Both exact public scan-directory links currently return HTTP 403; raw-array reanalysis of these cases has not been performed. The report is [ATA-published-rejections-audit-2026-11-02.md](https://chatgpt.com/library?file_id=libfile_dda33beda8108191b9a2c6b1e13fc291&account_id=personal), and the evidence package is [ATA-published-rejections-evidence-2026-11-02.zip](https://chatgpt.com/library?file_id=libfile_9f5bc41d48b48191bf92bafcb93664bb&account_id=personal). Read their latest saved versions on resumption.

Batch 2 complete: CEPT ERC Report 91 explicitly supports a possible Iridium unwanted-emission mechanism above 1626.5 MHz, so the band edge does not rule Iridium out. Both exact and four adjacent example directories returned 403; the old July 3 control remains accessible. A new first-nine/last-ten crossbeam transfer diagnostic on our 15 exploratory candidate windows gives test R² 0.060–0.228. Sixty neighboring-frequency controls also transfer, so common background contributes; no emitter or message is identified. Results and code are in the updated evidence package. Next: obtain accessible paired powers for the published cases or the authors complete rejection ledger, and run a frozen relational search on unexamined accessible observations. Keep authors' candidate identities separate from our own. Persist results and this checkpoint after the batch. The historical recovery record below remains preserved.

## Active task — do not substitute another branch

Lee Sharks asks to recover a specific interrupted pass: looking further at radio features ruled out as human-sourced/terrestrial interference, and testing how solid those classifications were. He reports an hour or more of work on that pass before a gap. The latest assistant response mistakenly discussed a future teaching/decoder test instead of addressing that interrupted audit.

Do not treat synthetic injections, a template-bank null, or a future decoding proposal as the missing real-feature rejection audit. Do not rerun adjacent work and label it recovery of the missing pass. New reconstruction must be identified as new reconstruction.

## Recovery result

Completed research packages survive in durable storage. The present temporary workspace no longer contains the later baseline/readable-signal working directories. The three-scan package was restored in this recovery check and its archive CRCs were verified. Older first-pass and filter-audit ZIPs were also CRC-checked. Named real-feature tables have been recovered.

A distinct later human-source classification audit from the hour described by Lee has **not been located** in the inspected saved-file inventory, current working files, or retrieved conversation context. This does not establish that the work never occurred. Do not claim that the missing pass is safely retained or completed without finding its actual evidence.

The latest substantive saved outputs found in the 2 November file inventory were the readable-signal report/package and revised archive review, saved around 11:59 a.m. Eastern (16:59 UTC). No later substantive research artifact was found in that inventory during this check.

## What does survive

| Work | Verified surviving content | Scope distinction |
|---|---|---|
| First excluded-data pass | Paired spectra and report around 1075 MHz; ZIP CRC checked | Shared feature supports an interference/instrumental interpretation, not identification of a particular human transmitter |
| Filter/code follow-up | 11 real-track rows; archived selector tests; 72 injections; code and arrays; ZIP CRC checked | Our shortlist and source-code behavior; not the authors' complete rejected-hit catalogue |
| Three-scan real-feature follow-up | 15 named maxima and 40 adjacent-scan comparisons; full ZIP restored and CRC checked; tables extracted | Real-feature screening survives; not proof that these were the authors' individually classified 211 final cases |
| Baseline-emitter pass | Report and analysis/spectra packages present in saved-file inventory | A separate physical-trajectory search, not the missing RFI-classification audit |
| Eight-family readable-signal pass | Report read in full; analysis package present in inventory | Expanded model coverage and synthetic recovery; not a replacement for checking actual human-source classifications |

The three-scan record reports that the 15 maxima largely cross or follow shared spectral structures; two time bins account for 63.7–91.0% of their positive beam-difference contribution. None of 40 exact adjacent-scan continuations passed its stated screen. Fourteen looser window comparisons passed, but were not exact recurrence. This supports the limited conclusion of no convincing persistent target-specific line in that sample. It does not identify each transmitter or rule out every possible coexisting weaker component.

Recovered named examples include S0-target-0000 at approximately 1075.010054588 MHz, drift −0.372640190 Hz/s, and S0-target-0002 at approximately 1075.060820580 MHz, drift +0.05 Hz/s. Refer to the recovered CSV for exact stored values and definitions. These are our exploratory maxima, not authenticated IDs from the original survey's rejection ledger.

## Durable file references

- [First excluded-data package](https://chatgpt.com/library?file_id=libfile_b7612f610a80819181b16a3f3f9e82f5&account_id=personal)
- [Filter/code audit package](https://chatgpt.com/library?file_id=libfile_3cf2d2e5c9808191acf61a59eb5a1fa0&account_id=personal)
- [Three-scan real-feature report](https://chatgpt.com/library?file_id=libfile_533c20002e088191a0f5d921f4f89206&account_id=personal)
- [Three-scan data and analysis package](https://chatgpt.com/library?file_id=libfile_6f7ab05ea5688191bb1b1fd0e15d9785&account_id=personal)
- [Baseline report](https://chatgpt.com/library?file_id=libfile_4eaf891f124c8191beb093c4e58efc1b&account_id=personal)
- [Baseline analysis package](https://chatgpt.com/library?file_id=libfile_859f52be87c48191bf1133ac14264170&account_id=personal)
- [Baseline spectra package](https://chatgpt.com/library?file_id=libfile_f61c525436548191bee7e5850e30f54a&account_id=personal)
- [Readable-signal report](https://chatgpt.com/library?file_id=libfile_8fdb6d0d835c81919363e236ba63a28c&account_id=personal)
- [Readable-signal analysis package](https://chatgpt.com/library?file_id=libfile_490eb1973bf08191abe8cc161b8b1e7d&account_id=personal)
- [Archive review, current version](https://chatgpt.com/library?file_id=libfile_972eb58bcec48191b1158ce7f769f809&account_id=personal)

## Unresolved materials and next substantive action

The inspected saved reports state that the exact executed blanking script, complete signed pre/post-filter hit catalogues, full rejection ledger, and study-specific final plotting population had not been obtained. A statistical or spatial screen suggesting RFI must not be silently upgraded to identification of a human transmitter.

Before restarting research, read this checkpoint and the current three-scan report, inspect the restored per-candidate tables, and identify which real-feature branch Lee means from any available contemporaneous evidence. If no later pass can be recovered, state that limitation and label any continuation as a new reconstruction. Continue the human-source rejection question, not an unrelated decoder-learning study.

For a reconstructed audit, the first deliverable should be a per-feature ledger: original source/candidate identifier if available; observation coordinates; exact rejection reason and executed-rule evidence; same-time other-beam evidence; neighboring-frequency and adjacent-epoch checks; evidence for a specific terrestrial emitter versus generic interference; alternative explanations; and what remains unresolved. Keep our new candidates distinct from the authors' candidates.

## Checkpoint procedure for subsequent work

This is an execution requirement from Lee's request, not a claim that live processes or unsaved memory can survive interruption.

1. Update this same checkpoint before a long run: task, branch, frozen choices, inputs and hashes, command, output paths, and the next action.
2. Break work into bounded batches. At the end of each completed batch, write its results and rejection reasons to files; atomically finish those files; update this checkpoint with completed versus pending work.
3. Persist the partial results and checkpoint as versions during the work, rather than waiting for a polished final report. Inspect each save result. An unconfirmed save is not durable completion.
4. On resumption, read the latest saved checkpoint first, restore the named files, validate inputs, and resume from the last confirmed batch. Never infer that a process is still running because an earlier message said it was.
5. If an interruption happens within an unfinished batch, that batch may need rerunning. Preserve earlier completed batches and disclose the gap; do not silently replace the active task with an adjacent one.

The companion recovery evidence ZIP contains the saved-file inventory, CRC/hash verification receipts, recovered 15-row candidate and 40-row continuation tables, and the 11-row filter-audit shortlist. It does not purport to contain the missing later pass.

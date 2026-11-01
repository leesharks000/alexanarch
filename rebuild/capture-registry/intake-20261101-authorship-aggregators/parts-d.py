"""Part d (session, 2026-11-01 02:20 EDT): Pessoa Digital. Held at first: its census row had no readable source (both pages refused with http 418).
The operator supplied the Cologne Center for eHumanities' project page for it (02:14 EDT, 'is this the one we want?'); the census fetched that page
(pessoa-digital--cceh), rewrote the row from it (a participant's account, basis third_party), and the capture is read against that row here."""
from helpers import *

s = "pessoa-digital"
parts = {}
parts[s] = mk(s, "Pessoa Digital",
  aset(s, {
    "name": (["pessoadigital.pt", "Pessoa Digital"], None, ["link"]),
    "operator": (["Ulrike Henny", "Henny-Krahmer", "Pedro Sepúlveda", "Jorge Uribe", "ELAB", "CCeH", "Cologne Center for eHumanities"], "Edited by Ulrike Henny-Krahmer, Pedro Sepúlveda and Jorge Uribe; begun with ELAB (Universidade Nova de Lisboa) and the CCeH.", ["editors", "participants"]),
    "date": (["2014"], "Begun at the CCeH in 2014–2016, ongoing since then.", ["runtime"]),
    "claim boundary": ([], "A digital edition of the editorial projects and publications of Fernando Pessoa.", ["self_description"]),
    "corpus": ([], "Pessoa's handwritten notes, lists and plans for his work, juxtaposed with his works published during his lifetime.", ["record_object"]),
    "commitments": ([], "TEI transcriptions, facsimiles, indexes of persons, journals and titles, and visualizations (timelines, a network of persons).", ["holdings"]),
    "lineage": (["FCT", "Fundação para a Ciência e a Tecnologia", "DCH", "EAFIT"], "Funded by the FCT; hosted by the DCH; the cooperation extended to EAFIT University, Medellín.", ["funding", "host", "extended"])},
    "A web resource: its own pages refused automated requests on 2026-11-01; the Cologne Center for eHumanities' project page, saved 2026-11-01, describes it as a digital edition of the editorial projects and publications of Fernando Pessoa. A site, read on the site template."),
  [A("name", True, "Digital Edition of Fernando Pessoa (pessoadigital.pt)"),
   A("operator", True, "Cologne Center for eHumanities (CCeH)"),
   A("date", False),
   A("claim boundary", True, "A digital scholarly edition and research framework dedicated to the works and manuscripts of the renowned Portuguese writer Fernando Pessoa (1888–1935)."),
   A("corpus", False),
   A("commitments", False),
   A("lineage", True, "The digital edition is hosted by the DCH.")],
  {"kind": "collision", "abn": False, "span": "The term Pessoa Digital most commonly refers to digital academic and archival projects dedicated to the Portuguese poet Fernando Pessoa, or to municipal digital services in Brazil.",
   "basis": "The edition reached as the first of two senses of the name, beside João Pessoa na Palma da Mão, the municipal app of João Pessoa, Brazil, which takes the second section and three of the five cards."},
  "'PESSOA DIGITAL' ON THE OVERVIEW — THE EDITION FIRST OF TWO SENSES, BESIDE A BRAZILIAN CITY'S APP; THE PLANS AND LISTS IT EDITS NOT CARRIED; THE CCeH MADE THE HOST OF ESTRANHAR PESSOA",
  ("THE EDITION'S NAME, SIGNED OUT, 2026-11-01: 'The term Pessoa Digital most commonly refers to digital academic and archival projects dedicated to the Portuguese poet Fernando Pessoa, or to municipal digital services in Brazil.' "
   "Section 1, the Digital Edition of Fernando Pessoa (pessoadigital.pt): 'A digital scholarly edition and research framework'; it 'connects with ... the Estranhar Pessoa project hosted by the Cologne Center for eHumanities (CCeH) and the National Library of Portugal collection'. "
   "Section 2, João Pessoa na Palma da Mão, the municipality's app of 'over 200 municipal services'. Cards: the CCeH's project page, the University of Rostock's page on the edition, three Instagram videos on the app."),
  "The innocent reading first. Given a two-word name shared by a scholarly edition and a city's services, the Overview gives both senses, the edition first, and asks which the user wants.",
  ["THE EDITION REACHED, AT THE GRAIN OF ITS KIND. 'A digital scholarly edition and research framework dedicated to the works and manuscripts' of Pessoa: the CCeH's page gives 'a digital edition of the editorial projects and publications of the Portuguese author Fernando Pessoa (1888–1935)'. "
   "What it edits is not carried: 'Above all, handwritten notes, lists and plans with which Pessoa conceived his work are edited. These will be juxtaposed with his works published during his lifetime' (the CCeH's page). The plans and lists in which Pessoa assigned his works to their names are the edition's object and the census's reason for holding it.",
   "THE HOST MISASSIGNED. The composition has 'the Estranhar Pessoa project hosted by the Cologne Center for eHumanities (CCeH)'. The CCeH's page, carded first, says 'The digital edition is hosted by the DCH' and points to Estranhar Pessoa as a framework project 'running since mid-2013' at its own address. The CCeH was a participant in the edition (2014–2016); the editors (Ulrike Henny-Krahmer, Pedro Sepúlveda, Jorge Uribe) are named on the CCeH's page and nowhere in the composition.",
   "THE SECOND SENSE. João Pessoa na Palma da Mão, an app of the municipality of João Pessoa in Brazil, takes the second section and three of the five cards, all Instagram videos. The edition's title as the University of Rostock card gives it, 'Fernando Pessoa. Projects and Publications', is not composed."],
  "The edition reached first and at its kind, with its host misassigned and its object, Pessoa's plans and lists for his own work, left out; a Brazilian city's app shares the name and three of the five cards.",
  [C("Cologne Center for eHumanities", "Pessoa Digital - CCeH - Das Cologne Center for eHumanities", "The digital edition is hosted by the DCH. Further information on the Estranhar Pessoa framework project, which has been running since mid-2013, can be found at ..."),
   C("Universität Rostock", "development and sustainability measures for the Digital Edition of Fernando Pessoa", "Jul 4, 2023 — The digital scholarly edition \"Fernando Pessoa. Projects and Publications\" (http://www.pessoadigital.pt) was originally created as part of a ..."),
   C("Instagram·TV Cidade João Pessoa", "A população de João Pessoa conta com uma ferramenta digital que facilita o ...", None, "third_party", "the municipal app (homonym)"),
   C("Instagram·TV Cidade João Pessoa", "O aplicativo 'João Pessoa na Palma da Mão' passa a contar, nesta sexta-feira (9) ...", None, "third_party", "the municipal app (homonym)"),
   C("Instagram·Valentina Tem Jp", "⚠️UTILIZEM O APP⚠️ O app \"João Pessoa na Palma da Mão\" é a plataforma ...", None, "third_party", "the municipal app (homonym)")],
  {"author": False, "inst": True, "id": False, "src": True},
  "The edition named with its domain and a participant institution; its editors and host not named, the host misassigned.")
write(parts)

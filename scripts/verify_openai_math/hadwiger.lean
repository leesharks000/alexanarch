import Mathlib
import OAI.Combinatorics.HadwigerCounterexample.Main
/-- K_t minor: t disjoint nonempty connected branch sets, pairwise joined by an edge. Written here. -/
def AlexanarchCliqueMinor {V : Type} (G : SimpleGraph V) (t : ℕ) : Prop :=
  ∃ B : Fin t → Set V,
    (∀ i, (G.induce (B i)).Connected) ∧
    (∀ i j, i ≠ j → Disjoint (B i) (B j)) ∧
    (∀ i j, i ≠ j → ∃ v ∈ B i, ∃ w ∈ B j, G.Adj v w)
noncomputable def alexanarchHadwiger {V : Type} (G : SimpleGraph V) : ℕ :=
  sSup {t : ℕ | AlexanarchCliqueMinor G t}
/-- Hadwiger's conjecture fails, with the minor notion defined in this file. -/
theorem alexanarch_not_hadwiger :
    ¬ (∀ (m : ℕ) (G : SimpleGraph (Fin m)), G.chromaticNumber ≤ ↑(alexanarchHadwiger G)) :=
  OAI.HadwigerCounterexample.not_hadwiger_conjecture
#print axioms alexanarch_not_hadwiger

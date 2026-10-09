import Mathlib
import OAI.RingTheory.DirectFiniteness.Main
/-- Kaplansky's direct-finiteness conjecture fails: restated here from Mathlib terms only. -/
theorem alexanarch_kaplansky :
    ∃ (K : Type) (_ : Field K) (_ : Fintype K) (_ : CharP K 2),
      ∃ (G : Type) (_ : Group G) (_ : Group.FG G),
        ∃ a b : MonoidAlgebra K G, a * b = 1 ∧ b * a ≠ 1 :=
  OAI.KaplanskyCounterexample.main_theorem
#print axioms alexanarch_kaplansky

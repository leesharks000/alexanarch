import Mathlib
import OAI.NumberTheory.DirichletL.Nonvanishing
/-- Mathlib's Riemann zeta has no zero with real part above 7/8. -/
theorem alexanarch_zeta_seven_eighths {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0 :=
  OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re hs
#print axioms alexanarch_zeta_seven_eighths

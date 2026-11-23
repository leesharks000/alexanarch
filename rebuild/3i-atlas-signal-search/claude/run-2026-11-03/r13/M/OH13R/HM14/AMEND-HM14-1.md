# PLAN-HM14, amendment 1 (before any product)

The first run was stopped after ten minutes with no session complete and nothing written (hm14-run1.log is empty): `np.load` of a compressed npz decompresses an array on every access, and the inner loop touched each scan's window array once per cohort and candidate. The amendment reads each array once per session. Arithmetic unchanged.

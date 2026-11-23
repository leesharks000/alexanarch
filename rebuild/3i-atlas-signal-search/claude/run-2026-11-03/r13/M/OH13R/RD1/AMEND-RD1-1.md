# PLAN-RD1, amendment 1 (before any product)

The first run stopped at its first file open, before any statistic or product existed (rd1.log of the first run, kept as rd1-run1.log): `from common import *` brought in common.py's HERE, the OH13R folder, over this module's, so the window index was sought one folder too high and the outputs would have been written outside RD1. The same defect as FD's first amendment (notebook §8.15). Amendment: the module's own folder is RD; the window index is read from common's HERE, where the products are. Nothing else is changed.

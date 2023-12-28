# TODO: score generation

# Table 2
python3 src/evaluation_mt/tab_ref_quality_orig.py

# Table 3
python3 src/evaluation_mt/tab_ref_quality_pe.py --aggregate random --annotator student
python3 src/evaluation_mt/tab_ref_quality_pe.py --aggregate random --annotator layman
python3 src/evaluation_mt/tab_ref_quality_pe.py --aggregate random --annotator professional

# Table 4
python3 src/evaluation_mt/tab_ref_quantity.py --aggregate average
python3 src/evaluation_mt/tab_ref_quantity.py --aggregate max

# Figure 1
python3 src/evaluation_mt/fig_ref_quantity.py

# Table 5
python3 src/evaluation_mt/tab_ref_scores.py
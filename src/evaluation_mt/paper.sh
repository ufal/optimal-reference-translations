# TODO: score generation

# Table 1
python3 src/evaluation_mt/exp_ref_quality_orig.py

# Table 2
python3 src/evaluation_mt/exp_ref_quality_pe.py --aggregate random --annotator student
python3 src/evaluation_mt/exp_ref_quality_pe.py --aggregate random --annotator layman
python3 src/evaluation_mt/exp_ref_quality_pe.py --aggregate random --annotator professional
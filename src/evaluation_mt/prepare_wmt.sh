
# setup
mkdir -p data/data_tmp/
pip3 install git+https://github.com/google-research/mt-metrics-eval.git
alias mtme='python3 -m mt_metrics_eval.mtme'
mtme --download

mtme -t wmt20 -l en-cs --scores | tail -n +2 > ~/optimal-reference-translations/data/data_tmp/scores.tsv
mtme -t wmt20 -l en-cs --echosys doc,src > ~/optimal-reference-translations/data/data_tmp/text.tsv

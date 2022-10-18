1. Install pyDCOP:
 ```
git clone https://github.com/Orange-OpenSource/pyDcop.git
cd pyDcop
pip install .
 ```

2. Change direction to the 'DCOP' folder and then run:
 ```
pydcop --output /results/DCOP/results_mgm2.json solve --algo mgm2 --collect_on period --period 300 --run_metric /results/DCOP/metrics_mgm2.csv matrix.yaml
 ```
   
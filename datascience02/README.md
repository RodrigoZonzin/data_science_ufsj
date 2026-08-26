git clone https://github.com/RodrigoZonzin/data_science_ufsj.git
cd datascience02
conda env create -f environment.yml
conda activate label_prop
python3 label_prop.py {nome do arquivo}

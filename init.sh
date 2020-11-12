git clone https://github.com/digital-cube/BASE.git base  
cd base
git checkout devel
cd -


cd users
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd .venv/lib/python3.8/site-packages
ln -sf ../../../../../base .
cd -

cd contacts
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd .venv/lib/python3.8/site-packages
ln -sf ../../../../../base .
cd -

rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd .venv/lib/python3.8/site-packages
ln -sf ../../../../base .
cd -

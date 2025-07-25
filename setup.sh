mkdir -p ~/.streamlit

echo "\
[server]\n\
port = \$PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
2. Install Git LFS and fetch the actual .pkl files
apt-get update && apt-get install -y git-lfs
git lfs install
git lfs pull

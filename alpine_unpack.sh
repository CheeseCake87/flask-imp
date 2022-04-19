if ! hash python3; then
  echo "python is not installed"
  apk add python3
  apk add python3-dev
fi

python3 apline_install.py
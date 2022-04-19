if ! hash python3; then
  echo "python is not installed"
  apk add python3
  apk add python3-dev
fi

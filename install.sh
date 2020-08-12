if [ -a /usr/local/bin/python3 ]; then
  echo "Python3 is present, installing remaining dependencies..."
  mkdir ~/Library/Application\ Support/Seiri
  mkdir ~/Library/Application\ Support/Seiri/Scripts
  mv ./seiri.py ~/Library/Application\ Support/Seiri/Scripts
  echo "Done! ✅"
else
  echo "Install Python3 first"
fi

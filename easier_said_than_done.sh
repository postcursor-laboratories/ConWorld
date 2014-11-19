set -x # @ECHO ON for those from .bat(ch) files
echo 'Yea, it works, k?' > itworks.txt
bundle install --deployment --binstubs
cd forums
iced -I window -c -o js/ cs/


# MySQL
First, set up a MySQL database on port 5000, and create a table `last_battery_measures`

sudo mysql -u root -p
root : caramel


# install on raspberry
sudo apt-get update
sudo apt-get dist-upgrade
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install gcc g++ make
sudo apt-get install -y nodejs
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
sudo apt-get install -y nodejs
sudo npm install -g @angular/cli
cd ~/prog/rpy_battery_tester/angularapp
npm install

# Run the app
ng serve
# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# Set Environment Variables
export AD_URL="ldap://freeipa.example.org"
export AD_DOMAIN="EXAMPLE.ORG"
export AD_BASEDN="cn=users,cn=accounts,dc=example,dc=org"
export AD_BINDDN='uid=admin,cn=users,cn=accounts,dc=example,dc=org'
export AD_BINDDN_PASSWORD="password"
export SECRET_KEY="deesohshoayie6PiGoGaghi6thiecaingai2quab2aoheequ8vahsu1phu8ahJio"
export ZOHO_AUTHTOKEN="add-your-auth-token"
export PAYPAL_RECEIVER_EMAIL="money@vagrant.lan"

# Update the System
#sudo pacman -Syu --noconfirm
pacman -Syy
pacman -S archlinux-keyring --noconfirm

# Set Timezone
timedatectl set-timezone America/Chicago

# Setup locale.gen
cat << EOF > /etc/locale.gen
en_US.UTF-8 UTF-8  
en_US ISO-8859-1  
EOF
locale-gen

# Install Dependencies 
pacman -S --noconfirm --needed postgresql samba nginx redis

# Setup Samba
samba-tool domain provision --realm=vagrant.lan --domain=${AD_DOMAIN} --server-role=dc --use-rfc2307 --adminpass=${AD_BINDDN_PASSWORD}
systemctl start samba
systemctl enable samba

# Set Shell Environment Variables
cat << EOF >> .bashrc
export AD_URL=${AD_URL}
export AD_DOMAIN=${AD_DOMAIN}
export AD_BASEDN=${AD_BASEDN}
export AD_BINDDN=${AD_BINDDN}
export AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}
export SECRET_KEY=${SECRET_KEY}
export ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}
export PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}
source venv/bin/activate
EOF

#  Setup Database
chmod 755 /home/vagrant
sudo -u postgres initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'
systemctl start postgresql
systemctl enable postgresql
sudo -u postgres createuser --superuser vagrant
sudo -u vagrant createdb ps1auth

# Bootstrap App

sudo -u vagrant python -m venv venv
sudo -u vagrant venv/bin/pip install -r /vagrant/requirements/local.txt
sudo -u vagrant venv/bin/pip install gunicorn
sudo -u vagrant -E venv/bin/python /vagrant/manage.py syncdb --noinput

# Setup systemd environment file
cat << EOF > /home/vagrant/ps1auth.conf
AD_URL=${AD_URL}
AD_DOMAIN=${AD_DOMAIN}
AD_BASEDN=${AD_BASEDN}
AD_BINDDN=${AD_BINDDN}
AD_BINDDN_PASSWORD=${AD_BINDDN_PASSWORD}
SECRET_KEY=${SECRET_KEY}
ZOHO_AUTHTOKEN=${ZOHO_AUTHTOKEN}
PAYPAL_RECEIVER_EMAIL=${PAYPAL_RECEIVER_EMAIL}
EOF


# PS1Auth Systemd Service File
cat << EOF > /etc/systemd/system/ps1auth.service
[Unit]
Description=PS1 Auth (Members site)
After=vboxservice.service

[Service]
Type=simple
User=vagrant
WorkingDirectory=/vagrant
ExecStart=/home/vagrant/venv/bin/gunicorn --log-level debug ps1auth.wsgi:application --reload
EnvironmentFile=-/home/vagrant/ps1auth.conf

[Install]
WantedBy=multi-user.target
EOF

# PS1Auth systemd socket file
cat << EOF > /etc/systemd/system/ps1auth.socket
[Socket]
ListenStream=/tmp/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Nginx config
cat << EOF > /etc/nginx/nginx.conf
error_log /var/log/nginx/error.log;
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    access_log /var/log/nginx/access.log combined;
    upstream ps1auth
    {
        server unix:/tmp/gunicorn.sock fail_timeout=0;
    }
    server {
        listen       8001;
        server_name  _;
        client_max_body_size 4G;
        keepalive_timeout 5;
        root /vagrant;
        location / {
            proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
            proxy_set_header Host \\$http_host;
            proxy_redirect off;
            proxy_pass   http://ps1auth;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
EOF

# PS1Auth Celery Worker Systemd Service File
cat << EOF > /etc/systemd/system/celery.service
[Unit]
Description=PS1 Auth Celery Worker
After=vboxservice.service

[Service]
Type=simple
User=vagrant
WorkingDirectory=/vagrant
ExecStart=/home/vagrant/venv/bin/celery -A ps1auth worker -l info
EnvironmentFile=-/home/vagrant/ps1auth.conf
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure App to Start Automatically
systemctl start ps1auth.socket
systemctl enable ps1auth.socket
systemctl start nginx
systemctl enable nginx
systemctl start redis
systemctl enable redis
systemctl start celery
systemctl enable celery
systemctl start systemd-journal-gatewayd.socket
systemctl enable systemd-journal-gatewayd.socket

SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|


	config.vm.define "ipa-server" do |ipaserver| 
		ipaserver.vm.box = "vStone/centos-7.x-puppet.3.x"

		# The hostname MUST match the main IP address of the host, and be specified
		# as such in /etc/hosts. As such, this Vagrantfile depends on the 
		# vagrant-hosts plugin.
		ipaserver.vm.hostname = "freeipa.example.org"
		ipaserver.vm.network "private_network", ip: "192.168.65.4"
		ipaserver.vm.provision :hosts do |provisioner|
			provisioner.add_host '192.168.65.4', ['freeipa.example.org']
		end
		ipaserver.vm.provision "shell", inline: <<-SHELL
		sed -i 's/127.0.1.1.*freeipa.example.org.*//' /etc/hosts
		SHELL


		# Forwarding interesting ports from 
		# http://docs.fedoraproject.org/en-US/Fedora/15/html/FreeIPA_Guide/installing-ipa.html#tab.ipa-ports:
		# Web UI:
		ipaserver.vm.network "forwarded_port", guest: 443, host: 4443
		# LDAP:
		ipaserver.vm.network "forwarded_port", guest: 389, host: 3389
                ipaserver.vm.provider "virtualbox" do |v|
                  v.memory = 1024
                  v.cpus = 1
                end

		# And install freeipa:
		ipaserver.vm.provision "shell", inline: <<-SHELL
		puppet module install huit/ipa
		SHELL
		ipaserver.vm.provision "puppet" do |puppet|
			puppet.manifest_file = "default.pp"
		end
	end
	config.vm.define "ps1auth-server" do |ps1auth|
		ps1auth.vm.box = "archlinux-x86_64"
		ps1auth.vm.box_url = "http://cloud.terry.im/vagrant/archlinux-x86_64.box"
		# Set up a private network on the same net as the freeipa box
		ps1auth.vm.network "private_network", ip: "192.168.65.5"
		ps1auth.vm.provision :hosts do |provisioner|
			provisioner.add_host '192.168.65.4', ['freeipa.example.org']
		end

		ps1auth.vm.provision "shell", inline: $script
		ps1auth.vm.network "forwarded_port", guest: 5555, host: 5555, auto_correct: true
		ps1auth.vm.network "forwarded_port", guest: 8001, host: 8001, auto_correct: true
		ps1auth.vm.network "forwarded_port", guest: 19531, host: 8002, auto_correct: true
		ps1auth.vm.provider "virtualbox" do |v|
			v.memory = 1024
			v.cpus = 2
		end
	end
end

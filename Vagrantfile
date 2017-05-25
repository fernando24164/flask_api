# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "debian/jessie64"
  config.vm.hostname = "api"

  server_ip = "192.168.0.42"
  cpus = 1

  config.vm.provision "shell" do |s|
    s.path = "bootstrap.sh"
    s.args = [server_ip, cpus]
  end

  config.vm.network :private_network, ip: server_ip
  config.vm.network "forwarded_port", guest: 80, host: 5000

  config.vm.provider "virtualbox" do |v|
    v.name = "api"
    v.memory = 256
    v.cpus = cpus
  end

end

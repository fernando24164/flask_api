# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
BOX_NAME = "debian/jessie64"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define "api" do |subconfig|
    subconfig.vm.box = BOX_NAME
    subconfig.vm.hostname = "api"
    subconfig.vm.network :private_network, ip: "192.168.15.3"
    subconfig.vm.synced_folder "./", "/app/api", type: "rsync", rsync_exclude: ".git"
    subconfig.vm.provider "virtualbox" do |v|
      v.memory = 64
      v.cpus = 1
    end
    subconfig.vm.provision "shell" do |s|
      s.path = "bootstrap.sh"
    end
end

# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provision "shell", path: "pg_config.sh"
  # config.vm.box = "hashicorp/precise32"
  # http://stackoverflow.com/questions/18457306/enable-internet-access-inside-vagrant
  #config.vm.provider "virtualbox" do |v|
  #    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  #    v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  #end
  config.vm.box = "ubuntu/trusty32"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.define "resthost" do |resthost|
  end
end

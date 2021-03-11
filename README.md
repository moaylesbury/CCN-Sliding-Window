## Virtual machine setup

All the assignment can be done inside the VM created in the following way.

1. Install [Virtualbox 6.1](https://www.virtualbox.org/) and
   [Vagrant](https://www.vagrantup.com/) in your computer. If you use Windows,
also install [Git for Windows](https://gitforwindows.org/).
2. Create an *empty* directory somewhere you can remember.
3. Copy or download [Vagrantfile](./Vagrantfile) in this directory.  
4. Open a terminal (Mac or Linux) or Git Bash (Windows).
5. Go to the directory that includes [Vagrantfile](./Vagrantfile) using `cd` command.
6. Launch a VM with:
```
vagrant up
```

This will take about 10-30 minutes in the first time, and slightly shorter in
the later times because the base VM image has been cached.
Below is some basic commands to control the VM (comments after #)
```
vagrant ssh      # login to the vm
vagrant halt     # shut down the vm
vagrant destroy  # delete the vm
```
Note that these commands must be run in the same directory with
[Vagrantfile](./Vagrantfile).

In the VM console window, you can login to the VM with "vagrant" for both
username and password.

Files in the Vagrantfile directory can be seen inside the vm, which appear in /vagrant.

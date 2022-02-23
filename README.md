# Ansible Project
Update Invetory with your host machines IP address and Credentials

Use ansible-vault to encrypt password for invemtory
* Command for encrypting password: ansible-vault encrypt_string 'Your String/Password' --ask-vault-pass

Command to run Playbooks
ansible-playbook -i your_inventory.yml -v your_playbook.yml

P1 Member Access System - The SSH:C Fork
========================================

About this fork
---------------

Basically, this sets up a FreeIPA server alongside the ps1auth box.
It's configured to talk to it, but hasn't been tested past that. It all boots,
that's all I've tested so far. -- @cswingler.
 

Getting Started with Vagrant
============================

    vagrant up

Creating a user
===============

    vagrant ssh
    cd /vagrant
    ./manage.py createsuperuser

Viewing the site
================

open a browser to http://127.0.0.1:8001 on the host machine

class { 'ipa':
  master  => true, # Only one master per Puppet master
  domain  => 'example.org',
  realm   => 'EXAMPLE.ORG',
  adminpw => 'password',
  dspw    => 'password',
  require => File['/etc/yum.repos.d/epel.repo']
}

package { 'epel-release':
  ensure => installed
}

file { '/etc/yum.repos.d/epel.repo':
  ensure => present,
  content => '[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
#baseurl=http://download.fedoraproject.org/pub/epel/7/$basearch
mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch
failovermethod=priority
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7',
  require => Package['epel-release']
}



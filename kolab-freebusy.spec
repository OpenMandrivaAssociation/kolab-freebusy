%define prj Kolab_FreeBusy

%define xmldir  %{_var}/lib/pear
%define peardir %(pear config-get php_dir 2> /dev/null)
%define cachedir %{_var}/cache/freebusy

Name:          kolab-freebusy
Version:       0.1.5
Release:       %mkrel 1
Summary:       A package for providing free/busy information
License:       LGPL
Group:         Networking/Mail
Url:           http://pear.horde.org/index.php?package=%{prj}
Source0:       %{prj}-%{version}.tgz
BuildArch:     noarch
PreReq:        %{_bindir}/pear
Requires:      php-pear
Requires:      horde-framework
Requires:      horde-date
Requires:      horde-icalendar
Requires:      kolab-storage
Requires:      kolab-server
Requires:      php-dba
BuildRequires: horde-framework
BuildRequires: php-pear
BuildRequires: php-pear-channel-horde
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%description
This package provides free/busy information for the users of a Kolab server.
A Kolab client changing calendar data in an IMAP folder is required to call
the triggering script provided within this package via HTTP. This will
refresh the cache maintained by this package with partial free/busy data.
This partial data sets are finally combined to the complete free/busy
information once a client requests this data for a particular user.

%prep
%setup -q -n %{prj}-%{version}
%__cp %{SOURCE0} %{prj}-%{version}.tgz

%build

%install
pear -d www_dir=/srv/www/htdocs/freebusy install --packagingroot %{buildroot} --nodeps --offline %{prj}-%{version}.tgz

%__rm -rf %{buildroot}/%{peardir}/.{filemap,lock,registry,channels,depdb,depdblock}

%__mkdir_p %{buildroot}%{xmldir}
%__cp %{_builddir}/package.xml %{buildroot}%{xmldir}/%{prj}.xml
install -d -m 750 %{buildroot}%{cachedir}

%clean
%__rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/%{prj}.xml

%postun
if [ "$1" -eq "0" ]; then
  pear uninstall --nodeps --ignore-errors --register-only pear.horde.org/%{prj}
fi

%files
%defattr(-, root, root)
%{xmldir}/%{prj}.xml
%dir %{peardir}/Horde/Kolab
%dir %{peardir}/Horde/Kolab/FreeBusy
%{peardir}/Horde/Kolab/FreeBusy.php
%{peardir}/Horde/Kolab/FreeBusy/Access.php
%{peardir}/Horde/Kolab/FreeBusy/Cache.php
%{peardir}/Horde/Kolab/FreeBusy/Imap.php
%{peardir}/Horde/Kolab/FreeBusy/View.php
%{peardir}/Horde/Kolab/FreeBusy/Report.php
%dir %{peardir}/Horde/Kolab/Test
%{peardir}/Horde/Kolab/Test/FreeBusy.php
%dir %{peardir}/docs/Kolab_FreeBusy
%{peardir}/docs/Kolab_FreeBusy/COPYING
%dir %{peardir}/tests/Kolab_FreeBusy
%dir %{peardir}/tests/Kolab_FreeBusy/Horde
%dir %{peardir}/tests/Kolab_FreeBusy/Horde/Kolab
%dir %{peardir}/tests/Kolab_FreeBusy/Horde/Kolab/FreeBusy
%{peardir}/tests/Kolab_FreeBusy/Horde/Kolab/FreeBusy/AllTests.php
%{peardir}/tests/Kolab_FreeBusy/Horde/Kolab/FreeBusy/FreeBusyTest.php
%{peardir}/tests/Kolab_FreeBusy/Horde/Kolab/FreeBusy/FreeBusyScenarioTest.php
%dir /srv/www/htdocs/freebusy
%config /srv/www/htdocs/freebusy/config.php
/srv/www/htdocs/freebusy/freebusy.php
/srv/www/htdocs/freebusy/pfb.php
/srv/www/htdocs/freebusy/regenerate.php
%attr(750,wwwrun,www) %{cachedir}

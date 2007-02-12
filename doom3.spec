# NOTE: You could add to your 'mirrors', to get stuff downloaded:
#  ftp://dl.xs4all.nl/pub/mirror/idsoftware/idstuff/doom3/linux/
# TODO:
#  - package dedicated server - doomded.x86
#  - check if system libstdc++ and libgcc_s can be used
#    answered here: http://zerowing.idsoftware.com/linux/doom/#head-d15dfbca9b3ba90b9bacb7476ad2f0afe3bb0f72
#    so? we are not gentoo.
#  - check license?
#
# Conditional build:
%bcond_with	demo	# package demo data
%define		demo_version 1.1.1286
#
Summary:	Doom III - 3rd installment of the classic id 3D first-person shooter
Summary(de.UTF-8):	Doom III - der dritte Teil des FPP Klassikers von id Software
Summary(pl.UTF-8):	Doom III - trzecia część klasyki FPP z id Software
Name:		doom3
Version:	1.3.1302
Release:	0.8
Vendor:		id Software
License:	DOOM3
Group:		Applications/Games
Source0:	ftp://ftp.idsoftware.com/idstuff/doom3/linux/%{name}-linux-%{version}.x86.run
# NoSource0-md5:	b1d04da2d64bb8d54f64cbaa2fdb4490
Source1:	ftp://ftp.idsoftware.com/idstuff/doom3/linux/%{name}-linux-%{demo_version}-demo.x86.run
# NoSource1-md5:	81dcf8ead198f14844c554b25e07abbe
Source2:	%{name}.desktop
NoSource:	0
NoSource:	1
URL:		http://www.doom3.com/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		_noautoprov		libgcc_s.so.1 libstdc++.so.5
%define		_noautoreq		libgcc_s.so.1 libstdc++.so.5
%define		_gamelibdir		%{_libdir}/games/doom3
%define		_gamedatadir	%{_datadir}/games/doom3

%description
Doom III for Linux.

To play the game you need to copy data files from your Doom III CD or
you could try playing demo by installing %{name}-demo package.

%description -l de.UTF-8
Doom III für Linux.

Um das Spiel zu spielen musst du die Dateien aus deiner Doom III CD
kopieren oder du kannst das Demo ausprobieren indem du %{name}-demo
installierst.

%description -l pl.UTF-8
Doom III dla Linuksa.

Do grania trzeba skopiować pliki danych z płyty Doom III, albo można
spróbować grać w wersji demo instalując pakiet %{name}-demo.

%package demo
Summary:	Doom III Demo data files
Summary(de.UTF-8):	Doom III Demo Dateien
Summary(pl.UTF-8):	Pliki danych Doom III Demo
Group:		Applications/Games
Version:	%{demo_version}
# main package version is mostly bigger than demo itself.
Requires:	%{name} >= %{demo_version}

%description demo
This package contains the data files for Doom III Demo.

%description demo -l de.UTF-8
Dieses Packet enthält Dateien für das Doom III Demo.

%description demo -l pl.UTF-8
Ten pakiet zawiera pliki danych dla gry Doom III Demo.

%prep
%setup -qcT
%if %{with demo}
sh %{SOURCE1} --tar xf
%endif
# here we overwrite files which are shared with demo package. that's intentional
sh %{SOURCE0} --tar xf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_gamelibdir},%{_gamedatadir}/{demo,base}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_bindir}}

install libgcc_s.so.1 libstdc++.so.5 $RPM_BUILD_ROOT%{_gamelibdir}
install bin/Linux/x86/doom.x86 $RPM_BUILD_ROOT%{_gamelibdir}

install %{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

cat << 'EOF' > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
# Needed to make symlinks/shortcuts work.
# the binaries must run with correct working directory
cd %{_gamelibdir}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
exec ./doom.x86 "$@"
EOF

%if %{with demo}
install gamex86.so $RPM_BUILD_ROOT%{_gamelibdir}
install demo/* $RPM_BUILD_ROOT%{_gamedatadir}/demo
ln -s %{_gamedatadir}/demo $RPM_BUILD_ROOT%{_gamelibdir}/demo
%endif

install base/* $RPM_BUILD_ROOT%{_gamedatadir}/base
ln -s %{_gamedatadir}/base $RPM_BUILD_ROOT%{_gamelibdir}/base

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License.txt README version.info
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_gamelibdir}
%attr(755,root,root) %{_gamelibdir}/doom.x86
%attr(755,root,root) %{_gamelibdir}/libgcc_s.so.1
%attr(755,root,root) %{_gamelibdir}/libstdc++.so.5
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%dir %{_gamedatadir}
%dir %{_gamedatadir}/base
%{_gamedatadir}/base/*
%{_gamelibdir}/base

%if %{with demo}
%files demo
%defattr(644,root,root,755)
%attr(755,root,root) %{_gamelibdir}/gamex86.so
%dir %{_gamedatadir}/demo
%{_gamedatadir}/demo/*
%{_gamelibdir}/demo
%endif

# NOTE: You could add to your 'mirrors', to get stuff downloaded: 
#  ftp://dl.xs4all.nl/pub/mirror/idsoftware/idstuff/doom3/linux/
# TODO:
#  - package dedicated server - doomded.x86, I couldn't get doom3 running so I
#  wasn't interested anymore :)
#  - check if system libstdc++ and libgcc_s can be used
#  - check license?
#
# Conditional build:
%bcond_with	demo	# package demo data
#
Summary:	Doom III - 3rd installment of the classic id 3D first-person shooter
Summary(pl):	Doom III - trzecia czê¶æ klasyki FPP z id Software
Name:		doom3
Version:	1.1.1286
Release:	0.1
Vendor:		id Software
License:	DOOM3
Group:		Applications/Games
Source0:	ftp://ftp.idsoftware.com/idstuff/doom3/linux/doom3-linux-%{version}.x86.run
# NoSource0-md5:	2a45d0769b39473887c61a11cbba981c
Source1:	ftp://ftp.idsoftware.com/idstuff/doom3/linux/doom3-linux-%{version}-demo.x86.run
# NoSource1-md5:	81dcf8ead198f14844c554b25e07abbe
Source2:	%{name}.desktop
NoSource:	0
NoSource:	1
URL:		http://www.doom3.com/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		_noautoprov	libgcc_s.so.1 libstdc++.so.5
%define		_gamedir	/usr/%{_lib}/games/doom3

%description
Doom III demo for Linux.

%description -l pl
Demo Doom III dla Linuksa.

%prep
%setup -qcT
sh %{SOURCE0} --tar xf
sh %{SOURCE1} --tar xf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_gamedir}/{demo,base} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_bindir}}

install gamex86.so $RPM_BUILD_ROOT%{_gamedir}
install libgcc_s.so.1 libstdc++.so.5 $RPM_BUILD_ROOT%{_gamedir}
install bin/Linux/x86/doom.x86 $RPM_BUILD_ROOT%{_gamedir}

install %{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
# Needed to make symlinks/shortcuts work.
# the binaries must run with correct working directory
cd %{_gamedir}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
exec ./doom.x86 "$@"
EOF

%{?with_demo:install demo/* $RPM_BUILD_ROOT%{_gamedir}/demo}

install base/* $RPM_BUILD_ROOT%{_gamedir}/base

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License.txt README version.info
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_gamedir}
%attr(755,root,root) %{_gamedir}/doom.x86
%attr(755,root,root) %{_gamedir}/gamex86.so
%attr(755,root,root) %{_gamedir}/libgcc_s.so.1
%attr(755,root,root) %{_gamedir}/libstdc++.so.5

%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png

%if %{with demo}
%dir %{_gamedir}/demo
%{_gamedir}/demo/*
%endif

%dir %{_gamedir}/base
%{_gamedir}/base/*

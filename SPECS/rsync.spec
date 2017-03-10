%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}

Summary: A program for synchronizing files over a network
Name: opt-rsync
Version: 3.1.0
Release: _BUILDNUMBER._DISTRO
Group: Applications/Internet
URL: http://rsync.samba.org/
Packager: Patrick Marcotte <adumos@gmail.com>

Source0: https://download.samba.org/pub/rsync/src/rsync-%{version}.tar.gz
Source1: https://download.samba.org/pub/rsync/src/rsync-patches-%{version}.tar.gz
BuildRequires: libacl-devel, libattr-devel, autoconf, popt-devel, zlib-devel
Requires: zlib
License: GPLv3+

%define _prefix /opt/rsync

Patch0: rsync-3.1.0-fadvise.patch

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

%prep -n rsync-%{version}

%setup -q -n rsync-%{version}
%setup -q -b 1 -n rsync-%{version}

chmod -x support/*

#Needed for compatibility with previous patched rsync versions
patch -p1 -i patches/acls.diff
patch -p1 -i patches/xattrs.diff
#Enable --copy-devices parameter
patch -p1 -i patches/copy-devices.diff
#Adds --drop-cache option
%patch0 -p1 -b .fadvise

%build -n rsync-%{version}
rm -fr autom4te.cache
autoconf -o configure.sh
autoheader && touch config.h.in

%configure

make proto
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall INSTALLCMD='install -p'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/rsync

%post

%preun

%postun

%changelog
* Thu Apr 21 2016 Patrick Marcotte <adumos@gmail.com> - 3.1.0-1
- Update to release 3.1.0-2

* Thu Apr 21 2016 Patrick Marcotte <adumos@gmail.com> - 3.1.0-1
- Added fadvise patch for --drop-cache support

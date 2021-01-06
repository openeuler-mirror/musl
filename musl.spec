Name:		musl
Version:	1.2.0
Release:	1
Summary:	An implementation of the standard library for Linux-based systems

License:	MIT
URL:		https://musl.libc.org
Source0:	%{url}/releases/%{name}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	gnupg2
%description
musl is an implementation of the C standard library built
on top of the Linux system call API, including interfaces
defined in the base language standard, POSIX, and widely
agreed-upon extensions. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

%package libc
Summary:	Fully featured lightweight standard C library for Linux
Provides:	%{name}-libs%{?_isa} = %{version}-%{release}

%description libc
musl is an implementation of the C standard library built
on top of the Linux system call API, including interfaces
defined in the base language standard, POSIX, and widely
agreed-upon extensions. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.
This package provides the system dynamic linker library.
It also provides the dynamic libraries for linking
programs and libraries against musl.

%package devel
Summary:	Development files for %{name}
Provides:	%{name}-headers%{?_isa} = %{version}-%{release}
Requires:	%{name}-libc = %{version}-%{release}
Recommends:	%{name}-libc-static = %{version}-%{release}

%description devel
musl is an implementation of the C standard library built
on top of the Linux system call API, including interfaces
defined in the base language standard, POSIX, and widely
agreed-upon extensions. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.
This package provides header files and other required files
for developers.

%package libc-static
Summary:	Static link library for %{name}
Provides:	%{name}-static%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description libc-static
musl is an implementation of the C standard library built
on top of the Linux system call API, including interfaces
defined in the base language standard, POSIX, and widely
agreed-upon extensions. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.
This package provides the additional development files for
statically linking musl into programs and libraries.

%prep
%setup

%build
export LDFLAGS="%{?build_ldflags} -Wl,-soname,ld-musl.so.1"
%configure --enable-debug --enable-wrapper=no
%make_build

%install
%make_install
mkdir -p %{buildroot}/lib/
mv %{buildroot}%{_libdir}/libc.so %{buildroot}/lib/ld-musl.so.1
ln -sr %{buildroot}/lib/ld-musl.so.1 %{buildroot}%{_libdir}/ld-musl.so.1
ln -sr %{buildroot}%{_libdir}/ld-musl.so.1 %{buildroot}%{_libdir}/libc.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libcrypt.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libdl.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libm.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libpthread.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libresolv.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/librt.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libutil.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libxnet.so
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libc.so.6
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libcrypt.so.1
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libdl.so.2
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libm.so.6
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libpthread.so.0
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libresolv.so.2
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/librt.so.1
ln -sr %{buildroot}%{_libdir}/libc.so %{buildroot}%{_libdir}/libutil.so.1

%files libc
%license COPYRIGHT
/lib/ld-musl.so.1
%{_libdir}/*.so*

%files devel
%license COPYRIGHT
%doc README WHATSNEW
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.o
%{_libdir}/*.a
%exclude %{_libdir}/libc.a

%files libc-static
%license COPYRIGHT
%{_libdir}/libc.a

%changelog
* Fri Dec 4 2020 tangmeng5 <tangmeng5@huawei.com> - 1.2.0-1
- package init

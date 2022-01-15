# Ensure the value is set correctly
%ifarch %{ix86}
%global _musl_target_cpu i386
%endif
 
%ifarch %{arm}
%ifarch armv3l armv4b armv4l armv4tl armv5tl armv5tel armv5tejl armv6l armv7l
%global _musl_target_cpu arm
%else
%global _musl_target_cpu armhf
%endif
%global _musl_platform_suffix eabi
%endif
 
%ifarch %{mips64}
%global _musl_target_cpu mips64
%endif
 
%ifarch %{mips32}
%global _musl_target_cpu mips
%endif
 
%ifarch ppc
%global _musl_target_cpu powerpc
%endif
 
%ifarch %{power64}
# POWER architectures have a different name if little-endian
%ifarch ppc64le
%global _musl_target_cpu powerpc64le
%else
%global _musl_target_cpu powerpc64
%endif
%endif
 
%ifnarch %{ix86} %{arm} %{mips} %{power64} ppc
%global _musl_target_cpu %{_target_cpu}
%endif
 
# Define the platform name
%global _musl_platform %{_musl_target_cpu}-linux-musl%{?_musl_platform_suffix}
%global _musl_gcc_platform %{_musl_target_cpu}-linux-musl-gcc 

%global _libdir %{_prefix}/musl/lib
%global _includedir %{_prefix}/musl/include

Name:		musl
Version:	1.2.2
Release:	2
Summary:	An implementation of the standard library for Linux-based systems

License:	MIT
URL:		https://musl-libc.org
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
	
%package gcc
Summary:	Wrapper for using gcc with musl
Requires:	%{name}-devel = %{version}-%{release}
Requires:	gcc
 
%description gcc
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety. 
This package provides a wrapper around gcc to compile
programs and libraries with musl easily.

%prep
%autosetup

%build
export LDFLAGS="%{?build_ldflags} -Wl,-soname,ld-musl.so.1"
%configure --enable-debug --enable-wrapper=gcc
%make_build

%install
%make_install
mkdir -p %{buildroot}/lib/
mv %{buildroot}%{_libdir}/libc.so %{buildroot}/lib/ld-musl.so.1
ln -sr %{buildroot}/lib/ld-musl.so.1 %{buildroot}%{_libdir}/ld-musl.so.1
ln -sr %{buildroot}%{_bindir}/musl-gcc %{buildroot}%{_bindir}/%{_musl_gcc_platform}
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

%files gcc
%license COPYRIGHT
%{_bindir}/musl-gcc
%{_bindir}/%{_musl_gcc_platform}
%{_libdir}/musl-gcc.specs

%changelog
* Mon Oct 25 2021 zhuyan <zhuyan34@huawei.com> - 1.2.2-2
- fix compile error

* Fri Sep 24 2021 zhuyan <zhuyan34@huawei.com> - 1.2.2-1
- upgrade to 1.2.2

* Tue Aug 19 2021 zhuyan <zhuyan34@huawei.com> - 1.2.0-3
- fix CVE-2020-28928

* Tue May 11 2021 Jiajie Li <lijiajie11@huawei.com> - 1.2.0-2
- Add musl-gcc support

* Fri Dec 4 2020 tangmeng5 <tangmeng5@huawei.com> - 1.2.0-1
- package init

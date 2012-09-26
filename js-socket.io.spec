%define		plugin	socket.io
Summary:	Socket.IO client for the browser
Name:		js-%{plugin}
Version:	0.9.10
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/LearnBoost/socket.io-client/tarball/%{version}/%{plugin}-%{version}.tgz
# Source0-md5:	1896bc0a6631587ae089ae1152ffac9d
URL:		https://github.com/LearnBoost/socket.io-client
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
The 'socket.io' client is basically a simple HTTP Socket interface
implementation. It looks similar to WebSocket while providing
additional features and leveraging other transports when WebSocket is
not supported by the user's browser.

%package demo
Summary:	Demo for %{plugin}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{plugin}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{plugin}.

%prep
%setup -qc
mv *-%{plugin}-client-*/* .

# Apache1/Apache2 config
cat > apache.conf <<'EOF'
Alias /js/%{plugin} %{_appdir}
<Directory %{_appdir}>
	Allow from all
	Options +FollowSymLinks
</Directory>
EOF

# lighttpd config
cat > lighttpd.conf <<'EOF'
alias.url += (
	"/js/%{plugin}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -p dist/%{plugin}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p dist/%{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

cp -p dist/*.swf  $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md History.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

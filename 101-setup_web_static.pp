# sets up your web servers for the deployment of web_static

# Nginx config file
$nginx_config = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-served-By ${hostname};
    root /var/www/html;
    index index.html index.htm;
    location /hbnb_static {
            alias /data/web_static/current;
            index index.html index.htm;
    }
    location /redirect_me {
        return 301 https://th3-grOOt.tk;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
} _>

file { '/data':
  ensure => 'directory'
} _>

file { '/data/web_static':
  ensure => 'directory'
} _>

file { '/data/web_static/releases':
  ensure => 'directory'
} _>

file { '/data/web_static/releases/test':
  ensure => 'directory'
} _>

file { '/data/web_static/shared':
  ensure => 'directory'
} _>

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School puppet\n"
} _>

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} _>

exec { 'chown -R ubuntu:ubuntu /data/':
  command => ['/usr/bin/', '/usr/local/bin/', '/bin/'],
} _>

file { '/var/www':
  ensure => 'directory'
} _>

file { '/var/www/html':
  ensure => 'directory'
} _>

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n"
} _>

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
} _>

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_config
} _>

exec { 'nginx restart':
  command => '/etc/init.d/nginx restart',
}

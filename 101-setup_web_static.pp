# web_server_setup.pp

# Install Nginx
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { ['/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => '<html><body>Holberton School Testing Nginx Setup</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  force   => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    location / {
        # Your existing configuration
    }
}",
  notify  => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure  => running,
  enable  => true,
}

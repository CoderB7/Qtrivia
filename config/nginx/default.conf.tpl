upstream qtrivia {
    server 127.0.0.1:8000;
}

server {

    listen 80;
    server_name 127.0.0.1

    location / {
        proxy_pass      http://localhost:8000;
        include         /etc/nginx/proxy_params;
        autoindex on;
    }

    location /media/ {
        root /home/userb/user_ubuntu/Python Udemy davomi/Python Projects/QTrivia/qtrivia/media;
    }

}

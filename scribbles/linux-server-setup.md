# Complete Guide: Deploying Flask on Your Always-On Laptop

Hosting a Flask portfolio on an old home laptop is a fantastic way to utilize old hardware. This technical markdown documentation shows exactly how to configure the server environment.

---

## Step 1: Prevent Laptop from Sleeping when Lid is Closed
Ubuntu desktop environments put the system to sleep when the lid is closed. To bypass this, edit the system logind configuration:

```bash
sudo nano /etc/systemd/logind.conf
```

Find and uncomment (or append) the following settings:
```ini
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

Restart the systemd login daemon to apply:
```bash
sudo systemctl restart systemd-logind
```

---

## Step 2: Establish the Directory & Virtual Environment
Extract the portfolio and create a dedicated virtual workspace:

```bash
unzip terminal-portfolio.zip -d ~/terminal-portfolio
cd ~/terminal-portfolio

# Create local environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install Flask mistune gunicorn
```

---

## Step 3: Run Gunicorn as a Background System Service
Create a permanent system service so the portfolio starts automatically whenever your laptop boots:

```bash
sudo nano /etc/systemd/system/portfolio.service
```

Paste the following configurations (adjusting paths to your user directory):

```ini
[Unit]
Description=Gunicorn instance to serve Terminal Portfolio
After=network.target

[Service]
User=yubi
Group=www-data
WorkingDirectory=/home/yubi/terminal-portfolio
Environment="PATH=/home/yubi/terminal-portfolio/venv/bin"
ExecStart=/home/yubi/terminal-portfolio/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start portfolio
sudo systemctl enable portfolio
```

---

## Step 4: Configure Nginx Reverse-Proxy
Nginx manages incoming web requests on standard ports (80/443) and forwards them to Gunicorn:

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/portfolio
```

Add the server block structure:
```nginx
server {
    listen 80;
    server_name your_domain.com; # Or your local server IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 5: Secure with SSL (Let's Encrypt)
Apply free certificates to encrypt user connections:

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your_domain.com
```

Select choice `2` to automatically redirect all standard HTTP requests to encrypted HTTPS connections! Your terminal portfolio is now live, secure, and hosting right from your closet.

# Task02

## Task Description

Imagine a server with the following specs:

- 4 times Intel(R) Xeon(R) CPU E7-4830 v4 @ 2.00GHz
- 64GB of ram
- 2 tb HDD disk space
- 2 x 10Gbit/s nics

The server is used for SSL offloading and proxies around 25000 requests per second. Please let us know which metrics are interesting to monitor in that specific case and how would you do that?  What are the challenges of monitoring this?

## Thinking Process

A few things that still unknown that might help in understanding the metrics:
- Details of processor specification.
- Disk I/O speed not present, but seems like SSL offloading more CPU heavy we might not need it.
- OS and service (nginx / haproxy) configuration.

So I search for E7-4830 in result it is a 8 cores cpu with 16 threads ([source](https://ark.intel.com/content/www/us/en/ark/products/53676/intel-xeon-processor-e7-4830-24m-cache-2-13-ghz-6-40-gt-s-intel-qpi.html)). So in total We will have 48 cores CPU with 96 threds. So the full specs are:

- 48 Cores threads CPU.
- 64GB of RAM.
- 2 TB of HDD
- 2x10Gbit Network

From my point of view some *performance* metrics that are very interesting to monitor are:
- Latency.
- Time per request and
- Number of failed requests.

Some tools to monitor is already build in in the linux. For example:
```bash
# monitor the number of tcp connection
$ ss -s 
sh-5.0$ ss -s
Total: 1845
TCP:   120 (estab 55, closed 35, orphaned 0, timewait 13)

Transport Total     IP        IPv6
RAW       2         1         1        
UDP       25        24        1        
TCP       85        76        9        
INET      112       101       11       
FRAG      0         0         0      

# get the memory usage in gigabyte
$ free -g
free -g
              total        used        free      shared  buff/cache   available
Mem:             62          12          33           1          17          49
Swap:             0           0           0
```

A long term solution is to run haproxy and enable stats since some important information already there and can be monitor via web. I'd try to setup a simple service with haproxy in front to monitor the incoming requests.


## Implementation

I'm using a few tools:
- Vagrant.
- Ansible for easier configuration management.

I currently run the setup With linux as working environment.
```bash
uname -a
Linux endurance 5.7.9-arch1-1 #1 SMP PREEMPT Thu, 16 Jul 2020 19:34:49 +0000 x86_64 GNU/Linux
```

First initialize Vagrantfile.
```bash
vagrant init ubuntu/xenial64
```

Configure the cpu and memory of the virtual machine by modifying these value in Vagrantfile.
```ruby
  vb.memory = 8192
  vb.cpus = 6

# And add steps to install haproxy and golang
  apt-get update
  apt-get install -y haproxy golang-go
```

Then do SSH to vagrant to do a bit configuration.
```bash
vagrant ssh
```

I run a simple web server.
```bash
$ go run simple-web.go &
```

try to curl
```bash
$ curl localhost:8090/hello
hello
```

Inside the vagrant I add these configuration
```
...
frontend local_server
    bind localhost:8080
    mode http
    default_backend local_web_server

backend local_web_server
    mode http
    balance roundrobin
    option forwardfor
    http-request set-header X-Forwarded-Port %[dst_port]
    http-request add-header X-Forwarded-Proto https if { ssl_fc }
    option httpchk HEAD / HTTP/1.1rnHost:localhost
    server localhost 127.0.0.1:8090

listen stats
    bind 127.0.0.1:8081
    mode http
    stats enable
    stats hide-version
    stats realm Haproxy\ Statistics
    stats uri /
```

Then try to restart HAProxy
```
$ sudo systemctl restart haproxy.service 

# Try to access the web server via haproxy
$ curl localhost:8080/hello
hello

# Try to access stats
$ curl localhost:8081/stats
<a long http response>

# Then exit the virtual machine
exit
```

Update the Vagrant to do port forwarding so it can be accessed from outside the VM.
```ruby
config.vm.network "forwarded_port", guest: 8080, host: 9080, protocol: "tcp"
config.vm.network "forwarded_port", guest: 8081, host: 9081, protocol: "tcp"
```

From outside the VM we'll be able to hit HAproxy stats by accessing [http://127.0.0.1:8081/stats](http://127.0.0.1:8081/stats)

for further testing we can do a simple load test to the VM and monitor the stats.